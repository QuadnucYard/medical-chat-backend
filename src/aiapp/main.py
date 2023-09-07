from fastapi import Body, FastAPI

from aiapp.config import settings
from aiapp import service

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json")

@app.get("/api")
def ping():
    return "OK"


@app.post("/api/qa", tags=["ai"])
async def qa(question: str = Body()):
    return await service.qa(question)
