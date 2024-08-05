import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import math
import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
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
    
def start_end(df:pd.DataFrame) -> None:
    
    # columnas
    cols : list = list(df.columns)
    
    # loop
    dct : dict = {}
    for col in cols:
        end = df[col].iloc[0]
        start = df[col].iloc[-1]
        delta = np.round((end/start - 1)*100,2)
        #delta = round(delta,3)
        if end > start:
            tag = '+'
        else:
            tag = '-'
        dct[col] = [start, end, delta, tag]
    
    return dct
    
    

## === LAYOUT ===

# --- sidebar ---
# image
st.sidebar.image('assets/images/BC_LOGO.png')

# title
st.sidebar.markdown('''
                    # Explorador Banco Central Chile
                    --- 
                    ''')

# menu
with st.sidebar:
    selectted = option_menu(
        menu_title=None,
        options=['Tasas', 'Inflación'],
        icons=['database-fill', 'bar-chart-fill'],
        orientation='vertical',
        default_index=0
    )

# dates
st.sidebar.date_input('Inicio',key='start', format='YYYY-MM-DD', value=dt.datetime.now() - dt.timedelta(365))
st.sidebar.date_input('Fin',key='end', format='YYYY-MM-DD', value=dt.datetime.now() - dt.timedelta(2))
start_ = str(st.session_state['start'])
end_ = str(st.session_state['end'])

# created by
st.sidebar.markdown('Created by: [`Manuel Progaska`](https://cl.linkedin.com/in/manuel-progaska-concha-98b304135)')


## === DATA ===

if selectted == 'Tasas':
    
    selectted_swp = option_menu(
        menu_title=None,
        options=['SPC CLP', 'SPC UF' ,'Gobierno', 'Monedas'],
        icons=['database-fill', 'database-fill','database-fill','database-fill','database-fill'],
        orientation='horizontal',
        default_index=1
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
        st.markdown(f'### Swap Promedio Camara CLP: {end_}')
        st.markdown(' ')
        deltas = start_end(df=df_data)
        first_col, second_col, third_col, fourth_col = st.columns(4)

        with first_col:
            st.metric(label='SPC 90d',value=f'{deltas["SWP_CLP_90D"][1]}',delta=f'{deltas["SWP_CLP_90D"][2]}%', delta_color='inverse')
            st.metric(label='SPC 180d',value=f'{deltas["SWP_CLP_180D"][1]}',delta=f'{deltas["SWP_CLP_180D"][2]}%', delta_color='inverse')

        with second_col:
            st.metric(label='SPC 360d',value=f'{deltas["SWP_CLP_360D"][1]}',delta=f'{deltas["SWP_CLP_360D"][2]}%', delta_color='inverse')
            st.metric(label='SPC 2Y',value=f'{deltas["SWP_CLP_02Y"][1]}',delta=f'{deltas["SWP_CLP_02Y"][2]}%', delta_color='inverse')

        with third_col:
            st.metric(label='SPC 3Y',value=f'{deltas["SWP_CLP_03Y"][1]}',delta=f'{deltas["SWP_CLP_03Y"][2]}%', delta_color='inverse')
            st.metric(label='SPC 4Y',value=f'{deltas["SWP_CLP_04Y"][1]}',delta=f'{deltas["SWP_CLP_04Y"][2]}%', delta_color='inverse')
            
        with fourth_col:
            st.metric(label='PC 5Y',value=f'{deltas["SWP_CLP_05Y"][1]}',delta=f'{deltas["SWP_CLP_05Y"][2]}%', delta_color='inverse')
            st.metric(label='PC 10Y',value=f'{deltas["SWP_CLP_10Y"][1]}',delta=f'{deltas["SWP_CLP_10Y"][2]}%', delta_color='inverse')
        
        # header
        st.markdown('---')
        st.markdown('### Data histórica SPC-CLP')
        st.write(f'Desde {start_} hasta {end_}')

        # line chart
        st.multiselect('Curvas', tuple(df_data.columns), default=tuple(df_data.columns),key='plot_filter')
        df_linechart : pd.DataFrame = df_data[list(st.session_state['plot_filter'])]
        fig = px.line(df_linechart, x=df_linechart.index, y=list(df_linechart.columns))
        st.plotly_chart(fig)
        
        # table    
        st.dataframe(df_linechart, key='data_swp_cl', use_container_width=True)
        
        
    if selectted_swp == 'SPC UF':   
        # --- page ---
        # data
        df_data : pd.DataFrame = data(type='SWAP_UF', start=start_, end=end_)
        df_data = df_data[(df_data != 'NaN').any(axis=1)]
        df_data = df_data.astype(float).round(4)
        
        #data metrics
        df_aux : pd.DataFrame = df_data
        df_aux.index = df_aux.index.astype(str)
        df_aux = df_aux[df_aux.index.isin([start_, end_])]
        df_aux.fillna('-', inplace=True)
        
        #metrics
        st.markdown(f'### Swap Promedio Camara UF {end_}')
        st.markdown(' ')
        deltas = start_end(df=df_data)
        first_col, second_col, third_col = st.columns(3)


        with first_col:
            st.metric(label='SPC UF 1Y',value=f'{deltas["SWP_UF_01Y"][1]}',delta=f'{deltas["SWP_UF_01Y"][2]}%', delta_color='inverse')
            st.metric(label='SPC UF 2Y',value=f'{deltas["SWP_UF_02Y"][1]}',delta=f'{deltas["SWP_UF_02Y"][2]}%', delta_color='inverse')

        with second_col:
            st.metric(label='SPC UF 3Y',value=f'{deltas["SWP_UF_03Y"][1]}',delta=f'{deltas["SWP_UF_03Y"][2]}%', delta_color='inverse')
            st.metric(label='SPC UF 4Y',value=f'{deltas["SWP_UF_04Y"][1]}',delta=f'{deltas["SWP_UF_04Y"][2]}%', delta_color='inverse')
            
        with third_col:
            st.metric(label='SPC UF 5Y',value=f'{deltas["SWP_UF_05Y"][1]}',delta=f'{deltas["SWP_UF_05Y"][2]}%', delta_color='inverse')
            st.metric(label='SPC UF 10Y',value=f'{deltas["SWP_UF_10Y"][1]}',delta=f'{deltas["SWP_UF_10Y"][2]}%', delta_color='inverse')
        
        # header
        st.markdown('---')
        st.markdown('### Data histórica SPC-UF')
        st.write(f'Desde {start_} hasta {end_}')

        # line chart
        st.multiselect('Curvas', tuple(df_data.columns), default=tuple(df_data.columns),key='plot_filter')
        df_linechart : pd.DataFrame = df_data[list(st.session_state['plot_filter'])]
        fig = px.line(df_linechart, x=df_linechart.index, y=list(df_linechart.columns))
        st.plotly_chart(fig)
        
        # table    
        st.dataframe(df_linechart, key='data_UF_cl', use_container_width=True)
      

    if selectted_swp == 'Gobierno':
        # --- page ---
        # data uf
        df_data_uf : pd.DataFrame = data(type='GOVT_UF', start=start_, end=end_)
        df_data_uf = df_data_uf[(df_data_uf != 'NaN').any(axis=1)]
        df_data_uf = df_data_uf.astype(float).round(4)
        
        # data clp
        df_data_clp : pd.DataFrame = data(type='GOVT_CLP', start=start_, end=end_)
        df_data_clp = df_data_clp[(df_data_clp != 'NaN').any(axis=1)]
        df_data_clp = df_data_clp.astype(float).round(4)
        
        st.markdown('### Bonos de Gobierno en UF')
        first_col, second_col = st.columns(2)
        
        
        with first_col:
            st.dataframe(df_data_uf)
            st.dataframe(df_data_clp)
        
        with second_col:
            data_line_chart = df_data_uf.fillna(method='ffill')
            fig = px.line(data_line_chart, x=data_line_chart.index, y=list(data_line_chart.columns))
            st.plotly_chart(fig)
    
