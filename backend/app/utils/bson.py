from typing import Any, Dict, List


def task_serializer(task: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description", ""),
        "completed": task.get("completed", False),
        "created_at": task["created_at"],
        "updated_at": task["updated_at"],
    }


def task_list_serializer(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [task_serializer(task) for task in tasks]