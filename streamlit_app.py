import random
import streamlit as st
from schemas.search import SearchResult
import templates

def mock_search_results():
    return [
        SearchResult(
            title=f"Article #{i+1}",
            page_content="Lorem Ipsum fdskfls " * 50,
            link="https://google.com",
        ) for i in range(10)
    ], [f"tag{i}" for i in range(10)]

def main():
    st.set_page_config(page_title='AI-Powered Search Engine')
    st.write(templates.load_css(), unsafe_allow_html=True)
    st.title('AI-Powered Search')
    search = st.text_input('Enter search words:')
    if search:
        results, tags = mock_search_results()
        # show number of results and time taken
        st.write(templates.number_of_results(len(results), random.random()),
                 unsafe_allow_html=True)
        # render popular tags as filters
        st.write(templates.tag_boxes(search, tags, ''),
                 unsafe_allow_html=True)
        # search results
        for i, result in enumerate(results):
            st.write(
                templates.search_result(
                    i=i,
                    url=result.link,
                    title=result.title,
                    highlights=result.page_content), unsafe_allow_html=True)
            st.write(templates.tag_boxes(search, tags[:2], ''),
                     unsafe_allow_html=True)
if __name__ == '__main__':
    main()