import re

import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, text, Column, Integer, Float, String, select, make_url, modifier, \
    ColumnElement, and_, literal
from sqlalchemy.dialects import registry
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import expression, visitors
from sqlalchemy.sql.visitors import replacement_traverse, cloned_traverse, traverse

from k2magic.dataframe_db import DataFrameDB
from k2magic.dataframe_db_exception import DataFrameDBException
from k2magic.dialect.k2a_repo_wrapper import disclose
from k2magic.dialect.k2a_repo_wrapper import modify_timestamp, print_element


class K2DataFrameDB(DataFrameDB):

    def __init__(self, db_url, schema=None):
        db_url_obj = make_url(db_url)
        self.behind_repo = db_url_obj.drivername == 'k2assets+repo' or db_url_obj.drivername == 'repo'
        if self.behind_repo:
            db_url_obj = disclose(db_url_obj)

        super().__init__(db_url_obj,schema)


    def select(self, table_name: str, columns: list = None, condition: str = None,
               limit: int = None, order_by: list = None):
        """
        查询指定表中的数据，并返回 DataFrame。

        Parameters:
        -----------
        table_name : str
            关系表名。
        columns : list, optional
            要查询的列的字符串列表。如果未指定，将查询所有列。
        condition : str, optional
            查询条件，字符串格式，例如 'col1 > 10'。
        limit : int, optional
            查询结果的最大行数
        order_by : list, optional
            排序条件，例如 'k_device DESC'

        Returns:
        --------
        pandas.DataFrame
            查询结果。

        Raises:
        -------
        DataFrameDBException
            在操作数据库时发生错误。
        """
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
                if condition:
                    query = query.where(text(condition))

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
                                                          if col=='k_ts' else table.c[col] for col in columns))
                print(str(query))
                result = conn.execute(query)
                return pd.DataFrame(result.fetchall(), columns=result.keys())
        except SQLAlchemyError as e:
            raise DataFrameDBException(
                "Failed to query records due to a database error.",
                original_exception=e
            )

