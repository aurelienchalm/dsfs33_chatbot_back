from fastapi import APIRouter, Request, Response
import logging
import weaviate as wv

from app.models import ChatRequest, ChatResponse
from app.utils import get_set_session_id
from .logic import run_chat_chain

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chatbot_endpoint(
    chat: ChatRequest,
    request: Request,
    response: Response
):
    chat_id = get_set_session_id(request, response, "chat_id")

    final_answer = None
    error_message = ""

    try:
        raw_response = await run_chat_chain(user_input=chat.user, chat_id=chat_id, app=request.app)

        logging.warning(f"Réponse brute reçue du LLM (chat) : {raw_response}")

        if isinstance(raw_response, str):
            final_answer = raw_response.strip()
        else:
            final_answer = str(raw_response)

        # On ajoute une vérif simple pour éviter de renvoyer un texte vide ou inapproprié
        if not final_answer or "je ne sais pas" in final_answer.lower():
            error_message = "Le modèle n’a pas pu générer une réponse pertinente."

    except wv.exceptions.WeaviateBaseError as e:
        error_message = f"Weaviate error: {e}"
        logging.error(error_message)
    except Exception as e:
        error_message = f"General error: {e}"
        logging.error(error_message)

    if not final_answer:
        final_answer = "Désolé, je n'ai pas pu générer de réponse."

    return ChatResponse(answer=final_answer, error=error_message)