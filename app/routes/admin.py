from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import text
from app.database import get_db
from app.schemas.hackathon import MessageResponse
from app.models.hackathon import Hackathon
from app.schemas.hackathon import ActiveHackathonCreate, ActiveHackathonResponse
from app.models.forbidden_word import ForbiddenWord, ForbiddenWordDeleteRequest
from app.models.user import RegisteredUser
from app.schemas.forbidden_word import ForbiddenWordCreate, ForbiddenWordResponse, ForbiddenWordGetResponse

router = APIRouter()

@router.post("/forbidden-word/add", response_model=ForbiddenWordResponse)
async def add_forbidden_word(forbidden_word: ForbiddenWordCreate, db: AsyncSession = Depends(get_db)):
    # Приведение слова к нижнему регистру
    word = forbidden_word.word.lower()

    # Проверка, чтобы слово не существовало в таблице
    existing_word_query = text("SELECT * FROM forbidden_words WHERE word = :word")
    existing_word = await db.execute(existing_word_query, {"word": word})
    existing_word = existing_word.fetchone()
    if existing_word:
        raise HTTPException(status_code=400, detail="Это слово уже запрещено.")

    # Добавление нового слова в базу данных
    new_word = ForbiddenWord(word=word)
    db.add(new_word)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        print(f"Добавляемое слово: {word}")
        raise HTTPException(status_code=400, detail=f"Ошибка при добавлении слова: {str(e)}")

    # Удаление стека из stack_table, если в названии содержится запрещённое слово
    try:
        delete_query = text("DELETE FROM stack_table WHERE LOWER(technology_name) LIKE :word")
        await db.execute(delete_query, {"word": f"%{word}%"})
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка при удалении стека: {str(e)}")

    return ForbiddenWordResponse(message="Слово добавлено в список запрещённых и стеки с этим словом удалены.")

@router.get("/forbidden-word", response_model=list[ForbiddenWordGetResponse])
async def get_forbidden_words(db: AsyncSession = Depends(get_db)):
    # Запрос к базе данных для получения всех слов
    result = await db.execute(text("SELECT id_word AS id, word FROM forbidden_words"))
    forbidden_words = result.fetchall()
    
    # Форматирование данных
    response = [{"id": row.id, "word": row.word} for row in forbidden_words]
    return response

@router.post("/forbidden-words/delete", response_model=dict)
async def delete_forbidden_word(request: ForbiddenWordDeleteRequest, db: AsyncSession = Depends(get_db)):
    # Удаление слова из таблицы
    result = await db.execute(text("DELETE FROM forbidden_words WHERE word = :word RETURNING id_word"), {"word": request.word})
    deleted_row = result.fetchone()

    # Если слово не найдено
    if not deleted_row:
        raise HTTPException(status_code=404, detail="Слово не найдено в списке запрещённых.")

    # Подтвердить изменения
    await db.commit()
    return {"message": "Запрещённое слово удалено"}

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    # Получаем все пользователи из таблицы
    result = await db.execute(
        text("SELECT id_telegram, tag_telegram FROM registered_users")
    )
    users = result.fetchall()
    
    # Формируем список пользователей
    users_list = [{"user_id": user.id_telegram, "telegram_tag": user.tag_telegram} for user in users]
    
    return users_list

@router.post("/hackathons/add", response_model=ActiveHackathonResponse)
async def add_hackathon(
    hackathon: ActiveHackathonCreate, db: AsyncSession = Depends(get_db)
):
    # Проверка, чтобы хакатон с таким же названием не существовал
    existing_hackathon = await db.execute(
        select(Hackathon).filter(Hackathon.hackathon_name == hackathon.hackathon_name)
    )
    existing_hackathon = existing_hackathon.scalars().first()
    if existing_hackathon:
        raise HTTPException(status_code=400, detail="Хакатон с таким названием уже существует.")

    # Добавление нового хакатона в базу данных без генерации ID
    new_hackathon = Hackathon(
        hackathon_name=hackathon.hackathon_name,
        host_hackathon=hackathon.host_hackathon,
        activity_status=hackathon.activity_status
    )
    db.add(new_hackathon)
    await db.commit()

    return ActiveHackathonResponse(message="Хакатон успешно добавлен")

@router.post("/change-status", response_model=MessageResponse)
async def change_hackathon_status(hackathon_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем хакатон по ID
    result = await db.execute(select(Hackathon).filter(Hackathon.hackathon_id == hackathon_id))
    hackathon = result.scalars().first()

    # Если хакатон не найден, возвращаем ошибку
    if not hackathon:
        raise HTTPException(status_code=404, detail="Хакатон не найден")

    # Меняем статус на противоположный
    hackathon.activity_status = 1 if hackathon.activity_status == 0 else 0

    # Применяем изменения
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка при изменении статуса хакатона")

    return MessageResponse(message="Статус хакатона успешно изменён")