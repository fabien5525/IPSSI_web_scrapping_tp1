import streamlit as st

from function import get_all_boursorama_from_db, clear_boursorama

st.title('LDLC - mes articles')

if st.button('Supprimer tous les articles'):
    clear_boursorama()
    st.toast('Suppression effectuée', icon='👍')

boursoramas = get_all_boursorama_from_db()

st.write(boursoramas)