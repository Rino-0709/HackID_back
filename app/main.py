from fastapi import FastAPI
from app.routes import user, hackathon, stack, admin

app = FastAPI()

# Подключение маршрутов
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(hackathon.router, prefix="/api/hackathon", tags=["Hackathon"])
app.include_router(stack.router, prefix="/api/tech-stack", tags=["Stack"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
