import datetime
import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.utils import get_chat_history
from app.prompts import CHAT_PROMPT_TEMPLATE


async def run_chat_chain(user_input: str, chat_id: str, app) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CHAT_PROMPT_TEMPLATE),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    retriever = app.state.vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    def format_docs(docs):
        content = []
        for doc in docs:
            if hasattr(doc, "page_content") and isinstance(doc.page_content, str):
                authors = doc.metadata.get("authors") if isinstance(doc.metadata.get("authors"), str) and len(doc.metadata.get("authors")) < 60 else ""
                title = doc.metadata.get("title") if isinstance(doc.metadata.get("title"), str) and len(doc.metadata.get("title")) < 60 else ""
                created_raw = doc.metadata.get("creationDate")
                try:
                    created = datetime.datetime.strptime(str(created_raw), "%Y%m%d") if created_raw and isinstance(created_raw, int) else datetime.datetime.fromisoformat(created_raw)
                except ValueError:
                    created = ""
                filename = doc.metadata.get("originalFile")
                pages = doc.metadata.get("pages", [])
                pages = ', '.join(map(str, pages)) if pages else ""
                document = doc.page_content.strip()
                properties = f"Propriétés: [authors: '{authors}', title: '{title}', filename: '{filename}', pages: '{pages}', date : '{created}']"
                content.append(f"\n\n===============\n{document}\n\n{properties}")
        return "".join(content)

    rag_chain_core = (
        RunnablePassthrough.assign(context=(lambda x: x["question"]) | retriever | format_docs)
        | prompt
        | app.state.llm
        | StrOutputParser()
    )

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain_core,
        lambda session_id: get_chat_history(session_id, app),
        input_messages_key="question",
        history_messages_key="history",
    )

    config = {"configurable": {"session_id": chat_id}}
    response = await conversational_rag_chain.ainvoke({"question": user_input}, config=config)

    logging.info(str(response))
    return str(response)