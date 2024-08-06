from typing import Any, Dict, Optional

from fa_common.models import CamelModel
from fa_common.workflow.models import ArgoWorkflowRun, JobTemplate, LocalWorkflowRun


class RequestCallback(CamelModel):
    workflow: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any] | str] = None
    template: Optional[JobTemplate] = None
    message: Optional[str] = None
    background_task_id: Optional[int] = None


class ResponseWorkflow(CamelModel):
    workflow: Optional[LocalWorkflowRun | ArgoWorkflowRun] = None
    background_task_id: Optional[int] = None
    message: Optional[str] = None
