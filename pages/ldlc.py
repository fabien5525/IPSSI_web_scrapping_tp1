from function import save_ldlc_data_to_db, scraping_ldlc
import streamlit as st
import pandas as pd
from urllib.parse import quote
from selenium import webdriver

st.title('LDLC')

url = 'https://www.ldlc.com/recherche/'

search = st.text_input('Recherche', value='')
count_page = st.number_input('Nombre de page', value=1, min_value=1, max_value=10)

if st.button('Rechercher'):
    with st.spinner('Recherche en cours...'):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        search_clean = quote(search)

        data = {}

        for i in range(count_page):

            if i == 0:
                page_str = ''
            else:
                page_str = '/page' + str(i + 1)
                
            url_complete = url + search_clean + page_str
            data.update(scraping_ldlc(driver, url_complete))

        driver.close()

        df = pd.DataFrame.from_dict(data, orient='index')
        st.write(df)

        st.download_button(
            label='Télécharger',
            data=df.to_csv().encode('utf-8'),
            file_name=search_clean + '.csv',
            mime='text/csv'
        )       
           
        st.toast('Recherche terminée', icon='👏')

        save_ldlc_data_to_db(df)
        st.toast('Enregistrement effectué', icon='👍')
    




        