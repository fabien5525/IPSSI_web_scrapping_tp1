import streamlit as st

st.title("MyAnimeList Fast API")

st.markdown(
    """
    <iframe src="http://localhost:8000/redoc#operation/" width="100%" height="500px"></iframe>
    """,
    unsafe_allow_html=True
)