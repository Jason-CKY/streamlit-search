import streamlit as st
import datetime

def sidebar():
    # Using object notation
    today = datetime.datetime.now()
    data_source = st.sidebar.selectbox(
        label = "Data source",
        options = ("Confluence (Policies & Circulars)",)
    )
    date_range = st.sidebar.date_input(
        label="Date range filter",
        value=(datetime.date(today.year, 1 if today.month - 1 == 0 else today.month, 1), today),
        min_value=datetime.date(today.year, 1, 1),
        max_value=datetime.date(today.year, 12, 31),
        format="MM.DD.YYYY",
    )
    st.session_state.search_params = {
        "data_source": data_source,
        "date_range": date_range
    }
