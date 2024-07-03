import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from functools import partial
from main import BC_Data

# page confict
st.set_page_config(layout="wide")


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

## LAYOUT

# sidebar menu
with st.sidebar:
    selectted = option_menu(
        menu_title='Tasas',
        options=['Swap CLP', 'SWAP UF']
    )

# sidebar
st.sidebar.title('Parametros')

# page
st.title('EXPLORADOR DE TASAS BANCO CENTRAL CHILE')
st.header('Tasas Históricas SPC-CLP')
st.dataframe(swp_cl, use_container_width=True, hide_index=True)
