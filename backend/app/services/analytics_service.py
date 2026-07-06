import time

from sqlalchemy.orm import Session

from app.db.models import Task


def calculate_task_summary(db: Session):
    # Simulate expensive analytics calculation for performance benchmarking.
    # To helps us compare between database calculation & Redis cache.
    time.sleep(0.5)

    total_tasks = db.query(Task).count()

    completed_tasks = db.query(Task).filter(Task.completed == True).count()

    pending_tasks = db.query(Task).filter(Task.completed == False).count()

    completed_with_time = (
        db.query(Task)
        .filter(Task.completed == True, Task.completion_time.isnot(None))
        .all()
    )

    if completed_with_time:
        average_completion_time = sum(
            task.completion_time for task in completed_with_time
        ) / len(completed_with_time)
    else:
        average_completion_time = 0

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "average_completion_time": average_completion_time
    }