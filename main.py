import bcchapi
import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass


## CLIENTE BANCO CENTRAL

@dataclass
class Cliente_BC:
    """Conexión a la API del Banco Central de Chile """

    siete : bcchapi.Siete = None # Objeto principal de la librería bcchapi
    
    
    def __post_init__(self) -> None:
        
        # conexión a api
        self.connect()
        
        # series
        self.series()

        
    def connect(self) -> None:
        """ """
        
        self.siete =bcchapi.Siete(file=Path.cwd() /'assets' /'files' / 'credenciales.txt')
    
    
    def series(self) -> None:
        """ """
        
        self.series = pd.DataFrame = pd.read_excel(Path.cwd() /'assets' /'files' / 'series.xlsx')
    




## BANCO CENTRAL DATA

@dataclass
class BC_Data(Cliente_BC):
    """
    Descarga datos desde la la base de datos del Banco Central

    Args:
        Cliente_BC (class): clase padre que se conecta a la API del Banco Central
    """
    
    spc_clp : pd.DataFrame = None
    spc_uf : pd.DataFrame = None
    
    
    def tasa_swap_clp(self, start: str = None, end: str = None) -> pd.DataFrame:
        
        self.spc_clp = self.siete.cuadro(
            
            series = [
                        'F022.SPC.TIN.AN10.NO.Z.D',
                        'F022.SPC.TIN.AN05.NO.Z.D',
                        'F022.SPC.TIN.AN04.NO.Z.D',
                        'F022.SPC.TIN.AN03.NO.Z.D',
                        'F022.SPC.TIN.AN02.NO.Z.D',
                        'F022.SPC.TPR.D360.NO.Z.D',
                        'F022.SPC.TPR.D180.NO.Z.D',
                        'F022.SPC.TPR.D090.NO.Z.D'
                
                     ],
            nombres=[
                        '10Y',
                        '5Y',
                        '4Y',
                        '3Y',
                        '2Y',
                        '360D',
                        '180D',
                        '90D'
                    ],
            desde= start,
            hasta=end,
            observado='max'
            
        )
        
        df : pd.DataFrame = self.spc_clp
        
        return df
        
        
    
    def tasa_swap_uf(self, start: str = None, end: str = None) -> pd.DataFrame:
        
        self.spc_clp = self.siete.cuadro(
            
            series = [
                        'F022.SPC.TIN.AN20.UF.Z.D',
                        'F022.SPC.TIN.AN10.UF.Z.D',
                        'F022.SPC.TIN.AN05.UF.Z.D',
                        'F022.SPC.TIN.AN04.UF.Z.D',
                        'F022.SPC.TIN.AN03.UF.Z.D',
                        'F022.SPC.TIN.AN02.UF.Z.D',
                        'F022.SPC.TIN.AN01.UF.Z.D'
                
                     ],
            nombres=[
                        '20Y',
                        '10Y',
                        '5Y',
                        '4Y',
                        '3Y',
                        '2Y',
                        '1Y'
                    ],
            desde= start,
            hasta=end,
            observado='max'
            
        )
        
        df : pd.DataFrame = self.spc_clp
        
        return df
        


    def bcu(self, start: str = None, end: str = None) -> pd.DataFrame:
        """
        Tasas de interés de los bonos licitados por el BCCh, en UF (BCU) (porcentaje) 

        Args:
            start (str, optional): _description_. Defaults to None.
            end (str, optional): _description_. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        
        self.spc_clp = self.siete.cuadro(
            
            series = [
                        'F022.BCU.TIN.AN20.UF.Z.M',
                        'F022.BCU.TIN.AN10.UF.Z.M',
                        'F022.BCU.TIN.AN05.UF.Z.M',
                        'F022.BCU.TIN.AN02.UF.Z.M'
                
                     ],
            nombres=[
                        '20Y',
                        '10Y',
                        '5Y',
                        '2Y'
                    ],
            desde= start,
            hasta=end,
            observado='max'
            
        )
        
        df : pd.DataFrame = self.spc_clp
        
        return df



    def tasas_uf(self, start: str = None, end: str = None) -> pd.DataFrame:
        """Tasas de interés mercado secundario, bonos, en UF (porcentaje) """

        self.spc_clp = self.siete.cuadro(
                    
                    series = [
                               'F022.BUF.TIS.AN30.UF.Z.D',
                               'F022.BUF.TIS.AN20.UF.Z.D',
                               'F022.BUF.TIS.AN10.UF.Z.D',
                               'F022.BUF.TIS.AN05.UF.Z.D',
                               'F022.BUF.TIS.AN02.UF.Z.D',
                               'F022.BUF.TIS.AN01.UF.Z.D'
                        
                            ],
                    nombres=[
                                '30Y',
                                '20Y',
                                '10Y',
                                '5Y',
                                '2Y',
                                '1Y'
                            ],
                    desde= start,
                    hasta=end,
                    observado='max'
                    
                )
                
        df : pd.DataFrame = self.spc_clp
        
        return df



    def tasas_clp(self, start: str = None, end: str = None) -> pd.DataFrame:
        """Tasas de interés mercado secundario, bonos, en UF (porcentaje) """

        self.spc_clp = self.siete.cuadro(
                    
                    series = [
                                'F022.BCLP.TIS.AN10.NO.Z.D',
                                'F022.BCLP.TIS.AN05.NO.Z.D',
                                'F022.BCLP.TIS.AN02.NO.Z.D',
                                'F022.BCLP.TIS.AN01.NO.Z.D'
                        
                            ],
                    nombres=[
                                '10Y',
                                '5Y',
                                '2Y',
                                '1Y'
                            ],
                    desde= start,
                    hasta=end,
                    observado='max'
                    
                )
                
        df : pd.DataFrame = self.spc_clp
        
        return df
    

def main() -> None:
       
    bc = BC_Data()
    swp = bc.tasas_clp()
    
    return swp
        
        
def tasas(nombre:str, start:str=None, end:str=None) -> pd.DataFrame:

    # datos banco central
    bc = BC_Data()

    if nombre == 'Swap Camara CLP':

        df: pd.DataFrame = bc.tasa_swap_clp(start=start, end=end)

        return df

df : pd.DataFrame = tasas(nombre='Swap Camara CLP')
print(df)