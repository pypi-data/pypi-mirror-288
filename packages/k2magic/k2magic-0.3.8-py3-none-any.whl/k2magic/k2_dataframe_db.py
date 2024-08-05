import re
from datetime import datetime
from typing import Union

import pandas as pd
from requests.auth import HTTPBasicAuth

from k2magic.dialect import k2a_requests
from sqlalchemy import make_url, literal, URL, text, and_, MetaData, Table, String, Integer, Column, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.visitors import traverse

from k2magic.dataframe_db import DataFrameDB
from k2magic.dataframe_db_exception import DataFrameDBException
from k2magic.dialect.k2a_repo_wrapper import modify_timestamp, modify_case


class K2DataFrameDB(DataFrameDB):
    """
    扩展DataFrameDB，提供访问K2Assets Repo数据的能力（原生方式，非REST方式）
    """

    def __init__(self, db_url, schema=None):
        db_url_obj = make_url(db_url)
        self.behind_repo = (db_url_obj.drivername == 'k2assets+repo')
        self.repo_meta = _fetch_repo_meta(db_url_obj)
        if self.behind_repo:
            db_url_obj = disclose_db_url(db_url_obj, self.repo_meta)

        super().__init__(db_url_obj, schema)

        self.metadata = build_engine_meta(self.repo_meta)

    def get_repo_data(self, table_name: str, start_time: Union[str, int, datetime], end_time: Union[str, int, datetime],
                      devices: list = None,
                      columns: list = None, limit: int = None, order_by: list = None):
        # 统一参数类型
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        elif isinstance(start_time, int):
            start_time = datetime.fromtimestamp(start_time / 1000)
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        elif isinstance(end_time, int):
            end_time = datetime.fromtimestamp(end_time / 1000)

        # 若没有指定schema前缀则添加self.schema前缀
        if (self.schema is not None) and ('.' not in table_name):
            table_name = f"{self.schema}.{table_name}"

        if table_name in self.metadata.tables:
            table = self.metadata.tables[table_name]
        else:
            raise DataFrameDBException(f"Table '{table_name}' does not exist")

        try:
            with self.engine.connect() as conn:
                query = table.select()
                if columns:
                    # PG repo: 数据库中使用的列名都是小写
                    # if self.behind_repo:
                    #     if self.engine.name == "postgresql":
                    #         columns = [item.lower() for item in columns]
                    query = query.with_only_columns(*(table.c[col] for col in columns))
                # 时间过滤条件
                query = query.where(and_(table.c.k_ts >= int(start_time.timestamp() * 1000),
                                         table.c.k_ts < int(end_time.timestamp() * 1000)))

                # 设备过滤条件
                query = query.where(table.c.k_device.in_(devices))

                # if group_by:
                #     query = query.group_by(*[text(col) for col in group_by])
                if order_by:
                    query = query.order_by(*[text(col) for col in order_by])
                if limit:
                    query = query.limit(limit)

                if self.behind_repo:
                    if self.engine.name == "postgresql":
                        # 处理小写
                        query = traverse(obj=query, opts={},
                                         visitors={"binary": modify_case, "textclause": modify_case,
                                                   "column": modify_case})
                        # 处理原始表里的纳秒，转换为毫秒返回给用户
                        query = traverse(obj=query, opts={},
                                         visitors={"textclause": modify_timestamp, "column": modify_timestamp,
                                                   "binary": modify_timestamp})
                        query = query.with_only_columns(*((table.c[col] / literal(1000000)).label('k_ts')
                                                          if col == 'k_ts' else table.c[col] for col in columns))
                print('Query: ', str(query))
                cursor_result = conn.execute(query)

                result = pd.DataFrame(cursor_result.fetchall(), columns=cursor_result.keys())

                # 将k_ts列转为datetime类型 （原始查询结果里是str，原因待查）
                # datetime带有时区信息
                result['k_ts'] = result['k_ts'].astype(float)
                result['k_ts'] = pd.to_datetime(result['k_ts'], unit='ms', utc=True).dt.tz_convert('Asia/Shanghai')

                return result
        except SQLAlchemyError as e:
            raise DataFrameDBException(
                "Failed to query records due to a database error.",
                original_exception=e
            )


def disclose_db_url(repo_db_url: URL, repo_meta: dict) -> URL:
    """
    将 k2assets+repo:// 开头的 conn_url 转换为底层数据库的 conn_url
    实现方式是先从repo获取元信息，然后让SQLAlchemy直接访问底层数据
    :param repo_db_url: 使用URL类型避免密码明文泄露
    :return:
    """
    if repo_db_url.drivername != 'k2assets+repo':
        raise ValueError("Not a valid url (k2assets+repo://) to dispose")
    storage = repo_meta['storage']
    if storage == 'postgresql':
        jdbc_url = repo_meta['jdbc_url']
        if jdbc_url.startswith('jdbc:'):
            jdbc_url = jdbc_url[5:]
        jdbc_url_obj = make_url(jdbc_url)
        jdbc_url_obj = jdbc_url_obj.set(drivername='postgresql+psycopg2', username=repo_meta['jdbc_user'],
                                        password=repo_meta['jdbc_password'])
        # jdbc_url_obj = jdbc_url_obj.set(host='192.168.132.167', port=5432)
        jdbc_url_obj = jdbc_url_obj.set(query={})  # 否则psycopg2报错ProgrammingError
    return jdbc_url_obj


def build_engine_meta(repo_meta) -> MetaData:
    metadata = MetaData()

    # 遍历列表中的每个字典
    for column_info in repo_meta['columns']:
        # 提取表名
        repo_name = column_info['repoName']

        # 检查表是否已经存在于MetaData中
        if repo_name not in metadata.tables:
            # 如果表不存在，创建一个新的Table对象
            table = Table(repo_name, metadata)

        # 根据类型创建Column对象
        if column_info['type'] == 'string':
            column = Column(column_info['name'], String)
        elif column_info['type'] == 'long':
            column = Column(column_info['name'], Integer)
        elif column_info['type'] == 'double':
            column = Column(column_info['name'], Float)
        else:
            print(f"Ignored unknown type column {column_info['name']}")

        # 将Column对象添加到对应的Table对象中
        metadata.tables[repo_name].append_column(column)
    return metadata


def _fetch_repo_meta(url: URL) -> dict:
    """
    获取Repo底层数据库的配置信息，如数据库类型、ip地址、用户名等。

    返回结果举例：
    {
      'storage': 'postgresql',
    	'jdbc_url': 'jdbc:postgresql://k2a-postgresql:5432/repos?currentSchema=public',
    	'jdbc_user': 'k2data',
    	'jdbc_password': 'K2data1234',
    	'jdbc_conn_pool_size': '20',
    	'batch_insert_size': '500',
    	'batch_insert_pool_size': '1',
    	'key_varchar_len': '256',
    	'varchar_len': '1024',
    	'completeness_stats_cache': 'true',
    	'latest_data_cache': 'true'
    }
    :param url:
    :return:
    """
    if url.drivername != 'k2assets+repo':
        raise ValueError("Not a valid url (k2assets+repo://) to fetch")

    result = {}
    protocol = url.query.get('protocol', 'https')  # k2assets http protocol
    auth = HTTPBasicAuth(url.username, url.password)
    tenant = url.query.get('tenant', None)

    # 获取repo的storage类型，一并放在返回的dict里（key为"storage")
    api_url = f"{protocol}://{url.host}:{url.port}/api/v2/repos/{url.database}"
    data = k2a_requests.get(api_url, auth=auth, tenant=tenant)
    result['storage'] = data.get('body').get('storageInfo').get('name')

    # 获取repo的meta-settings
    api_url = f"{protocol}://{url.host}:{url.port}/api/v2/repos/{url.database}/meta-settings"
    data = k2a_requests.get(api_url, auth=auth, tenant=tenant)
    settings = data.get('body').get('items')

    # 将json里的items转为dict类型
    for item in settings:
        name = item['name']
        pref_value = item['prefValue']
        if pref_value is None:
            pref_value = item['defaultValue']

        # 顺便翻译${}包裹的环境变量，例如${K2BOX_POSTGRESQL_URL}
        pattern = r'\$\{([a-zA-Z0-9_]+)\}'

        def replace(match):
            param_name = match.group(1)
            env_url = f"{protocol}://{url.host}:{url.port}/api/env/{param_name}"
            response2 = k2a_requests.get(env_url, auth=auth, tenant=tenant)
            return response2.get('body').get('values').get(param_name)

        pref_value = re.sub(pattern, replace, pref_value)

        result[name] = pref_value

    # 获取repo的数据结构
    api_url = f"{protocol}://{url.host}:{url.port}/api/v2/repos/{url.database}/columns?from=schema"
    data = k2a_requests.get(api_url, auth=auth, tenant=tenant)
    columns = data.get('body').get('all')
    result['columns'] = columns

    return result

