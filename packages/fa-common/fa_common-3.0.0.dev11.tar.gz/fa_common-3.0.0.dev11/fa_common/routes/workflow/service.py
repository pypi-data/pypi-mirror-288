from typing import List, Optional

import httpx
from fastapi import BackgroundTasks

from fa_common import get_logger
from fa_common.enums import WorkflowEnums
from fa_common.exceptions import BadRequestError, UnImplementedError
from fa_common.models import BucketMeta
from fa_common.routes.modules.models import ModuleDocument
from fa_common.workflow.enums import JobSubmitMode
from fa_common.workflow.local_client import LocalWorkflowClient
from fa_common.workflow.models import JobTemplate, LocalWorkflowRun, WorkflowCallBack, WorkflowId
from fa_common.workflow.utils import get_workflow_client

from .types import RequestCallback, ResponseWorkflow

logger = get_logger()


async def run_workflow(background_tasks: BackgroundTasks, job: JobTemplate):
    module_name = job.module.name
    module_ver = job.module.version

    job.module = await ModuleDocument.get_version(module_name, module_ver)

    if job.submit_mode == JobSubmitMode.ISOLATED:
        workflow_client = get_workflow_client(mode=WorkflowEnums.Type.ARGO)
        res = await workflow_client.run_job(job_base=job)
        return ResponseWorkflow(workflow=res, message=f"Argo workflow with name: {res.metadata.name} is submitted!")
    elif job.submit_mode in (JobSubmitMode.LOCAL, JobSubmitMode.ISOLATED_LOCAL):
        workflow_client = get_workflow_client(mode=WorkflowEnums.Type.LOCAL)
        background_tasks.add_task(run_local_job_in_background, job, workflow_client)
        return ResponseWorkflow(
            workflow=LocalWorkflowRun(template=job),
            message="Local job is scheduled to run in the background",
            background_task_id=id(job),
        )
    else:
        raise BadRequestError(f"Unknown submit mode: {job.submit_mode}")


async def get_workflow(
    uid: Optional[str] = None,
    name: Optional[str] = None,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    bucket_name: Optional[str] = None,
    bucket_path: Optional[str] = None,
    output: bool = False,
    file_refs: bool = False,
    namespace: Optional[str] = None,
):
    if mode == WorkflowEnums.Type.LOCAL:
        raise UnImplementedError("Get workflow is not implemented for local runs.")

    workflow_client = get_workflow_client(mode=mode)
    return await workflow_client.get_workflow(
        bucket_meta=BucketMeta(name=bucket_name, base_path=bucket_path),
        workflow_id=WorkflowId(name=name, uid=uid),
        output=output,
        file_refs=file_refs,
        namespace=namespace,
    )


async def get_workflow_log(
    uid: Optional[str] = None,
    name: Optional[str] = None,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    bucket_name: Optional[str] = None,
    bucket_path: Optional[str] = None,
    namespace: Optional[str] = None,
):
    if mode == WorkflowEnums.Type.LOCAL:
        raise UnImplementedError("Getting workflow logs is not implemented for local runs.")

    workflow_client = get_workflow_client(mode=mode)
    return await workflow_client.get_workflow_log(
        workflow_id=WorkflowId(name=name, uid=uid),
        bucket_meta=BucketMeta(name=bucket_name, base_path=bucket_path),
        namespace=namespace,
    )


async def delete_workflow(
    uid: Optional[str] = None,
    name: Optional[str] = None,
    mode: WorkflowEnums.Type = WorkflowEnums.Type.ARGO,
    bucket_name: Optional[str] = None,
    bucket_path: Optional[str] = None,
    namespace: Optional[str] = None,
):
    if mode == WorkflowEnums.Type.LOCAL:
        raise UnImplementedError("Deleting a workflow is not implemented for local runs.")

    workflow_client = get_workflow_client(mode=mode)
    return await workflow_client.delete_workflow(
        workflow_id=WorkflowId(name=name, uid=uid),
        bucket_meta=BucketMeta(name=bucket_name, base_path=bucket_path),
        namespace=namespace,
        force_data_delete=True,
    )


async def callback(items: List[WorkflowCallBack], result: LocalWorkflowRun, task_id: int):
    for item in items:
        headers = {"x-api-key": item.api_key} if item.api_key else {}
        data = RequestCallback(
            workflow=result.model_dump(),
            metadata=item.metadata,
            message="Local Job completed!",
            background_task_id=task_id,
        )
        async with httpx.AsyncClient() as client:
            await client.post(item.url, json=data.model_dump(), headers=headers)


async def run_local_job_in_background(job: JobTemplate, workflow_client: LocalWorkflowClient):
    logger.info(f"Starting background job for job ID: {id(job)}")
    try:
        result = await workflow_client.run_job(job_base=job)
        logger.info(f"Job completed with result: {result}")
        if job.callbacks:
            await callback(items=job.callbacks, result=result, task_id=id(job))
            logger.info("Callback has been executed successfully.")
    except Exception as e:
        logger.error(f"Error occurred: {e!s}")
        raise


# async def verify_api_key(x_api_key: str = Header(...)):
#     if x_api_key != wb_settings.MASTER_API_KEY:
#         raise HTTPException(status_code=403, detail="Invalid API Key")
#     return x_api_key
