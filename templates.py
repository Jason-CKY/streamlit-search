import urllib
import streamlit as st
from schemas.search import PaginationButton

def load_css() -> str:
    """ Return all css styles. """
    common_tag_css = """
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: .15rem .40rem;
                position: relative;
                text-decoration: none;
                font-size: 95%;
                border-radius: 5px;
                margin-right: .5rem;
                margin-top: .4rem;
                margin-bottom: .5rem;
    """
    return f"""
        <style>
            #tags {{
                {common_tag_css}
                color: rgb(88, 88, 88);
                border-width: 0px;
                background-color: rgb(240, 242, 246);
            }}
            #tags:hover {{
                color: black;
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
            #active-tag {{
                {common_tag_css}
                color: rgb(246, 51, 102);
                border-width: 1px;
                border-style: solid;
                border-color: rgb(246, 51, 102);
            }}
            #active-tag:hover {{
                color: black;
                border-color: black;
                background-color: rgb(240, 242, 246);
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
        </style>
    """

def number_of_results(total_hits: int, duration: float) -> str:
    """ HTML scripts to display number of results and duration. """
    return f"""
        <div style="color:grey;font-size:95%;">
            {total_hits} results ({duration:.2f} seconds)
        </div><br>
    """

def search_result(i: int, url: str, title: str, highlights: str) -> str:
    """ HTML scripts to display search results. """
    return f"""
        <div style="font-size:120%;">
            {i + 1}.
            <a href="{url}">
                {title}
            </a>
        </div>
        <div style="font-size:95%;">
            <div style="color:grey;font-size:95%;">
                {url[:90] + '...' if len(url) > 100 else url}
            </div>
            {highlights}
        </div>
    """

def pagination_on_click(search, page):
    st.query_params["search"] = search
    st.query_params["page"] = page

def pagination(total_pages: int, search: str, current_page: int) -> str:
    """ HTML scripts to render pagination buttons. """
    # avoid invalid page number (<=0)
    if (current_page - 5) > 0:
        start_from = current_page - 5
    else:
        start_from = 1

    buttons = []
    # st.columns()
    if current_page != 1:
        buttons += [
            PaginationButton(text="<<First", onClick=pagination_on_click, args=[search, 1]),
            PaginationButton(text="<<Previous", onClick=pagination_on_click, args=[search, current_page - 1]),
        ]
        
    for i in range(start_from, min(total_pages + 1, start_from + 10)):
        if i == current_page:
            buttons.append(PaginationButton(text=f"{current_page}", onClick=lambda x: x, disabled = True, args=[]))
        else:
            buttons.append(PaginationButton(text=f"{i}", onClick=pagination_on_click, args=[search, i]))

    if current_page != total_pages:
        buttons.append(PaginationButton(text="Next>", onClick=pagination_on_click, args=[search, current_page + 1]))

    for column, button in zip(st.columns([1 for _ in range(len(buttons))]), buttons):
        with column:
            st.button(button.text, disabled=button.disabled, on_click=button.onClick,
                      args=button.args)
    st.markdown("""
        <style>
            div[data-testid="column"] {
                width: fit-content !important;
                flex: unset;
            }
            div[data-testid="column"] * {
                width: fit-content !important;
            }
        </style>
    """, unsafe_allow_html=True)

def tag_boxes(search: str, tags: list, active_tag: str) -> str:
    """ HTML scripts to render tag boxes. """
    html = ''
    search = urllib.parse.quote(search)
    for tag in tags:
        if tag != active_tag:
            html += f"""
            <a id="tags" href="?search={search}&tags={tag}">
                {tag.replace('-', ' ')}
            </a>
            """
        else:
            html += f"""
            <a id="active-tag" href="?search={search}">
                {tag.replace('-', ' ')}
            </a>
            """

    html += '<br><br>'
    return html