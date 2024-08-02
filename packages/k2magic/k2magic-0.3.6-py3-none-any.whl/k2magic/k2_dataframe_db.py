import re
from datetime import datetime
from typing import Union

import pandas as pd
from requests.auth import HTTPBasicAuth
from sqlalchemy.testing import in_

from k2magic.dialect import k2a_requests
from sqlalchemy import make_url, literal, URL, text, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.visitors import traverse

from k2magic.dataframe_db import DataFrameDB
from k2magic.dataframe_db_exception import DataFrameDBException
from k2magic.dialect.k2a_repo_wrapper import modify_timestamp


class K2DataFrameDB(DataFrameDB):
    """
    扩展DataFrameDB，提供访问K2Assets Repo数据的能力（原生方式，非REST方式）
    """

    def __init__(self, db_url, schema=None):
        db_url_obj = make_url(db_url)
        self.behind_repo = (db_url_obj.drivername == 'k2assets+repo')
        if self.behind_repo:
            db_url_obj = disclose_db_url(db_url_obj)

        super().__init__(db_url_obj, schema)

    def get_repo_data(self, table_name: str, start_time: Union[str, int, datetime], end_time: Union[str, int, datetime], devices: list = None,
                      columns: list = None, limit: int = None, order_by: list = None):
        # 统一参数类型
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        if isinstance(start_time, int):
            start_time = datetime.fromtimestamp(start_time / 1000)
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if isinstance(end_time, int):
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
                    if self.behind_repo:
                        if self.engine.name == "postgresql":
                            columns = [item.lower() for item in columns]
                    query = query.with_only_columns(*(table.c[col] for col in columns))
                # 时间过滤条件
                query = query.where(and_(table.c.k_ts >= int(start_time.timestamp()*1000), table.c.k_ts < int(end_time.timestamp()*1000)))

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
                                         visitors={"binary": modify_timestamp, "textclause": modify_timestamp,
                                                   "column": modify_timestamp})
                        # 处理纳秒
                        query = traverse(obj=query, opts={}, visitors={"textclause": modify_timestamp,
                                                                       "column": modify_timestamp})
                        query = query.with_only_columns(*((table.c[col] / literal(1000000)).label('k_ts')
                                                          if col == 'k_ts' else table.c[col] for col in columns))
                print('Query: ', str(query))
                result = conn.execute(query)
                return pd.DataFrame(result.fetchall(), columns=result.keys())
        except SQLAlchemyError as e:
            raise DataFrameDBException(
                "Failed to query records due to a database error.",
                original_exception=e
            )


def disclose_db_url(repo_db_url: URL) -> URL:
    """
    将 k2assets+repo:// 开头的 conn_url 转换为底层数据库的 conn_url
    实现方式是先从repo获取元信息，然后让SQLAlchemy直接访问底层数据
    :param repo_db_url: 使用URL类型避免密码明文泄露
    :return:
    """
    if repo_db_url.drivername != 'k2assets+repo':
        raise ValueError("Not a valid url (k2assets+repo://) to dispose")
    meta = _fetch_repo_meta(repo_db_url)
    storage = meta['storage']
    if storage == 'postgresql':
        jdbc_url = meta['jdbc_url']
        if jdbc_url.startswith('jdbc:'):
            jdbc_url = jdbc_url[5:]
        jdbc_url_obj = make_url(jdbc_url)
        jdbc_url_obj = jdbc_url_obj.set(drivername='postgresql+psycopg2', username=meta['jdbc_user'],
                                        password=meta['jdbc_password'])
        # jdbc_url_obj = jdbc_url_obj.set(host='192.168.132.167', port=5432)
        jdbc_url_obj = jdbc_url_obj.set(query={})  # 否则psycopg2报错ProgrammingError
    return jdbc_url_obj


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
    items = data.get('body').get('items')

    # 将json里的items转为dict类型
    for item in items:
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

    return result
