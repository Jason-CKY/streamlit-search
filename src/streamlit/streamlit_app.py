import asyncio
import time
import streamlit as st
import templates
from urllib import parse
from core.search import mock_get_source_documents, get_rag_response
from core.settings import settings


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
    st.set_page_config(page_title='AI-Powered Search Engine')
    st.write(templates.load_css(), unsafe_allow_html=True)
    st.title('AI-Powered Search')
   
    search = st.text_input('Enter search words:', key="search", on_change=search_input_on_change)
    if search:
        if st.session_state._search != search:
            with st.status('Generating answers...', expanded=True) as status:
                st.write('Searching for documents...')
                
                start_time = time.time()
                results = await mock_get_source_documents(search)
                query_time = time.time() - start_time
                
                st.write('Generating AI response...')
                
                start_time = time.time()
                llm_response = await get_rag_response(search, results)
                llm_response_time = time.time() - start_time

                st.session_state._search = search
                st.session_state.search_results = results
                st.session_state.llm_response = llm_response
                st.session_state.query_time = query_time
                status.update(label="Generation complete", state="complete", expanded=False)
        else:
            results = st.session_state.search_results
            llm_response = st.session_state.llm_response
            query_time = st.session_state.query_time

        from_i = (st.session_state.page - 1) * settings.page_size
        paginated_results = results[from_i:from_i + settings.page_size]

        # Show AI RAG Response
        st.chat_message("assistant").write(llm_response)
        # show number of results and time taken
        st.write(templates.number_of_results(len(results), query_time),
                 unsafe_allow_html=True)
        # search results
        for i, result in enumerate(paginated_results):
            st.write(
                templates.search_result(
                    i=from_i + i,
                    url=result.link,
                    title=result.title,
                    highlights=result.page_content), unsafe_allow_html=True)
        # pagination
        if len(results) > settings.page_size:
            total_pages = (len(results) + settings.page_size - 1) // settings.page_size
            templates.pagination(total_pages, search, st.session_state.page,)

if __name__ == '__main__':
    asyncio.run(main())