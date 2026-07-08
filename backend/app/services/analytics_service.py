import time

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.db.models import Task


def calculate_task_summary(db: Session):
    time.sleep(0.5)

    result = (
        db.query(
            func.count(Task.id).label("total_tasks"),
            func.sum(
                case(
                    (Task.completed == True, 1),
                    else_=0
                )
            ).label("completed_tasks"),
            func.sum(
                case(
                    (Task.completed == False, 1),
                    else_=0
                )
            ).label("pending_tasks"),
            func.avg(
                case(
                    (Task.completed == True, Task.completion_time),
                    else_=None
                )
            ).label("average_completion_time"),
        )
        .one()
    )

    return {
        "total_tasks": result.total_tasks or 0,
        "completed_tasks": result.completed_tasks or 0,
        "pending_tasks": result.pending_tasks or 0,
        "average_completion_time": float(result.average_completion_time or 0)
    }