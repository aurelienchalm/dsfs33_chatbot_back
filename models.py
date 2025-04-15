from typing import List, Optional

from pydantic import BaseModel


class QuizQuestion(BaseModel):
    question: str
    choices: List[str]
    answer: str
    origin: Optional[str] = None
    explain: Optional[str] = None


class Quiz(BaseModel):
    topic: str
    questions: List[QuizQuestion]


class ChatRequest(BaseModel):
    user: str


class ChatResponse(BaseModel):
    answer: str
    error: Optional[str] = None


class QuizRequest(BaseModel):
    user: str


class QuizResponse(BaseModel):
    quiz: Optional[Quiz] = None
    error: Optional[str] = None
