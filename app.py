import streamlit as st
import pandas as pd
from function import scraping_bdm

st.set_page_config(
    page_title="Streamlit App",
    page_icon="🧊",
    layout="wide",
)

# Champs de saisie de text pour les mots clef avec un bouton de validation
# scrapper en fonction de la recherche les artciles surl e site BDM
# Permettre à l'applidation de téélcharger les données en csv

st.title('Super Scrappeur BDM')

search = st.text_input('Recherche')

if st.button('Valider'):
    st.write('Vous avez choisi', search)

    results_dict = {}

    for index_page in range(1, 2): 
        url = f'https://www.blogdumoderateur.com/page/{str(index_page)}/'

        search_clean = search.replace(' ', '+')
        url_search = url + '?s=' + search_clean

        dict_page = scraping_bdm(url_search)
        results_dict.update(dict_page)

    df = pd.DataFrame(results_dict).T
    st.write(df)

    file_name = search.replace(' ', '_') + '.csv'

    st.download_button(
        label="Télécharger les données",
        data=df.to_csv().encode('utf-8'),
        file_name=file_name,
        mime='text/csv'
    )
