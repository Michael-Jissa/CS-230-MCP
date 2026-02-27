from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import logging

# ----------------------------
# basic logging
# ----------------------------
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("todo")

app = FastAPI()


# ----------------------------
# data model
# ----------------------------
class Task(BaseModel):
    client_id: str
    title: str
    notes: str | None = None
    priority: int = 3


# ----------------------------
# in-memory storage
# ----------------------------
tasks = {}


# ----------------------------
# create task
# ----------------------------
@app.post("/tasks")
def create_task(task: Task):

    task_id = str(uuid4())

    new_task = {
        "id": task_id,
        "client_id": task.client_id,
        "title": task.title,
        "notes": task.notes,
        "priority": task.priority,
        "completed": False,
        "created_at": datetime.utcnow()
    }

    tasks[task_id] = new_task

    logger.debug(f"Created task {task_id}")

    return new_task


# ----------------------------
# list tasks for a client
# ----------------------------
@app.get("/tasks")
def list_tasks(client_id: str):

    result = [
        t for t in tasks.values()
        if t["client_id"] == client_id
    ]

    logger.debug(f"Listing tasks for {client_id}")

    return result


# ----------------------------
# get single task
# ----------------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: str):

    if task_id not in tasks:
        raise HTTPException(status_code=404,
                            detail="Task not found")

    return tasks[task_id]


# ----------------------------
# mark complete
# ----------------------------
@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: str):

    if task_id not in tasks:
        raise HTTPException(status_code=404,
                            detail="Task not found")

    tasks[task_id]["completed"] = True

    logger.debug(f"Completed task {task_id}")

    return tasks[task_id]


# ----------------------------
# delete task
# ----------------------------
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):

    if task_id not in tasks:
        raise HTTPException(status_code=404,
                            detail="Task not found")

    del tasks[task_id]

    logger.debug(f"Deleted task {task_id}")

    return {"deleted": task_id}
