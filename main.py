from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import session_context
from app.chat.router import router as chat_router
from app.quiz.router import router as quiz_router

app = FastAPI(lifespan=session_context)

# On inclut les routes modulaires
app.include_router(chat_router, prefix="")
app.include_router(quiz_router, prefix="")

@app.get("/")
async def root():
    return RedirectResponse(url="/docs", status_code=308)