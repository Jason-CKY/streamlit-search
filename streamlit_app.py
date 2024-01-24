import streamlit as st
from schemas.search import SearchResult

def mock_search_results():
    return [
        SearchResult(
            title=f"Article #{i+1}",
            page_content="Lorem Ipsum fdskfls " * 50,
            link="https://google.com",
        ) for i in range(10)
    ]

def main():
    st.set_page_config(page_title='AI-Powered Search Engine')
    st.title('AI-Powered Search')
    search = st.text_input('Enter search words:')
    if search:
        results = mock_search_results()

if __name__ == '__main__':
    main()