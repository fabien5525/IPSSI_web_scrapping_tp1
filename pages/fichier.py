import streamlit as st
import pandas as pd

st.title('Super Scrappeur BDM')
st.text('Visualier les données')

# check if the file exists (bdm.json)

file_path = 'bdm.json'

def cols(infos):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(infos['image'], width=200)

    with col2:
        st.write(infos['title'])
        st.write(infos['date'])
        st.write(infos['categorie'])

    with col3:
        st.write(infos['link'])

def table():
    with open(file_path, 'r') as f:
        df = pd.read_json(f).T
        
        for index, row in df.iterrows():
            st.divider()
            cols(row)

try:
    table()

except:
    st.error('Le fichier n\'a pas  été trouvé')