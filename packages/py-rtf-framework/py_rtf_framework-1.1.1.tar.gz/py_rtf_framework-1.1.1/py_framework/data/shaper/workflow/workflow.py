#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#
"""The data processing workflow definition."""

import inspect
import json
import time
import traceback
from collections import OrderedDict, defaultdict
from collections.abc import Callable, Iterable
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import Any, Generic, TypeVar, cast
from uuid import uuid4
import asyncio
import pandas as pd
from jsonschema import validate as validate_schema

from py_framework.data.shaper.constants import DEFAULT_INPUT_NAME
from py_framework.data.shaper.errors import (
    NodeNotVisitedError,
    WorkflowInvalidInputError,
    WorkflowMissingInputError,
    WorkflowOutputNotReadyError,
    WorkflowVerbNotFoundError,
)
from py_framework.data.shaper.tables import InMemoryTableStore, TableStore
from py_framework.data.shaper.utils.progress import Progress
from py_framework.data.shaper.verbs import Table, VerbDetails, VerbInput, VerbManager, VerbResult
from py_framework.data.shaper.verbs.types import TableContainer

from .callbacks import (
    MemoryProfilingWorkflowCallbacks,
    WorkflowCallbacks,
    WorkflowCallbacksManager,
)
from .delegating_verb_callbacks import DelegatingVerbCallbacks
from .types import (
    ExecutionNode,
    MemoryProfile,
    VerbTiming,
    WorkflowInput,
    WorkflowRunResult,
)

log = getLogger(__name__)

# TODO(Chris): this won't work for a published package
SCHEMA_FILE = "../../schema/workflow.json"

Context = TypeVar("Context")


class PandasDtypeBackend(str, Enum):
    """Pandas dtype backend."""

    NUMPY_NULLABLE = "numpy_nullable"
    PYARROW = "pyarrow"


class Workflow(Generic[Context]):
    """A data processing graph."""

    _table_store: TableStore
    _schema: dict
    _graph: dict[str, ExecutionNode]
    _dependency_graph: dict[str, set[str]]
    _last_step_id: str
    _dependencies: set[str]
    _memory_profile: bool | None
    _validate_schema: bool | None
    _schema_path: str | None
    """Externals that this workflow depends on"""

    def dispose(self) -> None:
        """Dispose of the workflow and its resources."""
        self._table_store.dispose()
        self._graph.clear()
        self._dependency_graph.clear()
        self._schema.clear()

    def __init__(
            self,
            schema: dict,
            input_tables: dict[str, pd.DataFrame] | None = None,
            schema_path: str | None = None,
            verbs: dict[str, Callable] | None = None,
            validate: bool | None = False,
            memory_profile: bool | None = False,
            pandas_dtype_backend: PandasDtypeBackend = PandasDtypeBackend.NUMPY_NULLABLE,
            table_store: TableStore | None = None,
    ):
        """Create an execution graph from the Dict provided in workflow.

        :param schema: the Dict object that contains the workflow
        :type schema: Dict
        :param schema_path: Optional Workflow schema path, if provided input
                           tables will be loaded relative to that path, defaults to
                           a known JSON schema path.
        :type schema_path: str, optional
        :param validate: Optional value, if true perform JSON-schema validation.
                         Defaults to False.
        :type validate: bool, optional
        """
        # schema的基本信息，可以通过指定配置文件配置 或 直接使用dict字典配置
        self._schema_path = schema_path = schema_path or SCHEMA_FILE
        self._validate_schema = validate
        self._schema = schema

        self._memory_profile = memory_profile
        self._dependencies = self._compute_dependencies()
        self._dependency_graph = defaultdict(set)
        self._graph = OrderedDict()
        self._table_store = (
            table_store if table_store is not None else InMemoryTableStore()
        )

        # Perform JSON-schema validation
        # TODO(Chris): the current schema definition does not work in Python
        if validate and schema_path is not None:
            with Path(schema_path).open(encoding='utf-8') as schema_file:
                schema_json = json.load(schema_file)
                validate_schema(schema, schema_json)

        # 构建输入参数和结果的依赖关系
        if input_tables is not None:
            for input_name, table in input_tables.items():
                self.add_table(
                    input_name,
                    table.convert_dtypes(dtype_backend=pandas_dtype_backend.value),
                )
        else:
            print('workflow:使用空DataFrame作为初始输入')
            self.add_table(
                DEFAULT_INPUT_NAME,
                pd.DataFrame(),
            )

        # 注册verb
        if verbs is not None:
            VerbManager.get().register_verbs(verbs, override_existing=True)

        # 创建执行图
        previous_step_id = None
        for step in schema["steps"]:
            # step是否禁用
            step_enabled = step['enable'] if 'enable' in step else True
            if step_enabled is False:
                continue
            step_has_defined_id = "id" in step
            step_id = step["id"] if step_has_defined_id else str(uuid4())
            # 默认获取上一节点的输出作为本节点的输入
            step_input = (step.get("input", previous_step_id)) or DEFAULT_INPUT_NAME
            verb = Workflow.__get_verb(step["verb"])
            # 创建图执行节点
            step = ExecutionNode(
                node_id=step_id,
                node_input=step_input,
                verb=verb,
                has_explicit_id=step_has_defined_id,
                args=step.get("args", {}),
            )
            self._graph[step_id] = step
            # 存储依赖input的节点
            for input_name in Workflow.__list_inputs(step_input):
                self._dependency_graph[input_name].add(step_id)
            previous_step_id = step.node_id

        self._last_step_id = cast(str, previous_step_id)

    @property
    def name(self) -> str:
        """Get the name of the workflow, inferred from the schema json input."""
        return self._schema.get("name", "Workflow")

    @property
    def dependencies(self) -> set[str]:
        """Get the dependencies of the workflow."""
        return self._dependencies

    def _compute_dependencies(self) -> set[str]:
        deps: set[str] = set()
        known: set[str] = set()
        steps: list[dict] = self._schema["steps"]

        if len(steps) > 0:
            if "input" not in steps[0]:
                deps.add(DEFAULT_INPUT_NAME)

            for step in self._schema["steps"]:
                if "id" in step:
                    known.add(step["id"])
                # 添加输入到依赖中
                if "input" in step:
                    step_inputs = Workflow.__list_inputs(step["input"])
                    deps.update(step_inputs)

        # Remove known steps from dep list
        return deps.difference(known)

    @staticmethod
    def __list_inputs(input: str | dict | None) -> list[str]:
        if input is None:
            return []

        inputs: list[str] = []

        def resolve(value: str | dict) -> str:
            """解析如果为是字符串，直接返回，否则解析step属性"""
            if isinstance(value, str):
                return value
            return value["step"]

        # 如果input元素为字符串，则直接加入；否则解析列表内容项后加入
        if isinstance(input, str):
            inputs.append(input)
        else:
            for value in input.values():
                if isinstance(value, list):
                    for dep in value:
                        inputs.append(resolve(dep))  # noqa: PERF401
                else:
                    inputs.append(resolve(value))

        return inputs

    @staticmethod
    def __get_verb(verb: str) -> VerbDetails:
        """Get the verb function from the name."""
        verbs_manager = VerbManager.get()
        result = verbs_manager.get_verb(verb)
        if result is None:
            raise WorkflowVerbNotFoundError(verb)
        return result

    def _resolve_run_context(
            self,
            exec_node: ExecutionNode,
            context: Context | None,
            workflow_callbacks: WorkflowCallbacks,
    ) -> dict:
        """Injects the run context into the workflow steps."""
        callbacks = DelegatingVerbCallbacks(exec_node, workflow_callbacks)
        run_ctx: dict = {}

        # Pass in individual context items
        if context is not None:
            for context_key in dir(context):
                run_ctx[context_key] = getattr(context, context_key)

        run_ctx["context"] = context
        run_ctx["callbacks"] = callbacks
        run_ctx["workflow_instance"] = self
        return run_ctx

    def _get_missing_inputs(self, node_key: str, visited: set[str]) -> list[str]:
        """节点输入依赖的节点没有被访问 并且 也没有生成结果列表，则返回需要执行的节点"""
        node = self._graph[node_key]
        return [
            input
            for input in Workflow.__list_inputs(node.node_input)
            if input not in visited and input not in self._table_store.list()
        ]

    def _resolve_inputs(
            self,
            verb: VerbDetails,
            inputs: str | dict[str, WorkflowInput | list[WorkflowInput]],
    ) -> VerbInput:
        def input_table(name: str, output: str | None = None) -> TableContainer:
            graph_node = self._graph.get(name)
            step_table_is_safe_to_mutate = (
                    graph_node is not None and not graph_node.has_explicit_id
            )

            if output is not None:
                name = f"{name}.{output}"

            # if the node has an explicit id or if the verb is mutation-free, skip the copy
            #
            # NOTE: if this is an input table, we can probably use the original table if this is the only reference in the workflow ... TODO
            #
            use_original_table = (
                    verb.treats_input_tables_as_immutable or step_table_is_safe_to_mutate
            )

            if name not in self._table_store.list():
                raise WorkflowMissingInputError(name)

            # 使用table_store中已有的名称
            table_container = self._table_store.get(name)

            if use_original_table:
                return table_container

            table = table_container.table.copy()
            return TableContainer(table=table)

        if isinstance(inputs, str):
            return VerbInput(source=input_table(inputs))

        input_mapping: dict[str, TableContainer | list[TableContainer]] = {}
        for key, value in inputs.items():
            if isinstance(value, str):
                input_mapping[key] = input_table(value)
            elif isinstance(value, dict):
                value = cast(dict, value)
                input_mapping[key] = input_table(value["step"], value["table"])
            elif isinstance(value, list):

                def resolve(t: WorkflowInput) -> TableContainer:
                    if isinstance(t, str):
                        return input_table(t)
                    if isinstance(t, dict):
                        return input_table(t["step"], t["table"])
                    raise WorkflowInvalidInputError(str(type(t)))

                input_mapping[key] = [resolve(t) for t in value]
            else:
                raise WorkflowInvalidInputError(str(type(value)))

        source_tbl = cast(TableContainer, input_mapping.pop("source", None))
        other_tbl = cast(TableContainer, input_mapping.pop("other", None))
        others_tbl = cast(list[TableContainer], input_mapping.pop("others", None))
        input_mapping = cast(dict, input_mapping)
        if other_tbl is not None:
            input_mapping["other"] = other_tbl
        # 解析输入，包括source、others和其它命名后的输入
        return VerbInput(
            source=source_tbl,
            others=others_tbl,
            named=cast(dict[str, TableContainer], input_mapping),
        )

    def add_table(self, id: str, table: pd.DataFrame) -> None:
        """Add a dataframe to the graph with a given id."""
        self._table_store.add(id, TableContainer(table=table), tag="input")

    def output(self, id: str | None = None) -> Table:
        """Get a dataframe from the graph by id."""
        if id is None:
            id = self._last_step_id

        container: TableContainer | None = self._table_store.get(id)
        if container is None:
            raise WorkflowOutputNotReadyError(self.name, id)

        return container.table

    def run_until_complete(self, context: Context | None = None,
                           callbacks: WorkflowCallbacks | None = None) -> pd.DataFrame:
        asyncio.run(self.run(context, callbacks))
        return self.output()

    async def run(
            self,
            context: Context | None = None,
            callbacks: WorkflowCallbacks | None = None,
    ) -> WorkflowRunResult:
        """Run the execution graph."""
        visited: set[str] = set()
        nodes: list[str] = []

        def enqueue_available_nodes(possible_nodes: Iterable[str]) -> None:
            # 节点没有被访问并且无结果
            new_nodes = [
                n
                for n in possible_nodes
                if len(self._get_missing_inputs(n, visited)) == 0
            ]
            nodes.extend(new_nodes)

        def assert_all_visited() -> None:
            for node_id in self._graph:
                node = self._graph.get(node_id)

                if node_id not in visited:
                    missing_inputs = self._get_missing_inputs(node_id, visited)
                    node_id = node.node_id if node is not None else node_id
                    verb_name = node.verb.name if node is not None else "unknown"
                    raise NodeNotVisitedError(node_id, verb_name, missing_inputs)

        # Use the ensuring variant to guarantee that all protocol methods are available
        callbacks, profiler = self._get_workflow_callbacks(callbacks)
        callbacks.on_workflow_start(self.name, self)
        enqueue_available_nodes(self._graph.keys())

        verb_idx = 0
        verb_timings: list[VerbTiming] = []

        if len(nodes) < 1:
            raise ValueError('无可运行的节点，请检查输入参数配置')

        while len(nodes) > 0:
            current_id = nodes.pop(0)
            node = self._graph[current_id]
            # 执行verb节点内容
            timing = await self._execute_verb(node, context, callbacks)
            verb_timings.append(
                VerbTiming(
                    id=node.node_id,
                    verb=node.verb.name,
                    index=verb_idx,
                    timing=timing,
                )
            )

            visited.add(current_id)
            # 释放依赖当前节点的其它依赖节点
            enqueue_available_nodes(self._dependency_graph[current_id])
            verb_idx += 1

        assert_all_visited()
        callbacks.on_workflow_end(self.name, self)

        return WorkflowRunResult(
            verb_timings=verb_timings, memory_profile=_get_memory_profile(profiler)
        )

    async def _execute_verb(
            self,
            node: ExecutionNode,
            context: Context | None,
            callbacks: WorkflowCallbacks,
    ) -> float:
        start_verb_time = time.time()

        try:
            # 构建输入参数和运行时上下文
            verb_input = self._resolve_inputs(node.verb, node.node_input)
            verb_context = self._resolve_run_context(node, context, callbacks)
            # 构建完整的输入参数：将输入、上下文以及参数都作为函数参数一部分
            verb_args = {
                "input": verb_input,
                **verb_context,
                **node.args,
            }
            callbacks.on_step_start(node, verb_args)
            callbacks.on_step_progress(node, Progress(percent=0))
            log.info("executing verb %s", node.verb.name)
            result = node.verb.func(**verb_args)

            # Unroll the result if it's a coroutine
            # (we need to do this before calling on_step_end)
            if inspect.iscoroutine(result):
                result = await result
        except Exception as e:
            message = f'Error executing verb "{node.verb.name}" in {self.name}: {e}'
            log.exception(message)
            callbacks.on_error(message, e, traceback.format_exc())
            raise
        else:
            # 如果执行过程没有异常，则执行else中内容
            if isinstance(result, TableContainer):
                self._table_store.add(node.node_id, result, tag="output")
            elif isinstance(result, VerbResult):
                self._table_store.add(node.node_id, result.output, tag="output")
                for name, table in result.named_outputs.items():
                    self._table_store.add(f"{node.node_id}.{name}", table, tag="output")
        finally:
            callbacks.on_step_progress(node, Progress(percent=1))
            callbacks.on_step_end(node, None)

        # Return verb timing
        return time.time() - start_verb_time

    def _get_workflow_callbacks(
            self, callbacks: WorkflowCallbacks | None
    ) -> tuple[WorkflowCallbacks, MemoryProfilingWorkflowCallbacks | None]:
        profiler: MemoryProfilingWorkflowCallbacks | None = None
        callback_handler = WorkflowCallbacksManager()

        if callbacks is not None:
            callback_handler.register(callbacks)

        if self._memory_profile:
            profiler = MemoryProfilingWorkflowCallbacks()
            callback_handler.register(profiler)

        return (callback_handler, profiler)

    def export(self) -> dict:
        """Export the graph into a workflow JSON object."""
        return {
            "input": [table for table in self._table_store.list(tag="input")],
            "steps": [
                {
                    "id": step.node_id,
                    "verb": step.verb.name,
                    "input": step.node_input,
                    "args": step.args,
                }
                for step in self._graph.values()
            ],
        }

    def derive(
            self, schema: dict[str, Any], input_tables: dict[str, pd.DataFrame]
    ) -> "Workflow":
        """Derive a new workflow from the current one."""
        # Verbs are already registered, and we don't need to validate the schema again
        return Workflow(
            schema,
            input_tables=input_tables,
            validate=self._validate_schema,
            schema_path=self._schema_path,
        )


def _get_memory_profile(
        profile: MemoryProfilingWorkflowCallbacks | None,
) -> MemoryProfile | None:
    if profile is not None:
        return MemoryProfile(
            snapshot_stats=profile.get_snapshot_stats(),
            peak_stats=profile.get_peak_stats(),
            time_stats=profile.get_time_stats(),
            detailed_view=profile.get_detailed_view(),
        )

    return None
