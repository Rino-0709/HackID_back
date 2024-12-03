from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from app.database import get_db
from app.models.forbidden_word import ForbiddenWord
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

    return ForbiddenWordResponse(message="Слово добавлено в список запрещённых.")

@router.get("/forbidden-word", response_model=list[ForbiddenWordGetResponse])
async def get_forbidden_words(db: AsyncSession = Depends(get_db)):
    # Запрос к базе данных для получения всех слов
    result = await db.execute(text("SELECT id_word AS id, word FROM forbidden_words"))
    forbidden_words = result.fetchall()
    
    # Форматирование данных
    response = [{"id": row.id, "word": row.word} for row in forbidden_words]
    return response