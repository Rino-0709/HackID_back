from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
import random

router = APIRouter()

@router.post("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Генерируем заглушки для id_telegram, tag_telegram, role
    id_telegram = random.randint(1000, 9999)
    tag_telegram = "@username"+str(id_telegram)
    role = 1

    # Проверяем, существует ли пользователь с указанным id_telegram
    result = await db.execute(select(User).where(User.id_telegram == id_telegram))
    user = result.scalar()

    if not user:
        # Создаем нового пользователя
        user = User(
            id_telegram=id_telegram,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            study_group=user_data.study_group,
            tag_telegram=tag_telegram,
            role=role,
        )
        db.add(user)
    else:
        # Обновляем данные существующего пользователя
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.study_group = user_data.study_group

    await db.commit()
    await db.refresh(user)
    return user
