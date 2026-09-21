from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from . import repository


class TaskInput(BaseModel):
    title: str = Field(..., min_length=1)
    done: bool = False


class Task(TaskInput):
    id: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository.initialize_database()
    yield


app = FastAPI(
    title="Flyrank Task API",
    lifespan=lifespan,
)


@app.exception_handler(404)
async def not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": "Task not found"},
    )


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return repository.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = repository.get_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    return task


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskInput):
    title = task.title.strip()

    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"},
        )

    return repository.create_task(title, task.done)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskInput):
    title = task.title.strip()

    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"},
        )

    updated_task = repository.update_task(
        task_id,
        title,
        task.done,
    )

    if updated_task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int):
    deleted = repository.delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    return None