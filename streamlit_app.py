import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime as dt
from functools import partial
from main import BC_Data

# page confict
st.set_page_config(layout="wide")
st.markdown('# EXPLORADOR DE TASAS BANCO CENTRAL CHILE')

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

def data(type:str=None, start:str=None, end:str=None) -> pd.DataFrame:
    """_summary_

    Args:
        type (str, optional): _description_. Defaults to None.
        start (str, optional): _description_. Defaults to None.
        end (str, optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    
    df: pd.DataFrame = bc.load_type(type=type, start=start, end=end)
    
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
    # --- page ---
    
    # header
    st.header('Tasas Históricas SPC-CLP')
    
    # dates
    st.sidebar.date_input('Inicio',key='start')
    st.sidebar.date_input('Fin',key='end')
    start = str(st.session_state['start'])
    end = str(st.session_state['end'])
    
    # data
    df_data : pd.DataFrame = data(type='SWAP_CLP', start=start, end=end)
    st.dataframe(df_data, use_container_width=True, hide_index=True)
