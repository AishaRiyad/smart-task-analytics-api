from datetime import datetime, timedelta, timezone

from sqlalchemy import case, cast, Date, func
from sqlalchemy.orm import Session

from app.db.models import Task


def get_dashboard_data(
    db: Session,
    user_id: int,
    days: int = 7,
) -> dict:
    start_date = datetime.now(timezone.utc) - timedelta(days=days - 1)

    summary = (
        db.query(
            func.count(Task.id).label("total_tasks"),
            func.sum(
                case(
                    (Task.completed.is_(True), 1),
                    else_=0,
                )
            ).label("completed_tasks"),
            func.sum(
                case(
                    (Task.completed.is_(False), 1),
                    else_=0,
                )
            ).label("pending_tasks"),
            func.avg(
                case(
                    (
                        Task.completed.is_(True),
                        Task.completion_time,
                    ),
                    else_=None,
                )
            ).label("average_completion_time"),
        )
        .filter(Task.owner_id == user_id)
        .one()
    )

    total_tasks = summary.total_tasks or 0
    completed_tasks = summary.completed_tasks or 0
    pending_tasks = summary.pending_tasks or 0

    completion_rate = (
        round((completed_tasks / total_tasks) * 100, 2)
        if total_tasks > 0
        else 0.0
    )

    created_rows = (
        db.query(
            cast(Task.created_at, Date).label("date"),
            func.count(Task.id).label("count"),
        )
        .filter(
            Task.owner_id == user_id,
            Task.created_at >= start_date,
        )
        .group_by(cast(Task.created_at, Date))
        .order_by(cast(Task.created_at, Date))
        .all()
    )

    completed_rows = (
        db.query(
            cast(Task.updated_at, Date).label("date"),
            func.count(Task.id).label("count"),
        )
        .filter(
            Task.owner_id == user_id,
            Task.completed.is_(True),
            Task.updated_at.isnot(None),
            Task.updated_at >= start_date,
        )
        .group_by(cast(Task.updated_at, Date))
        .order_by(cast(Task.updated_at, Date))
        .all()
    )

    return {
        "summary": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "average_completion_time": float(
                summary.average_completion_time or 0
            ),
        },
        "completion_rate": completion_rate,
        "tasks_created_by_day": [
            {
                "date": row.date,
                "count": row.count,
            }
            for row in created_rows
        ],
        "tasks_completed_by_day": [
            {
                "date": row.date,
                "count": row.count,
            }
            for row in completed_rows
        ],
    }