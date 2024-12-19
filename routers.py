from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from p_models import PUser, PTask, PTaskEdit
from database import is_exists, add_user, login_validation, get_tasks, add_task, delete_task, edit_task
from auth import security


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth 🔐"]
)


@auth_router.get("", summary="Auth page")
async def auth_get():
    return JSONResponse(content="Auth page", status_code=status.HTTP_200_OK)


@auth_router.post(
        "/login",
        summary="Log in",
        responses={
            200: {
                "description": "Access approved",
                "content": {
                    "application/json": {
                        "example": {"msg": "Access approved", "success": True}
                    }
                }
            },
            400: {
                "description": "Incorrect login or password",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "Incorrect login or password", "success": False}}
                    }
                }
            }
        }
)
async def login_post(user: Annotated[str, Depends(PUser)]):
    access = login_validation(credentials=user)
    if access:
        access_token = security.create_access_token(uid=str(access))
        response = JSONResponse(content={"msg": "Access approved", "success": True}, status_code=status.HTTP_200_OK)
        security.set_access_cookies(token=access_token, response=response)
        return response
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Incorrect login or password", "success": False})


@auth_router.post(
        "/registration",
        summary="Registration",
        responses={
            201: {
                "description": "Successfully registered",
                "content": {
                    "application/json": {
                        "example": {"msg": "Successfully registered", "success": True}
                    }
                }
            },
            403: {
                "description": "User with exact name is already exists",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "User with exact name is already exists", "success": False}}
                    }
                }
            }
        },
        status_code=status.HTTP_201_CREATED
)
async def registration_post(user: Annotated[str, Depends(PUser)]):
    if not is_exists(userlogin=user.userlogin):
        add_user(user=user)
        return JSONResponse(content={"msg": "Successfully registered", "success": True}, status_code=status.HTTP_201_CREATED)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg": "User with exact name is already exists", "success": False})


account_router = APIRouter(
    prefix="/account",
    tags=["Account 🐱‍👤"],
    dependencies=[Depends(security.access_token_required)]
)


@account_router.get(
        "",
        summary="Account page",
        responses={
            200: {
                "description": "Shows ID in case of success",
                "content": {
                    "application/json": {
                        "example": {"msg": "Your account page", "uid": "0", "success": True}
                    }
                }
            },
            401: {
                "description": "Access denied",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "Access denied: Authorization required or expired. Please Log In", "success": False}}
                    }
                }
            }
        }
)
async def account_get(token=Depends(security.access_token_required)):
    return JSONResponse(content={"msg": "Your account page", "uid": token.sub, "success": True}, status_code=status.HTTP_200_OK)


@account_router.get(
        "/tasks",
        summary="Get all user tasks",
        responses={
            200: {
                "description": "Will return all tasks if successful",
                "content": {
                    "application/json": {
                        "example": [{"id": 0, "owner_id": 0, "title": "string", "description": "string", "status": "string"}]
                    }
                }
            },
            401: {
                "description": "Access denied",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "Access denied: Authorization required or expired. Please Log In", "success": False}}
                    }
                }
            }
        }
)
async def tasks_get(token=Depends(security.access_token_required)):
    tasks = get_tasks(owner_id=token.sub)
    return JSONResponse(content=tasks, status_code=status.HTTP_200_OK)


@account_router.get(
        "/tasks/{id}",
        summary="Get user task by id",
        responses={
            200: {
                "description": "Will return a specific task by its ID",
                "content": {
                    "application/json": {
                        "example": {"id": 0, "owner_id": 0, "title": "string", "description": "string", "status": "string"}
                    }
                }
            },
            404: {
                "description": "The task with the given id does not exist",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "The task with the given id does not exist", "success": False}}
                    }
                }
            },
            401: {
                "description": "Access denied",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "Access denied: Authorization required or expired. Please Log In", "success": False}}
                    }
                }
            }
        }
)
async def task_by_id_get(id: int, token=Depends(security.access_token_required)):
    tasks = get_tasks(owner_id=token.sub)
    task = {}
    for item in tasks:
        if item["id"] == id:
            task = item
    if task:
        return JSONResponse(content=task, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The task with the given id does not exist", "success": False})


@account_router.post(
        "/tasks",
        summary="Add task to task list",
        responses={
            201: {
                "description": "Create task and add it to task list",
                "content": {
                    "application/json": {
                        "example": {"msg": "Task successfully created", "success": True}
                    }
                }
            },
            401: {
                "description": "Access denied",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "Access denied: Authorization required or expired. Please Log In", "success": False}}
                    }
                }
            }
        },
        status_code=status.HTTP_201_CREATED
)
async def tasks_post(task: Annotated[str, Depends(PTask)], token=Depends(security.access_token_required)):
    add_task(in_owner_id=token.sub, task=task)
    return JSONResponse(content={"msg": "Task successfully created", "success": True}, status_code=status.HTTP_201_CREATED)


@account_router.delete(
        "/task/{id}",
        summary="Delete task by id",
        responses={
            200: {
                "description": "Delete task by id",
                "content": {
                    "application/json": {
                        "example": {"msg": "Task successfully deleted", "success": True}
                    }
                }
            },
            404: {
                "description": "Task not found",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "The task with the given id does not exist", "success": False}}
                    }
                }
            },
            401: {
                "description": "Access denied",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "Access denied: Authorization required or expired. Please Log In", "success": False}}
                    }
                }
            }
        }
)
async def task_by_id_delete(id, token=Depends(security.access_token_required)):
    is_deleted = delete_task(in_owner_id=token.sub, id=id)
    if is_deleted:
        return JSONResponse(content={"msg": "Task successfully deleted", "success": True}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The task with the given id does not exist", "success": False})


@account_router.put(
        "/tasks/{id}",
        summary="Edit task by id",
        responses={
            200: {
                "description": "Successfully edited",
                "content": {
                    "application/json": {
                        "example": {"msg": "Successfully edited", "success": True}
                    }
                }
            },
            404: {
                "description": "Task not found",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "The task with the given id does not exist", "success": False}}
                    }
                }
            },
            401: {
                "description": "Access denied",
                "content": {
                    "application/json": {
                        "example": {"detail": {"msg": "Access denied: Authorization required or expired. Please Log In", "success": False}}
                    }
                }
            }
        }
)
async def task_by_id_put(id, values: Annotated[str, Depends(PTaskEdit)], token=Depends(security.access_token_required)):
    is_edited = edit_task(in_owner_id=token.sub, id=id, values=values)
    if is_edited:
        return JSONResponse(content={"msg": "Successfully edited", "success": True}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The task with the given id does not exist", "success": False})
    