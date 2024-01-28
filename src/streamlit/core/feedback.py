import requests
from langchain_core.documents import Document
from loguru import logger
from streamlit_feedback import streamlit_feedback
from core.settings import settings

def submit_search_feedback(feedback, query: str, search_result: Document):
    submit_feedback_json = {
            "query": query,
            "page_content": search_result.page_content,
            "title": search_result.metadata["title"],
            "link": search_result.metadata["link"],
            "score": settings.score_mappings["faces"][feedback["score"]],
            "comments": feedback["text"],
    }
    logger.debug(submit_feedback_json)
    response = requests.post(
        f"{settings.directus_host}/items/{settings.directus_search_feedback_table}",
        headers={
            "Authorization": f"Bearer {settings.directus_api_key}"
        },
        json=submit_feedback_json,
    )
    if response.status_code != 200:
        logger.error(response.json())


def handle_search_feedback(query: str, search_result: Document, key: str):
    # Render feedback and set on_submit flag to submit feedback to directus
    streamlit_feedback(
        feedback_type="faces",
        optional_text_label="[Optional] Please provide an explanation",
        key=key,
        align="flex-start",
        on_submit = lambda feedback: submit_search_feedback(feedback, query, search_result)
    )

def submit_rag_feedback(feedback, query: str, rag_response: str):
    submit_feedback_json = {
            "query": query,
            "rag_response": rag_response,
            "score": settings.score_mappings["faces"][feedback["score"]],
            "comments": feedback["text"],
    }
    logger.debug(submit_feedback_json)
    response = requests.post(
        f"{settings.directus_host}/items/{settings.directus_rag_feedback_table}",
        headers={
            "Authorization": f"Bearer {settings.directus_api_key}"
        },
        json=submit_feedback_json,
    )
    if response.status_code != 200:
        logger.error(response.json())

def handle_rag_feedback(query: str, rag_response: str, key: str):
    # Render feedback and set on_submit flag to submit feedback to directus
    streamlit_feedback(
        feedback_type="faces",
        optional_text_label="[Optional] Please provide an explanation",
        key=key,
        align="flex-start",
        on_submit = lambda feedback: submit_rag_feedback(feedback, query, rag_response)
    )
    