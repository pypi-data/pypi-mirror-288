from typing import Any
from tqdm import tqdm
import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
from py_framework.bootstrap.application_context import get_config_dict_by_prefix
from langchain_elasticsearch.vectorstores import ElasticsearchStore


@verb(
    name="vector_store_es",
    adapters=[
        inputs(default_input_argname="table"),
        outputs(mode=OutputMode.Table),
    ],
)
def vector_store_es(
        table: pd.DataFrame,
        index_name: str,
        index_text_column: str,
        index_vector_column: str,
        index_config_prefix: str,
        index_id_column: str = None,
        store_step_size: int = 200,
        **_kwargs: Any,
) -> pd.DataFrame:
    # 获取es配置
    es_config_props = get_config_dict_by_prefix(index_config_prefix)
    print('es配置', es_config_props, len(table))

    # 设置es存储
    es_store = ElasticsearchStore(
        index_name=index_name,
        vector_query_field=index_vector_column,
        query_field=index_text_column,
        **es_config_props
    )

    # 分片存储
    max_size = len(table)
    index_ids = []
    with tqdm(total=max_size, desc="vector store es") as pbar:
        for start_index in range(0, max_size, store_step_size):
            end_index = max_size if start_index + store_step_size >= max_size else start_index + store_step_size
            sub_table = table[start_index:end_index]
            # 构建索引和元数据
            text_embeddings = sub_table[[index_text_column, index_vector_column]].values
            text_metadata = sub_table.drop([index_text_column, index_vector_column], axis=1).to_dict('records')
            # 如果索引列存在，则直接使用其中的值，否则生成索引后更新索引值
            text_ids = None
            if index_id_column is not None and index_id_column in table.columns:
                text_ids = sub_table[index_id_column].values.tolist()
            # 执行数据保存
            sub_index_ids = es_store.add_embeddings(text_embeddings=text_embeddings,
                                                    metadatas=text_metadata,
                                                    ids=text_ids,
                                                    create_index_if_not_exists=False)
            # 保存索引和更新进度
            index_ids.extend(sub_index_ids)
            pbar.update(len(sub_table))

    # 设置索引列
    if index_id_column is not None:
        table[index_id_column] = index_ids

    return table
