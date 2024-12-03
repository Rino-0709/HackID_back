from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Создание базового класса для моделей
Base = declarative_base()

# Загрузка переменных из .env
load_dotenv()

# Получение строки подключения из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Создание фабрики сессий
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Функция для получения сессии
async def get_db():
    async with async_session() as session:
        yield session
