from fastapi import APIRouter, Request, Response
import logging
import weaviate as wv
import pydantic as py
import json

from app.models import QuizRequest, QuizResponse, Quiz
from app.utils import get_set_session_id
from .logic import run_quiz_chain

router = APIRouter()


@router.post("/quiz", response_model=QuizResponse)
async def quiz_endpoint(
    quiz: QuizRequest,
    request: Request,
    response: Response
):
    quiz_id = get_set_session_id(request, response, "quiz_id")

    parsed_quiz = None
    error_message = ""

    try:
        raw_response = await run_quiz_chain(user_input=quiz.user, quiz_id=quiz_id, app=request.app)

        # Nettoyage si la réponse commence par ```json
        if raw_response.startswith("```json"):
            raw_response = raw_response[7:-3].strip()

        logging.warning(f"Réponse brute reçue du LLM (quiz) : {raw_response}")

        # Essai de parsing
        try:
            quiz_dict = json.loads(raw_response)
            parsed_quiz = Quiz.model_validate(quiz_dict)
        except json.JSONDecodeError:
            error_message = "La réponse n'est pas un JSON valide."
            logging.error(error_message)
        except py.ValidationError as ve:
            error_message = f"Erreur de validation du JSON : {ve}"
            logging.error(error_message)

    except wv.exceptions.WeaviateBaseError as e:
        error_message = f"Weaviate error: {e}"
        logging.error(error_message)
    except Exception as e:
        error_message = f"General error: {e}"
        logging.error(error_message)

    return QuizResponse(quiz=parsed_quiz, error=error_message)