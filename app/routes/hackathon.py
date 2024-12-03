from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hackathon import SubmittedQuestionnaire
from app.schemas.hackathon import HackathonRegister, HackathonRegisterResponse
import random

router = APIRouter()

@router.get("/")
async def get_hackathons():
    hackathons = [
        {"id": 1, "name": "Hackathon 1", "host": "Москва", "status": 1},
        {"id": 2, "name": "Hackathon 2", "host": "онлайн", "status": 0},
        {"id": 3, "name": "Hackathon 3", "host": "Санкт-Петербург", "status": 1},
        {"id": 4, "name": "Hackathon 4", "host": "Екатеринбург", "status": 0},
        {"id": 5, "name": "Hackathon 5", "host": "Новосибирск", "status": 1},
        {"id": 6, "name": "Hackathon 6", "host": "онлайн", "status": 1},
        {"id": 7, "name": "Hackathon 7", "host": "Казань", "status": 0},
        {"id": 8, "name": "Hackathon 8", "host": "Красноярск", "status": 1},
        {"id": 9, "name": "Hackathon 9", "host": "Нижний Новгород", "status": 0},
        {"id": 10, "name": "Hackathon 10", "host": "онлайн", "status": 1},
    ]
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
