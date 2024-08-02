import re
from requests.auth import HTTPBasicAuth
from sqlalchemy import make_url, URL, TextClause, Column

from k2magic.dialect import k2a_requests


def disclose(repo_db_url: URL) -> URL:
    """
    将 repo:// 开头的 conn_url 转换为底层数据库的 conn_url
    实现方式是先从repo获取元信息，然后让SQLAlchemy直接访问底层数据
    :param repo_db_url: 使用URL类型避免密码明文泄露
    :return:
    """
    meta = _fetch_repo_meta(repo_db_url)
    storage = meta['storage']
    if storage == 'postgresql':
        jdbc_url = meta['jdbc_url']
        if jdbc_url.startswith('jdbc:'):
            jdbc_url = jdbc_url[5:]
        jdbc_url_obj = make_url(jdbc_url)
        jdbc_url_obj = jdbc_url_obj.set(drivername='postgresql+psycopg2', username=meta['jdbc_user'],
                                        password=meta['jdbc_password'])
        jdbc_url_obj = jdbc_url_obj.set(host='192.168.132.167', port=5432)
        jdbc_url_obj = jdbc_url_obj.set(query={})  # 否则psycopg2报错ProgrammingError
    return jdbc_url_obj


def _fetch_repo_meta(url: URL) -> dict:
    result = {}

    # 获取repo的storage类型，一并放在返回的dict里（key为"storage")
    api_url = f"https://{url.host}:{url.port}/api/v2/repos/{url.database}"
    auth = HTTPBasicAuth(url.username, url.password)
    data = k2a_requests.get(api_url, auth=auth)
    result['storage'] = data.get('body').get('storageInfo').get('name')

    # 获取repo的meta-settings
    api_url = f"https://{url.host}:{url.port}/api/v2/repos/{url.database}/meta-settings"
    data = k2a_requests.get(api_url, auth=auth)
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
            env_url = f"https://{url.host}:{url.port}/api/env/{param_name}"
            response2 = k2a_requests.get(env_url, auth=auth)
            return response2.get('body').get('values').get(param_name)

        pref_value = re.sub(pattern, replace, pref_value)

        result[name] = pref_value

    # {
    #   'storage': 'postgresql',
    # 	'jdbc_url': 'jdbc:postgresql://k2a-postgresql:5432/repos?currentSchema=public',
    # 	'jdbc_user': 'k2data',
    # 	'jdbc_password': 'K2data1234',
    # 	'jdbc_conn_pool_size': '20',
    # 	'batch_insert_size': '500',
    # 	'batch_insert_pool_size': '1',
    # 	'key_varchar_len': '256',
    # 	'varchar_len': '1024',
    # 	'completeness_stats_cache': 'true',
    # 	'latest_data_cache': 'true'
    # }
    return result




def modify_case(element):
    # # 检查元素是否为ColumnElement类型
    if isinstance(element, Column):
        element.name = element.name.lower()
        element.key = element.key.lower()
    if isinstance(element, TextClause):
        element.text = element.text.lower()

def modify_timestamp(element):
    # if isinstance(element, Column):
    #     if element.key == 'k_ts':
    #         element.key = 'k_ts/1000000'
    #         element.name = 'k_ts/1000000'
    # if isinstance(element, BinaryExpression):
    #     if element.left.key == 'k_ts':
    #         # element.right = element.right * 1000000
    #         print(element.right)
    # 处理where语句里的k_ts过滤条件
    # 对于TextClause类型的过滤条件，只能用正则来识别毫秒时间戳（12~13位数字），添加6个零以后变成纳秒单位
    if isinstance(element, TextClause):
        def add_zeros(match):
            number = match.group(0)
            return number + '000000'
        pattern = r'\b\d{12,13}\b'
        element.text = re.sub(pattern, add_zeros, element.text)

def print_element(element):
    print(element)