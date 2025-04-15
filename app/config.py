import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import weaviate as wv
from weaviate.classes.init import Auth
from fastapi import FastAPI
from langchain_mistralai import ChatMistralAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore

# Charger les variables d'environnement
load_dotenv()

@asynccontextmanager
async def session_context(app: FastAPI):
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
    weaviate_instance_url = os.getenv("WEAVIATE_URL")

    if not mistral_api_key or not weaviate_api_key or not weaviate_instance_url:
        raise ValueError("Clés API Mistral / Weaviate et URL manquantes.")

    try:
        app.state.client = wv.connect_to_weaviate_cloud(
            cluster_url=weaviate_instance_url,
            auth_credentials=Auth.api_key(weaviate_api_key)
        )
        app.state.llm = ChatMistralAI(
            model="mistral-small-latest",
            api_key=mistral_api_key
        )
        app.state.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        app.state.vector_store = WeaviateVectorStore(
            client=app.state.client,
            index_name="Article",
            text_key="text",
            attributes=["title", "authors", "creationDate", "originalFile", "pages"],
            embedding=app.state.embeddings
        )
        app.state.history_store = {}

        yield

    except Exception as e:
        logging.error(f"Erreur lors de l'initialisation : {e}")
        raise
    finally:
        if hasattr(app.state, 'client') and app.state.client:
            app.state.client.close()