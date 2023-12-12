import streamlit as st

from function import clear_articles, get_all_articles_from_db

st.title('LDLC - mes articles')

if st.button('Supprimer tous les articles'):
    clear_articles()
    st.toast('Suppression effectuée', icon='👍')

articles = get_all_articles_from_db()

st.write(articles)