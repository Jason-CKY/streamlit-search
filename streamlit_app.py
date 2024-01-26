import time
import asyncio
import random
import streamlit as st
import templates
from urllib import parse
from core.search import mock_search_results, tick
from core.settings import settings


def set_session_state():
    # set default values
    if 'search' not in st.session_state:
        st.session_state.search = None
    if 'page' not in st.session_state:
        st.session_state.page = 1

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

    placeholder = st.empty()
    # await tick(placeholder)
   
    search = st.text_input('Enter search words:', key="search", on_change=search_input_on_change)
    if search:
        with st.spinner('Wait for it...'):
            results = await mock_search_results(search)
        from_i = (st.session_state.page - 1) * settings.page_size
        paginated_results = results[from_i:from_i + settings.page_size]
        # show number of results and time taken
        st.write(templates.number_of_results(len(results), random.random()),
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