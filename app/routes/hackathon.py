from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.future import select
from app.models.hackathon import SubmittedQuestionnaire
from app.models.hackathon import Hackathon
from app.schemas.hackathon import HackathonRegister, HackathonRegisterResponse, HackathonResponse
import random

router = APIRouter()

@router.get("/", response_model=list[HackathonResponse])
async def get_hackathons(db: AsyncSession = Depends(get_db)):
    # Выполняем запрос для получения всех хакатонов из таблицы active_hackathons
    result = await db.execute(select(Hackathon))
    hackathons = result.scalars().all()

    if not hackathons:
        raise HTTPException(status_code=404, detail="Хакатоны не найдены")

    return hackathons


@router.post("/register", response_model=HackathonRegisterResponse)
async def register_for_hackathon(
    registration_data: HackathonRegister,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Генерация случайного id_telegram
        id_telegram = random.randint(1000, 9999)

        # Вставка данных в таблицу `submitted_questionnaires`
        questionnaire = SubmittedQuestionnaire(
            hackathon_id=registration_data.hackathon_id,
            id_telegram=id_telegram,
            captain_tag=registration_data.captain_tag,
            participant_role=registration_data.role_in_team,
            stack_list=registration_data.technology_stack,
            team_name=registration_data.team_name,
        )

        db.add(questionnaire)
        await db.commit()

        return {"message": "Регистрационная форма успешно подана"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка регистрации: {str(e)}")
