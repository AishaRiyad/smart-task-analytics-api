import asyncio

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task


async def calculate_task_summary(
    db: AsyncSession,
) -> dict:
    # Simulate expensive analytics work for benchmark comparison.
    await asyncio.sleep(0.5)

    statement = select(
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

    result = await db.execute(statement)
    row = result.one()

    return {
        "total_tasks": row.total_tasks or 0,
        "completed_tasks": row.completed_tasks or 0,
        "pending_tasks": row.pending_tasks or 0,
        "average_completion_time": float(
            row.average_completion_time or 0
        ),
    }