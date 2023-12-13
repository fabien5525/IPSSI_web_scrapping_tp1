import streamlit as st
import os
import pandas as pd

st.title('Boursorama')

if st.button('Lancer la collecte'):
    with st.spinner('Collecte en cours...'):

        pwd = os.getcwd()

        if pwd[-7:] != 'spiders':
            os.chdir('WebCrawler')
            os.chdir('WebCrawler')
            os.chdir('spiders')

        if os.path.exists('boursorama.csv'):
            os.remove('boursorama.csv')

        os.system('scrapy crawl boursorama -o boursorama.csv')

        os.chdir('../../../')

        st.success('Collecte terminée')

        st.subheader('Résultats (CAC40) :')

        df = pd.read_csv('./WebCrawler/WebCrawler/spiders/boursorama.csv')

        st.write(df)
        