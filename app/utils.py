import uuid
from fastapi import Request, Response
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

def get_set_session_id(request: Request, response: Response, cookie_name: str) -> str:
    """
    Récupère l'identifiant de session depuis les cookies ou en génère un nouveau,
    et le stocke dans un cookie.
    """
    cookie_value = request.cookies.get(cookie_name)

    if not cookie_value:
        cookie_value = str(uuid.uuid4())
        response.set_cookie(
            key=cookie_name,
            value=cookie_value,
            httponly=True,
            samesite='lax',
            max_age=60 * 60 * 24,
            secure=True
        )
    return cookie_value


def get_chat_history(chat_id: str, app) -> BaseChatMessageHistory:
    if chat_id not in app.state.history_store:
        app.state.history_store[chat_id] = ChatMessageHistory()
    return app.state.history_store[chat_id]


def get_quiz_history(quiz_id: str, app) -> BaseChatMessageHistory:
    if quiz_id not in app.state.history_store:
        app.state.history_store[quiz_id] = ChatMessageHistory()
    return app.state.history_store[quiz_id]