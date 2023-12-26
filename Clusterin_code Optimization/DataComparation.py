# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 19:02:04 2023

@author: Fabian F
"""
import pandas as pd
from fuzzywuzzy import fuzz
import re

def clean_text(text):
    # Convertir a minúsculas y eliminar signos de puntuación
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def compare_dataframes(df1, df2):
    # Definir las columnas específicas para comparar
    columns_to_compare = ['Grave', 'Individual', 'Level', 'Orientation', 'Type', 'Sex', 'Age',
                           'Position', 'Pottery types', 'Other objects']

    # Crear un nuevo DataFrame para almacenar los resultados de comparación
    comparison_result = pd.DataFrame(columns=['Grave', 'Individual', 'Column', 'Row', 'SafarTombs', 'Breteron', 'Similarity'])

    # Iterar sobre las filas
    for index in range(len(df1)):
        # Verificar si los valores de "Grave" e "Individual" coinciden entre los dos DataFrames
        if df1.at[index, 'Grave'] == df2.at[index, 'Grave'] and df1.at[index, 'Individual'] == df2.at[index, 'Individual']:
            # Iterar sobre las columnas específicas
            for column in columns_to_compare:
                # Obtener los valores de las celdas correspondientes en ambas DataFrames
                value1 = clean_text(str(df1.at[index, column]))
                value2 = clean_text(str(df2.at[index, column]))

                # Calcular la similitud difusa entre los valores
                similarity = fuzz.ratio(value1, value2)

                # Agregar los resultados a la DataFrame de comparación si la similitud es inferior al 100%
                if similarity < 1000:
                    comparison_result = comparison_result.append({
                        'Grave': df1.at[index, 'Grave'],
                        'Individual': df1.at[index, 'Individual'],
                        'Column': column,
                        'Row': index,
                        'SafarTombs': value1,
                        'Breteron': value2,
                        'Similarity': similarity
                    }, ignore_index=True)

    return comparison_result

# Cargar DataFrames de ejemplo
df1 = pd.read_csv("SafarTombs.csv")
df2 = pd.read_csv("cleaned_sample.csv")

# Comparar DataFrames
result = compare_dataframes(df1, df2)

# Mostrar los resultados
print(result)
