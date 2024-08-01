import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
import requests, json
from typing import Any, List
from py_framework.bootstrap.application_context import get_config_value_by_key
from tqdm import tqdm


@verb(
    name="llm_embedding",
    adapters=[
        inputs(default_input_argname="table"),
        outputs(mode=OutputMode.Table),
    ],
)
def llm_embedding(
        table: pd.DataFrame,
        source_column: str,
        embedding_type: str = 'local_rpc',
        embedding_column: str = 'llm_embedding_value',
        **_kwargs: Any,
) -> pd.DataFrame:
    # 获取需要embedding的列
    source_text_list = table[source_column].values

    # 计算embedding
    embedding_values = None
    if embedding_type == 'local_rpc':
        embedding_values = local_rpc_embedding(source_text_list)
    else:
        raise ValueError('不支持embedding类型：' + embedding_type)

    # 添加新的列
    table[embedding_column] = embedding_values

    return table


def local_rpc_embedding(text_list: List[str]) -> List[List[float]]:
    """执行本地化的embedding"""
    # 获取rpc的host
    # 获取llm的配置
    local_rpc_host = get_config_value_by_key('application.llm.embedding.local_rpc.host')
    if local_rpc_host is None:
        raise ValueError("llm embedding的配置：application.llm.embedding.local_rpc.host 不能为空")

    # 调换回车符号
    text_list = list(map(lambda x: x.replace("\n", " "), text_list))

    embeddings = []
    for text in tqdm(text_list, desc='llm embedding'):
        response = requests.post(url=local_rpc_host + '/api/rag/embedding/text',
                                 data=json.dumps({'text': text}),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            result_json = json.loads(response.content)
            embeddings.append(result_json['data']['vector'])
        else:
            embeddings.append([])

    return embeddings
