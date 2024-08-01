from typing import Any

import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
from py_framework.data.jdbc.jdbc_template import DbType, jdbc_template_from_config
from py_framework.data.jdbc.base_jdbc_template import BaseJdbcTemplate


@verb(
    name="jdbc_query",
    adapters=[
        outputs(mode=OutputMode.Table),
    ],
)
def jdbc_query(
        query_sql: str,
        query_param: dict = None,
        db_config_prefix: str = None,
        **_kwargs: Any,
) -> pd.DataFrame:
    jdbc_template: BaseJdbcTemplate = jdbc_template_from_config(config_prefix=db_config_prefix)

    query_result_df = jdbc_template.query_for_df(query_sql, query_param)

    return query_result_df
