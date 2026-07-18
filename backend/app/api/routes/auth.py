from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import (
    RefreshTokenRequest,
    TokenPair,
    UserCreate,
    UserResponse,
)
from app.services.auth_service import (
    ALGORITHM,
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def unauthorized_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    existing_user_result = await db.execute(
        select(User).where(
            or_(
                User.username == user_data.username,
                User.email == user_data.email,
            )
        )
    )

    existing_user = existing_user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=TokenPair,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user_result = await db.execute(
        select(User).where(
            User.username == form_data.username
        )
    )

    user = user_result.scalar_one_or_none()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise unauthorized_exception(
            "Invalid username or password"
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post(
    "/refresh",
    response_model=TokenPair,
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = jwt.decode(
            refresh_data.refresh_token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise unauthorized_exception(
                "Invalid refresh token"
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise unauthorized_exception(
                "Invalid refresh token"
            )

        parsed_user_id = int(user_id)

    except (JWTError, TypeError, ValueError):
        raise unauthorized_exception(
            "Invalid refresh token"
        )

    user_result = await db.execute(
        select(User).where(
            User.id == parsed_user_id
        )
    )

    user = user_result.scalar_one_or_none()

    if not user:
        raise unauthorized_exception(
            "User not found"
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "access":
            raise unauthorized_exception(
                "Invalid access token"
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise unauthorized_exception(
                "Invalid access token"
            )

        parsed_user_id = int(user_id)

    except (JWTError, TypeError, ValueError):
        raise unauthorized_exception(
            "Invalid access token"
        )

    user_result = await db.execute(
        select(User).where(
            User.id == parsed_user_id
        )
    )

    user = user_result.scalar_one_or_none()

    if not user:
        raise unauthorized_exception(
            "User not found"
        )

    return user


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user