import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from functools import partial
from main import BC_Data

# page confict
st.set_page_config(layout="wide")
st.markdown('# EXPLORADOR DE TASAS BANCO CENTRAL CHILE')
col1, col2 = st.columns(2)
with col1:
    st.date_input('Inicio',key='start')
with col2:
    st.date_input('Fin',key='end')


# incialize BC_Data
bc = BC_Data()

## FUNCTIONS
@st.cache_data
def swaps_cl() -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    
    
    df: pd.DataFrame = bc.load_type(type='SWAP_CLP')
    
    return df

## DATOS
swp_cl = swaps_cl() 

## === OPTION MENU ===

with st.sidebar:
    selectted = option_menu(
        menu_title=None,
        options=['Swap CLP', 'SWAP UF'],
        icons=['database-fill', 'database-fill'],
        orientation='vertical',
        default_index=0
    )

## === SWAP CLP ===

if selectted == 'Swap CLP':    
    # page
    st.header('Tasas Históricas SPC-CLP')
    st.dataframe(swp_cl, use_container_width=True, hide_index=True)
