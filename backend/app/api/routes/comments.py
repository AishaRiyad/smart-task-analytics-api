from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.database import get_db
from app.db.models import Comment, Task, User
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    comment: CommentCreate,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_comment = Comment(
        content=comment.content,
        task_id=task.id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/{task_id}", response_model=list[CommentResponse])
def get_task_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == current_user.id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return (
        db.query(Comment)
        .filter(Comment.task_id == task_id)
        .order_by(Comment.created_at.desc())
        .all()
    )


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = (
        db.query(Comment)
        .filter(
            Comment.id == comment_id,
            Comment.user_id == current_user.id
        )
        .first()
    )

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_comment.content = comment.content

    db.commit()
    db.refresh(db_comment)

    return db_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = (
        db.query(Comment)
        .filter(
            Comment.id == comment_id,
            Comment.user_id == current_user.id
        )
        .first()
    )

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()

    return None