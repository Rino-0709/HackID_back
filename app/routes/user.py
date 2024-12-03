from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

router = APIRouter()

@router.post("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Логика обновления профиля
    user = await db.execute(
        select(User).where(User.id_telegram == 1)  # Здесь будет ID из токена
    )
    user = user.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.study_group = user_data.study_group

    db.add(user)
    await db.commit()
    return user
