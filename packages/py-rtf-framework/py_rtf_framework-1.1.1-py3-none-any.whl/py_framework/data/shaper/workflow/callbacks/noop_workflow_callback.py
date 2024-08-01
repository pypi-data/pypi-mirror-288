"""A no-op implementation of WorkflowCallbacks."""

from py_framework.data.shaper.utils.progress import Progress
from py_framework.data.shaper.verbs.types import TableContainer
from py_framework.data.shaper.workflow.types import ExecutionNode

from .workflow_callbacks import WorkflowCallbacks


class NoopWorkflowCallbacks(WorkflowCallbacks):
    """A no-op implementation of WorkflowCallbacks."""

    def on_workflow_start(self, name: str, instance: object) -> None:
        """Execute this callback when a workflow starts."""

    def on_workflow_end(self, name: str, instance: object) -> None:
        """Execute this callback when a workflow ends."""

    def on_step_start(self, node: ExecutionNode, inputs: dict) -> None:
        """Execute this callback every time a step starts."""

    def on_step_end(self, node: ExecutionNode, result: TableContainer | None) -> None:
        """Execute this callback every time a step ends."""

    def on_step_progress(self, node: ExecutionNode, progress: Progress) -> None:
        """Handle when progress occurs."""

    def on_error(
        self,
        message: str,
        cause: BaseException | None = None,
        stack: str | None = None,
        details: dict | None = None,
    ) -> None:
        """Handle when an error occurs."""

    def on_warning(self, message: str, details: dict | None = None) -> None:
        """Handle when a warning occurs."""

    def on_log(self, message: str, details: dict | None = None) -> None:
        """Handle when a log message occurs."""

    def on_measure(self, name: str, value: float, details: dict | None = None) -> None:
        """Handle when a measurement occurs."""
