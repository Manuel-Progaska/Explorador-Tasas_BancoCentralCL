import streamlit as st
import pandas as pd
from main import BC_Data


bc = BC_Data()
df = bc.load_type(type='SWAP_CLP')

st.title('EXPLORADOR DE TASAS BANCO CENTRAL CHILE')
st.header('Tasa Swap Promedio Camara CLP')
st.dataframe(df, use_container_width=True)
