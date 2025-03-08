from fastapi import FastAPI
from app.routers.users import router as users_router
from app.database import Base, engine

app = FastAPI()
app.include_router(users_router, prefix="/users", tags=["User"])

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
