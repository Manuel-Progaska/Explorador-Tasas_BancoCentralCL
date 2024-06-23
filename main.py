import bcchapi
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
from functools import partial
from dotenv import dotenv_values


class BC_Data(bcchapi.webservice.Session):
    
    def __init__(self) -> None:
        
        # acceso a variables de entorno
        config : dotenv_values = dotenv_values('.env')
        
        # usuario
        self.user : str = config['bc_user']
        
        # clave
        self.pwd : str = config['bc_pwd']
        
        # inicialiar clase padre con credenciales 
        super().__init__(usr=self.user,pwd=self.pwd)
        
    
    def get_data(self, serie:str, name:str, start:str=None, end:str=None) -> pd.DataFrame:
        """_summary_

        Args:
            serie (str): _description_
            name (str): _description_
            start (str, optional): _description_. Defaults to None.
            end (str, optional): _description_. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        
        data = self.get(serie, first_date=start, last_date=end)
        valores = data.Series["Obs"]
        
        df : pd.DataFrame = pd.DataFrame(valores)
        df = df.rename(columns={'indexDateString': 'FECHA', 'value':name})
        df = df[['FECHA', name]]
        
        return df
    
    
    def get_series(self, type:str) -> dict:
        """_summary_

        Args:
            type (str): _description_

        Returns:
            dict: _description_
        """
        
        # conexión base de datos interna
        path: Path  = Path.cwd() / 'assets' /'database' / 'DATA.db'
        cnx: sqlite3 = sqlite3.connect(path)
        
        # series
        query: str = f'''
        SELECT * FROM DM_SERIES
        WHERE TYPE = '{type}'
        '''
        
        df: pd.DataFrame = pd.read_sql(sql=query, con=cnx)
        
        return df
    
    
    def load_type(self, type:str) -> pd.DataFrame:
        """_summary_

        Args:
            type (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
        
        # series
        df_series : pd.DataFrame = self.get_series(type=type)
        
        # data
        lst : list = []
        for i in range(len(df_series)):
            
           serie: str = df_series['SERIE'].iloc[i]
           name: str = df_series['NAME'].iloc[i]
           
           df_aux: pd.DataFrame = self.get_data(serie=serie, name=name)
           df_aux = df_aux.rename(columns={name:'VALOR'})
           df_aux['NAME'] = name
           df_aux = df_aux[['FECHA', 'NAME', 'VALOR']]
           lst.append(df_aux)
        
        df : pd.DataFrame = pd.concat(lst)
        pivot : pd.DataFrame = pd.pivot_table(df, index='FECHA', columns='NAME', values='VALOR', aggfunc='max')
        pivot = pivot.reset_index()
        
        return pivot
        
        
        
    
  
