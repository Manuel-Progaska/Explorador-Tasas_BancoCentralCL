import streamlit as st
import pandas as pd
from main import BC_Data


st.title('Explorador de Tasas Banco Central')

## FUNCIONES

@st.cache
def tasas(nombre:str, start:str=None, end:str=None) -> pd.DataFrame:

    # datos banco central
    bc = BC_Data()

    if nombre == 'Swap Camara CLP':

        df: pd.DataFrame = bc.tasa_swap_clp(start=start, end=end)

        return df

# tasas
df : pd.DataFrame = tasas(nombre='Swap Camara CLP')
st.write(df)