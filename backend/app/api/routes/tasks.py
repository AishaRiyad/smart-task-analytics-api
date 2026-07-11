from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy import or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import get_current_user
from app.db.database import get_db
from app.db.models import Task, User
from app.schemas.task import TaskCreate, TaskResponse
from app.services.cache_service import delete_cache
from app.services.email_service import (
    send_fake_email_background,
    send_fake_email_sync,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

ANALYTICS_CACHE_KEY = "analytics_summary"


async def get_task_or_404(
    task_id: int,
    db: AsyncSession,
    current_user: User,
) -> Task:
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id,
        )
    )

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(
        **task_data.model_dump(),
        owner_id=current_user.id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    await delete_cache(ANALYTICS_CACHE_KEY)

    background_tasks.add_task(
        send_fake_email_background,
        task.title,
    )

    return task


@router.post(
    "/sync-email",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_with_sync_email(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(
        **task_data.model_dump(),
        owner_id=current_user.id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    await delete_cache(ANALYTICS_CACHE_KEY)

    send_fake_email_sync(task.title)

    return task


@router.get(
    "/",
    response_model=list[TaskResponse],
)
async def get_tasks(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    offset = (page - 1) * size

    result = await db.execute(
        select(Task)
        .where(Task.owner_id == current_user.id)
        .order_by(Task.id.desc())
        .offset(offset)
        .limit(size)
    )

    return result.scalars().all()


@router.get(
    "/search/",
    response_model=list[TaskResponse],
)
async def search_tasks(
    keyword: str = Query(min_length=1),
    mode: str = Query(default="prefix", pattern="^(prefix|contains)$"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    offset = (page - 1) * size

    search_pattern = (
        f"%{keyword}%"
        if mode == "contains"
        else f"{keyword}%"
    )

    result = await db.execute(
        select(Task)
        .where(
            Task.owner_id == current_user.id,
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern),
            ),
        )
        .order_by(Task.id.desc())
        .offset(offset)
        .limit(size)
    )

    return result.scalars().all()


@router.get(
    "/full-text-search/",
    response_model=list[TaskResponse],
)
async def full_text_search_tasks(
    keyword: str = Query(min_length=1),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    offset = (page - 1) * size

    query = text(
        """
        SELECT *
        FROM tasks
        WHERE owner_id = :owner_id
          AND to_tsvector(
                'english',
                COALESCE(title, '') || ' ' ||
                COALESCE(description, '')
              )
              @@ plainto_tsquery('english', :keyword)
        ORDER BY id DESC
        LIMIT :size OFFSET :offset
        """
    )

    result = await db.execute(
        query,
        {
            "owner_id": current_user.id,
            "keyword": keyword,
            "size": size,
            "offset": offset,
        },
    )

    return result.mappings().all()


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_task_or_404(
        task_id,
        db,
        current_user,
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await get_task_or_404(
        task_id,
        db,
        current_user,
    )

    for field, value in task_data.model_dump().items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    await delete_cache(ANALYTICS_CACHE_KEY)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await get_task_or_404(
        task_id,
        db,
        current_user,
    )

    await db.delete(task)
    await db.commit()

    await delete_cache(ANALYTICS_CACHE_KEY)

    return None