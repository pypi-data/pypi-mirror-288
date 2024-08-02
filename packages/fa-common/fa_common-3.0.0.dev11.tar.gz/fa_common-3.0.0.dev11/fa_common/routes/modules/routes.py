from typing import Optional

from fastapi import APIRouter, Depends, Security

from fa_common.models import Message
from fa_common.routes.modules.types import Module, ModuleVersion
from fa_common.routes.user.models import UserDB
from fa_common.routes.user.service import get_current_app_user

from .models import ModuleDocument

router = APIRouter()


@router.get("")
async def get_all_module_names():
    """Gets the names of all available modules."""
    return await ModuleDocument.get_all()
    # return await ModuleService.get_module_list()


@router.get("/{name}")
async def get_specific_module(name: str):
    """Given the name of the module, it returns its full information."""
    return await ModuleDocument.get(name)


@router.get("/{name}/versions")
async def get_versions_of_a_module(name: str):
    """
    Given the name of the module, it returns back the names of
    all available versions for this module.
    """
    return await ModuleDocument.get_versions(name)


@router.get("/{name}/{version}")
async def get_specific_version_of_a_module(name: str, version: str):
    """
    Given the name of a Module and a specific version of it,
    it will return full information of the version. Note that
    it will fuse the version data with the basic version data
    (priority given to the version data).
    """
    return await ModuleDocument.get_version(name, version)


@router.post("")
async def create_new_module(new_module: Module, current_user: UserDB = Security(get_current_app_user, scopes=["admin"])):
    """Creates a new module."""
    return await ModuleDocument.insert_new(new_module)


@router.delete("")
async def delete_module(name: str, current_user: UserDB = Depends(get_current_app_user)) -> Message:
    """Deletes an existing module."""
    return await ModuleDocument.delete_module(name)


@router.put("/overwrite/{name}")
async def overwrite_module(name: str, update_module: Module, current_user: UserDB = Security(get_current_app_user, scopes=["admin"])):
    """Completely overwrites an existing module."""
    return await ModuleDocument.overwrite(curr_name=name, module=update_module)


@router.put("/{name}")
async def update_name_description_module(
    name: str,
    new_name: Optional[str] = None,
    new_description: Optional[str] = None,
    current_user: UserDB = Security(get_current_app_user, scopes=["admin"]),
):
    """Updates only name and description of a module."""
    return await ModuleDocument.update_meta(curr_name=name, new_name=new_name, description=new_description)


@router.put("/{name}/base-version")
async def update_base_version(name: str, version: ModuleVersion, current_user: UserDB = Security(get_current_app_user, scopes=["admin"])):
    """Updates the base version data of the module."""
    return await ModuleDocument.update_base_version(name, version)


@router.put("/{name}/new")
async def add_new_version(name: str, version: ModuleVersion, current_user: UserDB = Security(get_current_app_user, scopes=["admin"])):
    """Adds a new version to the module."""
    return await ModuleDocument.add_new_version(name, version)


@router.put("/{name}/{version_name}")
async def update_module_version(
    name: str, version_name: str, version: ModuleVersion, current_user: UserDB = Security(get_current_app_user, scopes=["admin"])
):
    """Updates a specific version of a module."""
    return await ModuleDocument.update_version(name, version_name, version)


@router.put("/{name}/{version_name}/delete")
async def delete_module_version(name: str, version_name: str, current_user: UserDB = Security(get_current_app_user, scopes=["admin"])):
    """Deletes an existing version of a module."""
    return await ModuleDocument.delete_version(name, version_name)
