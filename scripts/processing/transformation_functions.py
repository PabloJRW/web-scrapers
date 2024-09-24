import os
import re
import numpy as np
import pandas as pd
from datetime import datetime
import unicodedata


def estandarizar_marcas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función estandariza los nombres de marcas en una columna de un DataFrame de pandas
    según un diccionario de reemplazos proporcionado. Los nombres de marcas en la columna se
    reemplazan con claves específicas del diccionario si se encuentran las variantes especificadas.

    Parameters:
    - df: pd.DataFrame
        DataFrame que debe contener una columna llamada 'Nombre' con los nombres de las marcas.

    Retorna:
    - pd.DataFrame
        Un DataFrame con la columna 'Nombre' actualizada con las marcas estandarizadas.
    """

    reemplazos_marcas = {
        'Hyundai': ['hyudani'],
        'Porsche': ['porche'],
        'Mercedes-Benz': ['mercedes']
    }

    # Iterar sobre el diccionario de reemplazos
    for clave, valores in reemplazos_marcas.items():
        for valor in valores:
            # Reemplaza cada variante en la columna con la marca estandarizada
            df['nombre'] = df['nombre'].str.replace(valor.lower(), clave, case=False, regex=False)
            
    return df



def extraer_marcas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función extrae las marcas de autos y las agrega a una nueva columna en el DataFrame.

    Parameters:
    - df: pd.DataFrame
        DataFrame que debe contener una columna llamada 'Nombre' con los nombres de los autos.

    Retorna:
    - pd.DataFrame
        DataFrame con una nueva columna llamada 'marca' que contiene la marca extraída.
    """
    # Lista de marcas de autos
    lista_marcas = [
        "acura", "alfa romeo", "aston martin", "audi", "bentley", "bmw", "bugatti", "buick",
        "cadillac", "chevrolet", "chrysler", "citroën", "dacia", "daewoo", "daihatsu", "dodge",
        "ferrari", "fiat", "ford", "geely", "genesis", "gmc", "honda", "hummer", "hyundai", "infiniti",
        "isuzu", "jaguar", "jeep", "kia", "koenigsegg", "lamborghini", "lancia", "land rover",
        "lexus", "lincoln", "lotus", "mahindra", "maserati", "maybach", "mazda", "mclaren", "mercedes-benz",
        "mercury", "mg", "mini", "mitsubishi", "morgan", "nissan", "opel", "pagani", "peugeot",
        "plymouth", "polestar", "pontiac", "porsche", "ram", "renault", "rolls-royce", "saab",
        "seat", "škoda", "smart", "subaru", "suzuki", "tata", "tesla", "toyota", "volkswagen",
        "volvo", "wiesmann", "zotye", "byd", "chery", "jac", "ssangyong", "great wall", "fisker", "rivian", "lucid", "vinfast"
    ]

    def encontrar_marca(texto):
        texto = texto.lower()
        for marca in lista_marcas:
            patron = r'\b' + re.escape(marca) + r'\b'
            if re.search(patron, texto):
                return marca
        return "Desconocida"  # Retorna un valor por defecto si no se encuentra ninguna marca

    df['marca'] = df['nombre'].apply(encontrar_marca)
    return df



def extraer_anios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función extrae los años del modelo de los autos de una columna de nombres de autos
    y los agrega como una nueva columna en el DataFrame.

    Parameters:
    - df: pd.DataFrame
        DataFrame que debe contener una columna llamada 'Nombre' con los nombres de los autos.

    Retorna:
    - pd.DataFrame
        Un DataFrame con una nueva columna llamada 'anio' que contiene los años extraídos.
    """

    # Lista de años posibles
    lista_anios = np.arange(1990, datetime.now().year + 1)
    
    def encontrar_anio(nombre):
        for anio in lista_anios:
            if str(anio) in nombre:
                return anio
        return np.nan  # Retorna NaN si no se encuentra un año

    # Aplicar la función a cada fila de la columna 'Nombre'
    df['anio'] = df['nombre'].apply(encontrar_anio)
    
    return df


def extraer_modelos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función extrae los modelos de autos de una columna de nombres de autos,
    utilizando las columnas de marca y año como referencia.

    Parameters:
    - df: pd.DataFrame
        DataFrame que debe contener las columnas 'Nombre', 'marca' y 'anio'.

    Retorna:
    - pd.DataFrame
        Un DataFrame con una nueva columna llamada 'modelo' que contiene los modelos extraídos.
    """

    def encontrar_modelos(fila):
        nombre_auto = fila['nombre']
        marca = fila['marca']
        anio = fila['anio']
        
        # Encontrar la posición de la marca y el año en el texto
        start_index = nombre_auto.lower().find(marca.lower()) + len(marca)
        end_index = nombre_auto.find(str(anio))

        if start_index != -1 and end_index != -1 and end_index > start_index:
            # Extraer el texto entre la marca y el año como modelo
            modelo = nombre_auto[start_index:end_index].strip()
            return modelo
        return ""  # Retorna cadena vacía si no se encuentra modelo

    # Aplicar la función para extraer modelo a cada fila
    df['modelo'] = df.apply(encontrar_modelos, axis=1)
    
    return df


def remover_textos(df:pd.DataFrame) -> pd.DataFrame:
    """
    Esta función remueve textos indeseados como: 'full extra', etc, de los modelos de autos.

    Parameters:
    - df: pd.DataFrame
        Dataframe que debe contener la columna 'modelo'.
    
    Retorna:
    - pd.Series
        Una serie con los modelos.
    """

    # Lista de textos a eliminar
    textos_a_eliminar = ['full', 'xtra', 'extra', 'extras', 'full extra', 'full extras', 'full xtra', 'hatchback', 'negociable', 'mercedes']

    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(texto) for texto in textos_a_eliminar) + r')\b', re.IGNORECASE)
    df['modelo'] = df['modelo'].apply(lambda x: pattern.sub('', str(x)).strip())

    return df


def transformar_sport_edition(df:pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el texto 'Sport Edition' a 'SE'.

    Parameters:
    - df: pd.DataFrame
        Dataframe que debe contener la columna 'modelo'.

    Retorna:
    - pd.DataFrame
        Una serie con los modelos.
    """

    pattern = re.compile(r'\bsport[\s-]*edition\b', re.IGNORECASE)
    df['modelo'] = df['modelo'].apply(lambda x: pattern.sub('SE', str(x)))

    return df


def estandarizar_modelos(df:pd.DataFrame):
    """
    Estandariza los modelos, reemplazando los textos mal digitados.

    Parameters:
    - df: pd.DataFrame
        Dataframe que debe contener la columna 'modelo'.

    Retorna:
    - pd.Dataframe
        Una serie con los modelos.
    """
    reemplazos_modelos = {'X-Trail': ['extrail','xtrail','X-trail'], 'CRV':['Crv','cr-v'], 'CX-5':['Cx-5','cx5'], 'Rio':['RIO'], 'CX-9':['cx9'],
              'Pick Up':['pik up']}
    
    # Iterar sobre el diccionario de reemplazos
    for clave, valores in reemplazos_modelos.items():
        for valor in valores:
            # Reemplaza cada valor en la columna temporal en minúsculas
            df['modelo'] = df['modelo'].str.replace(rf'{valor}', clave, case=False, regex=False)

    return df


def normalizar_valores_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los valores de las columnas de un DataFrame.
    Convierte los valores de tipo texto a minúsculas y elimina las tildes.

    Parameters:
    - df: pd.DataFrame
        El DataFrame cuyos valores se normalizarán.

    Retorna:
    - pd.DataFrame
        El DataFrame con los valores de las columnas de texto normalizados.
    """
    def remover_tildes(texto):
        if isinstance(texto, str):
            texto_normalizado = unicodedata.normalize('NFD', texto)
            return ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn').lower()
        return texto  # Si no es string, devolver el valor original

    # Aplicar la normalización solo a las columnas de tipo 'object' (texto)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(remover_tildes)
    
    return df


def transformar_anio(df:pd.DataFrame) -> pd.DataFrame:
    """Convierte el año a un objeto date representando el primer día del año"""
    df['anio'] = pd.to_datetime(df['anio'].astype(str) + '-01-01').dt.date
    return df


def transformar_precios(df: pd.Series) -> pd.Series:
    """
    Convierte el precio a tipo int.

    Parameters:
    - df: pd.DataFrame
        Dataframe que debe contener la columna 'Precio'.
    
    Retorna:
    - pd.Dataframe
        Dataframe con la columna 'precio' en tipo 'int'.
    """
    df['precio'] = df['precio'].str.replace('$','').str.replace(',','')
    df['precio'] = df['precio'].astype(int)

    return df


def selector_columnas(df:pd.DataFrame) -> pd.DataFrame:
    mis_variables = ['marca','modelo','anio','carroceria','traccion','combustible','transmision',
                     'asientos','color','kilometraje','verificacion','precio']
    df = df[mis_variables].copy()

    return df       