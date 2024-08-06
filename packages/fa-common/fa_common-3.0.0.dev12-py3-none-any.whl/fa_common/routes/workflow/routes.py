from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends

from fa_common import get_logger
from fa_common.enums import WorkflowEnums
from fa_common.routes.user.models import UserDB
from fa_common.routes.user.service import get_current_app_user
from fa_common.routes.workflow import service
from fa_common.routes.workflow.types import ResponseWorkflow
from fa_common.workflow.models import JobTemplate

logger = get_logger()

router = APIRouter()


@router.post("/run")
async def run_workflow(
    background_tasks: BackgroundTasks,
    job: JobTemplate,
    current_user: UserDB = Depends(get_current_app_user),
) -> ResponseWorkflow:
    return await service.run_workflow(background_tasks, job)


# @router.post("/run/callback")
# async def run_workflow_callback(data: RequestCallback, api_key: str = Depends(service.verify_api_key)):
#     logger.info(f"Run callback received: {data}")
#     return data


def register_callback_endpoint(router: APIRouter, callback_endpoint):
    """Use this function to implement callback endpoint in the project."""
    router.add_api_route(
        "/run/callback",
        callback_endpoint,
        methods=["POST"],
        # response_model=WorkflowCallbackResponse
    )


@router.get("")
async def get_workflow(
    uid: Optional[str] = None,
    name: Optional[str] = None,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    bucket_name: Optional[str] = None,
    bucket_path: Optional[str] = None,
    output: bool = False,
    file_refs: bool = False,
    namespace: Optional[str] = None,
    current_user: UserDB = Depends(get_current_app_user),
):
    return await service.get_workflow(uid, name, mode, bucket_name, bucket_path, output, file_refs, namespace)


@router.get("/log")
async def get_workflow_log(
    uid: Optional[str] = None,
    name: Optional[str] = None,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    bucket_name: Optional[str] = None,
    bucket_path: Optional[str] = None,
    namespace: Optional[str] = None,
    current_user: UserDB = Depends(get_current_app_user),
):
    return await service.get_workflow_log(uid, name, mode, bucket_name, bucket_path, namespace)


@router.delete("")
async def delete_workflow(
    uid: Optional[str] = None,
    name: Optional[str] = None,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    bucket_name: Optional[str] = None,
    bucket_path: Optional[str] = None,
    namespace: Optional[str] = None,
    current_user: UserDB = Depends(get_current_app_user),
):
    return await service.delete_workflow(uid, name, mode, bucket_name, bucket_path, namespace)
