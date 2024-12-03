from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.models.stack import TechStack
from app.schemas.stack import TechStackCreate, TechStackResponse
import random

router = APIRouter()

@router.get("/")
async def get_stacks(db: AsyncSession = Depends(get_db)):
    # SQL-запрос для получения всех записей из таблицы stack_table
    query = text("SELECT technology_id AS id, technology_name AS name FROM stack_table")
    result = await db.execute(query)
    stacks = result.fetchall()

    # Преобразование результата в список словарей
    return [{"id": row.id, "name": row.name} for row in stacks]

@router.post("/add", response_model=TechStackResponse)
async def add_tech_stack(tech_stack: TechStackCreate, db: AsyncSession = Depends(get_db)):
    # Приведение названия технологии к нижнему регистру
    tech_name = tech_stack.tech_name.lower()

    # Проверка на наличие слова в таблице forbidden_words
    forbidden_query = text("SELECT word FROM forbidden_words WHERE word = :word")
    forbidden_result = await db.execute(forbidden_query, {"word": tech_name})
    forbidden_word = forbidden_result.scalar_one_or_none()
    if forbidden_word:
        raise HTTPException(status_code=400, detail="Этот стек нельзя добавить.")
    
    # Проверка, чтобы стек с таким же названием не существовал
    existing_stack_query = text("SELECT * FROM stack_table WHERE technology_name = :name")
    existing_stack = await db.execute(existing_stack_query, {"name": tech_name})
    existing_stack = existing_stack.fetchall()
    if existing_stack:
        raise HTTPException(status_code=400, detail="Технология уже существует.")
    
    # Генерация уникального ID
    technology_id = random.randint(1000, 9999)

    # Добавление нового стека в базу данных
    new_stack = TechStack(technology_id=technology_id, technology_name=tech_stack.tech_name)
    db.add(new_stack)
    await db.commit()

    return TechStackResponse(message="Новый стек успешно добавлен.")