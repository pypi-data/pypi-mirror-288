import re
from requests.auth import HTTPBasicAuth
from sqlalchemy import make_url, URL, TextClause, Column

from k2magic.dialect import k2a_requests


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