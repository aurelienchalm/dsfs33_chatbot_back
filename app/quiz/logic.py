import datetime
import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.prompts import QUIZ_PROMPT_TEMPLATE
from app.utils import get_quiz_history


async def run_quiz_chain(user_input: str, quiz_id: str, app) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", QUIZ_PROMPT_TEMPLATE),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    retriever = app.state.vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 50}
    )

    def format_docs(docs):
        content = []
        for doc in docs:
            if hasattr(doc, "page_content") and isinstance(doc.page_content, str):
                created_raw = doc.metadata.get("creationDate")
                try:
                    created = datetime.datetime.strptime(str(created_raw), "%Y%m%d") \
                        if created_raw and isinstance(created_raw, int) \
                        else datetime.datetime.fromisoformat(created_raw)
                except ValueError:
                    created = ""
                filename = doc.metadata.get("originalFile")
                pages = doc.metadata.get("pages", [])
                pages = ', '.join(map(str, pages)) if pages else ""
                document = doc.page_content.strip()
                properties = f"Propriétés: [filename: '{filename}', pages: '{pages}', date : '{created}']"
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
        lambda session_id: get_quiz_history(session_id, app),
        input_messages_key="question",
        history_messages_key="history",
    )

    config = {"configurable": {"session_id": quiz_id}}
    response = await conversational_rag_chain.ainvoke({"question": user_input}, config=config)

    logging.info(str(response))
    return str(response)