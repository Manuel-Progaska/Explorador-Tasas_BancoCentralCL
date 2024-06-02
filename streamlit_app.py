import streamlit as st
import pandas as pd
from main import BC_Data


## FUNCIONES

@st.cache_data
def tasas(nombre:str, start:str=None, end:str=None) -> pd.DataFrame:

    # datos banco central
    bc = BC_Data()

    if nombre == 'Swap Camara CLP':

        df: pd.DataFrame = bc.tasa_swap_clp(start=start, end=end)

        return df


st.title('Explorador de Tasas Banco Central Chile')

# tasas
df : pd.DataFrame = tasas(nombre='Swap Camara CLP')
st.dataframe(df)