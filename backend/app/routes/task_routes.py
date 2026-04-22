from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.core.database import get_database
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate
from app.utils.bson import task_list_serializer, task_serializer

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    db = get_database()
    task_data = task.model_dump()

    now = datetime.now(timezone.utc)

    task_data["created_at"] = now
    task_data["updated_at"] = now

    result = db.tasks.insert_one(task_data)

    created_task = db.tasks.find_one({"_id": result.inserted_id})

    return task_serializer(created_task)


@router.get("/", response_model=list[TaskResponse])
async def get_tasks():
    db = get_database()
    tasks = list(db.tasks.find().sort("created_at", -1))
    return task_list_serializer(tasks)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    db = get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = db.tasks.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task_serializer(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate):
    db = get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    existing_task = db.tasks.find_one({"_id": ObjectId(task_id)})

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = {
        key: value
        for key, value in task_update.model_dump().items()
        if value is not None
    }

    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc)

        db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )

    updated_task = db.tasks.find_one({"_id": ObjectId(task_id)})
    return task_serializer(updated_task)


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: str):
    db = get_database()

    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    result = db.tasks.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}