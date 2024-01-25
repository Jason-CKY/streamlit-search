import random
import streamlit as st
import templates
from urllib import parse
from schemas.search import SearchResult

def mock_search_results(search: str):
    return [
        SearchResult(
            title=f"Article #{i+1} {search}",
            page_content="Lorem Ipsum fdskfls " * 50,
            link="https://google.com",
        ) for i in range(20)
    ]


def set_session_state():
    # set default values
    if 'search' not in st.session_state:
        st.session_state.search = None

    # get parameters in url
    if 'search' in st.query_params:
        print("TEST SEARCH IS IN QUERY PARAMS")
        new_search = parse.unquote(st.query_params['search'])
        print(new_search)
        st.session_state.search = new_search


def main():
    set_session_state()
    st.set_page_config(page_title='AI-Powered Search Engine')
    st.write(templates.load_css(), unsafe_allow_html=True)
    st.title('AI-Powered Search')
    search = st.text_input('Enter search words:', value=st.session_state.search)
    if search:
        st.query_params["search"] = search
        results = mock_search_results(search)
        # show number of results and time taken
        st.write(templates.number_of_results(len(results), random.random()),
                 unsafe_allow_html=True)
        # search results
        for i, result in enumerate(results):
            st.write(
                templates.search_result(
                    i=i,
                    url=result.link,
                    title=result.title,
                    highlights=result.page_content), unsafe_allow_html=True)

if __name__ == '__main__':
    main()