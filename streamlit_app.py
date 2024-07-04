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
    df['FECHA'] = df['FECHA'].dt.date
    df.index = df['FECHA']
    df.drop('FECHA', inplace=True, axis=1)
    
    return df
    

## === OPTION MENU ===

with st.sidebar:
    selectted = option_menu(
        menu_title=None,
        options=['Swap CLP', 'Swap UF'],
        icons=['database-fill', 'database-fill'],
        orientation='vertical',
        default_index=0
    )

# dates
st.sidebar.date_input('Inicio',key='start', format='YYYY-MM-DD', value=dt.datetime.now() - dt.timedelta(1))
st.sidebar.date_input('Fin',key='end', format='YYYY-MM-DD')
start_ = str(st.session_state['start'])
end_ = str(st.session_state['end'])


## === SWAP CLP ===

if selectted == 'Swap CLP':    
    # --- page ---
    
    
    # header
    st.header('Tasas Históricas SPC-CLP')
    st.write(start_, end_)

    # data
    df_data : pd.DataFrame = data(type='SWAP_CLP', start=start_, end=end_)
    df_data = df_data[(df_data != 'NaN').any(axis=1)]
    df_data = df_data.astype(float).round(2,)
    st.dataframe(df_data, key='data_swp_cl')


    
