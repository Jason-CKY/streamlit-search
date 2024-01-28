import asyncio
import time
import streamlit as st
import templates
from urllib import parse
from core.search import mock_get_source_documents
from core.feedback import handle_search_feedback, handle_rag_feedback
from core.conversation_handler import ConversationHandler
from core.settings import settings
from core.sidebar import sidebar
from loguru import logger

def set_session_state():
    # set default values
    if 'search' not in st.session_state:
        st.session_state.search = None
    if 'page' not in st.session_state:
        st.session_state.page = 1
    if '_search' not in st.session_state:
        st.session_state._search = None
    if 'search_results' not in st.session_state:
        st.session_state._search = None
    if 'llm_response' not in st.session_state:
        st.session_state.llm_response = None    
    if 'query_time' not in st.session_state:
        st.session_state.query_time = None
    if 'rag_feedback' not in st.session_state:
        st.session_state.rag_feedback = None
    if 'search_feedbacks' not in st.session_state:
        st.session_state.search_feedbacks = {}  
    if 'search_params' not in st.session_state:
        st.session_state.search_params = {}

    # get parameters in url
    if 'search' in st.query_params:
        new_search = parse.unquote(st.query_params['search'])
        st.session_state.search = new_search
    if 'page' in st.query_params:
        st.session_state.page = int(st.query_params['page'])

def search_input_on_change():
    st.query_params["search"] = st.session_state.search
    st.query_params["page"] = 1

async def main():
    set_session_state()
    st.set_page_config(
        page_title='AI-Powered Search Engine', 
        initial_sidebar_state="collapsed"
    )
    st.write(templates.load_css(), unsafe_allow_html=True)
    st.title('AI-Powered Search')

    sidebar()

    search = st.text_input('Enter search words:', key="search", on_change=search_input_on_change)
    if search:
        if st.session_state._search != search:
            with st.spinner("Searching for docs..."):
                start_time = time.time()
                results = await mock_get_source_documents(search)
                query_time = time.time() - start_time
                st.session_state._search = search
                st.session_state.search_results = results           
                st.session_state.query_time = query_time

                # For the case of new generation, set as placeholder for later streaming
                llm_response_div = st.empty()
        else:
            results = st.session_state.search_results
            llm_response = st.session_state.llm_response
            query_time = st.session_state.query_time

            # For case of existing results, just write the existing response from session_state
            # We follow the case of Bing search, where the LLM response will not show on the screen
            # if the user goes to another page before it finishes streaming, but will show on all pages
            # after it finishes streaming. If it is stopped halfway through streaming via a page change, 
            # restart streaming if the user goes back to page 1
            if st.session_state.llm_response is not None:
                st.chat_message("assistant").write(llm_response)
                handle_rag_feedback(
                    query=search, 
                    rag_response=st.session_state.llm_response, 
                    key="rag_feedback", 
                    disable_with_score=st.session_state.rag_feedback["score"] if st.session_state.rag_feedback else None
                )  
                llm_response_div = None        
            elif st.session_state.page == 1:
                llm_response_div = st.empty()
            else:
                llm_response_div = None

        from_i = (st.session_state.page - 1) * settings.page_size
        paginated_results = results[from_i:from_i + settings.page_size]

        # show number of results and time taken
        st.write(templates.number_of_results(len(results), query_time),
                 unsafe_allow_html=True)
        
        # search results
        for i, result in enumerate(paginated_results):
            st.write(
                templates.search_result(
                    i=from_i + i,
                    url=result.metadata["link"],
                    title=result.metadata["title"],
                    highlights=result.page_content), unsafe_allow_html=True)
            handle_search_feedback(
                query=search,
                search_result=result,
                key=f"search_feedback_{from_i + i}",
                disable_with_score=st.session_state.search_feedbacks[f"search_feedback_{from_i + i}"]["score"] if st.session_state.search_feedbacks and f"search_feedback_{from_i + i}" in st.session_state.search_feedbacks else None,
            )
        # pagination
        if len(results) > settings.page_size:
            total_pages = (len(results) + settings.page_size - 1) // settings.page_size
            templates.pagination(total_pages, search, st.session_state.page)

        if llm_response_div is not None:
            st.session_state.llm_response = None
            with llm_response_div.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                handler = ConversationHandler(
                    model = settings.llm_model_id,
                    temperature = 0,
                    max_tokens = 1024,
                )
                rag_chain = handler.get_rag_chain()
                async for chunk in rag_chain.astream({
                    "context": handler.format_docs(results),
                    "question": search,
                }):
                    full_response += chunk + " "
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.llm_response = full_response
                st.rerun()


if __name__ == '__main__':
    asyncio.run(main())