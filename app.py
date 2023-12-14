import streamlit as st
import pandas as pd
from function import scraping_bdm
from dotenv import load_dotenv
import os

load_dotenv()


st.set_page_config(
    page_title="Streamlit App",
    page_icon="🧊",
    layout="wide",
)

# Champs de saisie de text pour les mots clef avec un bouton de validation
# scrapper en fonction de la recherche les artciles surl e site BDM
# Permettre à l'applidation de téélcharger les données en csv

st.title('Super Scrappeur BDM')

search = st.text_input('Recherche', placeholder='Adobe, web, IA, ...')
pages = st.slider('Nombre de pages', 1, 10, 1)

if st.button('Valider'):
    st.write('Vous avez choisi', search)

    with st.spinner('Chargement en cours...'):

        results_dict = {}

        for index_page in range(1, pages+1): 
            url = f'https://www.blogdumoderateur.com/page/{str(index_page)}/'

            search_clean = search.replace(' ', '+')
            url_search = url + '?s=' + search_clean

            try : 
                dict_page = scraping_bdm(url_search)
                results_dict.update(dict_page)
            except:
                break

        df = pd.DataFrame(results_dict).T
        st.write(df)

        file_name = search.replace(' ', '_') + '.csv'

        st.download_button(
            label="Télécharger les données",
            data=df.to_csv().encode('utf-8'),
            file_name=file_name,
            mime='text/csv'
        )

    st.snow()
    st.toast('Scraping terminé !', icon='🎉')

