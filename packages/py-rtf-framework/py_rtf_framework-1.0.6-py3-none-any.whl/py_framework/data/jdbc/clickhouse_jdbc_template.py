from typing import Any
from clickhouse_driver import Client
import pandas as pd

from py_framework.data.jdbc.base_jdbc_template import BaseJdbcTemplate, DbConfig


class ClickhouseJdbcTemplate(BaseJdbcTemplate):
    """clickhouse的jdbc模板类"""

    def __init__(self, db_config: DbConfig):
        super().__init__(db_config)

    def _get_client(self):
        client = Client(host=self.db_config.host, port=self.db_config.port,
                        user=self.db_config.user, password=self.db_config.password,
                        database=self.db_config.database)
        return client

    def query(self, sql: str, param: dict[str, Any] = None) -> list[dict[str, Any]]:
        client = self._get_client()
        values = client.execute(sql, param)
        return values

    def query_for_df(self, sql: str, param: dict[str, Any] = None) -> pd.DataFrame:
        client = self._get_client()
        value_df = client.query_dataframe(sql, param)
        return value_df

    def insert_df(self, table_name: str, record_df: pd.DataFrame):
        client = self._get_client()
        insert_sql = 'INSERT INTO ' + table_name + ' (' + ','.join(record_df.columns) + ') VALUES'
        client.insert_dataframe(insert_sql, record_df)

    def execute(self, sql: str, param: dict[str, Any] = None):
        client = self._get_client()
        client.execute(sql, param)
