from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.database import get_db
from app.db.models import Task, User
from app.services.export_service import (
    export_tasks_to_csv,
    export_tasks_to_excel,
    export_tasks_to_pdf,
)

router = APIRouter(
    prefix="/tasks/export",
    tags=["Task Export"],
)


def get_current_user_tasks(db: Session, current_user: User):
    return (
        db.query(Task)
        .filter(Task.owner_id == current_user.id)
        .order_by(Task.id.asc())
        .all()
    )


@router.get("/csv")
def export_tasks_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = get_current_user_tasks(db, current_user)
    file_content = export_tasks_to_csv(tasks)

    return StreamingResponse(
        BytesIO(file_content),
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="tasks.csv"'
        },
    )


@router.get("/excel")
def export_tasks_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = get_current_user_tasks(db, current_user)
    file_content = export_tasks_to_excel(tasks)

    return StreamingResponse(
        BytesIO(file_content),
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": 'attachment; filename="tasks.xlsx"'
        },
    )


@router.get("/pdf")
def export_tasks_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = get_current_user_tasks(db, current_user)
    file_content = export_tasks_to_pdf(tasks)

    return StreamingResponse(
        BytesIO(file_content),
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="tasks.pdf"'
        },
    )