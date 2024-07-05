import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime as dt
from functools import partial
from main import BC_Data

# === PAGE CONFICT ===
st.set_page_config(
    layout="wide", 
    initial_sidebar_state='expanded', 
    page_title='Explorador Banco Central',

    )

# === BC_Data ===
bc = BC_Data()

# === FUNCTIONS ===
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
    

## === LAYOUT ===

# --- sidebar ---
# image
st.sidebar.image('assets/images/BC_LOGO.png')

# menu
with st.sidebar:
    selectted = option_menu(
        menu_title=None,
        options=['Swap Promedio Camara', 'TPM & Gobierno'],
        icons=['database-fill', 'database-fill'],
        orientation='vertical',
        default_index=0
    )

# dates
st.sidebar.date_input('Inicio',key='start', format='YYYY-MM-DD', value=dt.datetime.now() - dt.timedelta(31))
st.sidebar.date_input('Fin',key='end', format='YYYY-MM-DD', value=dt.datetime.now() - dt.timedelta(1))
start_ = str(st.session_state['start'])
end_ = str(st.session_state['end'])

# created by
st.sidebar.markdown('Created by: [`Manuel Progaska`](https://cl.linkedin.com/in/manuel-progaska-concha-98b304135)')


## === SWAPS ===

if selectted == 'Swap Promedio Camara':
    
    selectted_swp = option_menu(
        menu_title=None,
        options=['SPC CLP', 'SPC UF'],
        icons=['database-fill', 'database-fill'],
        orientation='horizontal',
        default_index=0
    )
    
    if selectted_swp == 'SPC CLP':   
        # --- page ---
        # data
        df_data : pd.DataFrame = data(type='SWAP_CLP', start=start_, end=end_)
        df_data = df_data[(df_data != 'NaN').any(axis=1)]
        df_data = df_data.astype(float).round(4)
        
        #data metrics
        df_aux : pd.DataFrame = df_data
        df_aux.index = df_aux.index.astype(str)
        df_aux = df_aux[df_aux.index.isin([start_, end_])]
        df_aux.fillna('-', inplace=True)
        
        #metrics
        st.markdown(f'### Tasas al {end_}')
        st.markdown(' ')
        first_col, second_col, third_col, fourth_col = st.columns(4)

        with first_col:
            #st.metric(label='SPC 90d',value=f'{df_aux.loc[end_,'SWP_CLP_90D']}',delta='', delta_color='normal')
            st.metric(label='SPC 180d',value=f'{df_aux.loc[end_,"SWP_CLP_180D"]}',delta='6.0%', delta_color='normal')

        with second_col:
            st.metric(label='SPC 360d',value=f'{df_aux.loc[end_,'SWP_CLP_360D']}',delta='6.0%', delta_color='normal')
            st.metric(label='SPC 2Y',value=f'{df_aux.loc[end_,'SWP_CLP_02Y']}',delta='6.0%', delta_color='normal')

        with third_col:
            st.metric(label='SPC 3Y',value=f'{df_aux.loc[end_,'SWP_CLP_03Y']}',delta='6.0%', delta_color='normal')
            st.metric(label='SPC 4Y',value=f'{df_aux.loc[end_,'SWP_CLP_04Y']}',delta='6.0%', delta_color='normal')
            
        with fourth_col:
            st.metric(label='SPC 5Y',value=f'{df_aux.loc[end_,'SWP_CLP_05Y']}',delta='6.0%', delta_color='normal')
            st.metric(label='SPC 10Y',value=f'{df_aux.loc[end_,'SWP_CLP_10Y']}',delta='6.0%', delta_color='normal')
        
        # header
        st.markdown('---')
        st.markdown('### Data histórica SPC-CLP')
        st.write(start_, end_)

        # table    
        st.dataframe(df_data, key='data_swp_cl', use_container_width=True)
        
        


    
