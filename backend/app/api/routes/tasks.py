from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.database import get_db
from app.db.models import Task, User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.cache_service import delete_cache
from app.services.email_service import (
    send_fake_email_background,
    send_fake_email_sync,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_or_404(task_id: int, db: Session, current_user: User):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = Task(
        **task_data.model_dump(),
        owner_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    delete_cache("analytics_summary")
    background_tasks.add_task(send_fake_email_background, task.title)

    return task


@router.post("/sync-email", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_with_sync_email(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = Task(
        **task_data.model_dump(),
        owner_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    delete_cache("analytics_summary")
    send_fake_email_sync(task.title)

    return task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if page < 1:
        page = 1

    if size < 1:
        size = 20

    if size > 100:
        size = 100

    offset = (page - 1) * size

    return (
        db.query(Task)
        .filter(Task.owner_id == current_user.id)
        .order_by(Task.id.desc())
        .offset(offset)
        .limit(size)
        .all()
    )


@router.get("/search/", response_model=list[TaskResponse])
def search_tasks(
    keyword: str,
    mode: str = "prefix",
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if page < 1:
        page = 1

    if size < 1:
        size = 20

    if size > 100:
        size = 100

    offset = (page - 1) * size

    if mode == "contains":
        search_pattern = f"%{keyword}%"
    else:
        search_pattern = f"{keyword}%"

    return (
        db.query(Task)
        .filter(
            Task.owner_id == current_user.id,
            (
                (Task.title.ilike(search_pattern)) |
                (Task.description.ilike(search_pattern))
            )
        )
        .order_by(Task.id.desc())
        .offset(offset)
        .limit(size)
        .all()
    )


@router.get("/full-text-search/", response_model=list[TaskResponse])
def full_text_search_tasks(
    keyword: str,
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if page < 1:
        page = 1

    if size < 1:
        size = 20

    if size > 100:
        size = 100

    offset = (page - 1) * size

    query = text("""
        SELECT *
        FROM tasks
        WHERE owner_id = :owner_id
          AND to_tsvector('english', title || ' ' || COALESCE(description, ''))
              @@ plainto_tsquery('english', :keyword)
        ORDER BY id DESC
        LIMIT :size OFFSET :offset
    """)

    result = db.execute(
        query,
        {
            "owner_id": current_user.id,
            "keyword": keyword,
            "size": size,
            "offset": offset
        }
    )

    return result.mappings().all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_task_or_404(task_id, db, current_user)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_or_404(task_id, db, current_user)

    for field, value in task_data.model_dump().items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    delete_cache("analytics_summary")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_or_404(task_id, db, current_user)

    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    delete_cache("analytics_summary")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_or_404(task_id, db, current_user)

    db.delete(task)
    db.commit()
    delete_cache("analytics_summary")

    return None