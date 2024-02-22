# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 18:50:24 2023

@author: Fabian F
"""

import pandas as pd
import prince
import matplotlib.pyplot as plt
import seaborn as sns


############################# Level - Pottery #################################
def level_pottery():
    df = pd.read_csv('pottery_sample.csv',  usecols=lambda x: x != 'Unnamed: 0')
    
    # Manejar los valores NaN en la columna 'Level' antes de establecerla como índice
    df['Level'].fillna(df['Level'].mean(), inplace=True)
    
    df = df.set_index('Level')
    
    df = df.fillna(df.mean())
    
    if (df < 5).any().any():
        df = (df + 1) * 5
    
    ca = prince.CA(
        n_components=2,
        n_iter=10,
        copy=True,
        check_input=True,
        engine='sklearn',
        random_state=42
    )
    
    ca = ca.fit(df)
    
    print(ca.row_coordinates(df))
    print(ca.column_coordinates(df))
    
    
    
    # Crear una figura y un conjunto de subtramas
    fig, ax = plt.subplots()
    
    # Dibujar las coordenadas de las filas
    row_coords = ca.row_coordinates(df)
    ax.scatter(row_coords[0], row_coords[1], color='red', label='Level', s=1)  # Ajusta 's' para cambiar el tamaño de los puntos
    
    # Dibujar las coordenadas de las columnas
    col_coords = ca.column_coordinates(df)
    ax.scatter(col_coords[0], col_coords[1], color='blue', label='Pottery type', s=1)  # Ajusta 's' para cambiar el tamaño de los puntos
    
    # Añadir etiquetas a los puntos
    for i, (x, y) in enumerate(row_coords.iterrows()):
        ax.annotate(x, (y[0], y[1]), fontsize=3)
    for i, (x, y) in enumerate(col_coords.iterrows()):
        ax.annotate(x, (y[0], y[1]), fontsize=3)
        
    # Añadir una leyenda
    ax.legend()
    
    # Guardar el gráfico como un archivo PNG
    plt.savefig('Pottery_level_correspondence_analysis.png', dpi=2160)  # Ajusta 'dpi' para cambiar la resolución de la imagen
    
    # Mostrar el gráfico
    plt.show()
    
level_pottery()

############################# Overlap - Pottery #################################

df = pd.read_csv('pottery_overlap_sample.csv',  usecols=lambda x: x != 'Unnamed: 0')

# Eliminar las columnas donde todos los valores son cero
df = df.loc[:, (df != 0).any(axis=0)]

df = df.drop('Pottery_nan', axis=1)


df = df.astype(int)

df = df.set_index('Overlap')

df = df.sort_index(ascending=False)


plt.figure(figsize=(10,8))
sns.heatmap(df, annot=True, cmap='gist_gray')
# Guardar el gráfico como un archivo PNG
plt.savefig('Pottery_overlap_heatMap.png', dpi=2160)  # Ajusta 'dpi' para cambiar la resolución de la imagen

plt.show()

df = df.fillna(df.mean())

if (df < 5).any().any():
    df = (df + 1) * 5

ca = prince.CA(
    n_components=2,
    n_iter=10,
    copy=True,
    check_input=True,
    engine='sklearn',
    random_state=42
)

ca = ca.fit(df)

# Crear una figura y un conjunto de subtramas
fig, ax = plt.subplots()

# Dibujar las coordenadas de las filas
row_coords = ca.row_coordinates(df)
ax.scatter(row_coords[0], row_coords[1], color='red', label='Level', s=1)  # Ajusta 's' para cambiar el tamaño de los puntos

# Dibujar las coordenadas de las columnas
col_coords = ca.column_coordinates(df)
ax.scatter(col_coords[0], col_coords[1], color='blue', label='Pottery type', s=1)  # Ajusta 's' para cambiar el tamaño de los puntos

# Añadir etiquetas a los puntos
for i, txt in enumerate(df.index):
    ax.annotate(txt, (row_coords[0][i], row_coords[1][i]), fontsize=3)  # Ajusta 'fontsize' para cambiar el tamaño de las letras
for i, txt in enumerate(df.columns):
    ax.annotate(txt, (col_coords[0][i], col_coords[1][i]), fontsize=3)  # Ajusta 'fontsize' para cambiar el tamaño de las letras
    
# Añadir una leyenda
ax.legend()

# Guardar el gráfico como un archivo PNG
plt.savefig('Pottery_overlap_correspondence_analysis.png', dpi=2160)  # Ajusta 'dpi' para cambiar la resolución de la imagen

# Mostrar el gráfico
plt.show()








############################## Level - Sex ####################################

df2 = pd.read_csv('level_sex_sample.csv',  usecols=lambda x: x != 'Unnamed: 0')
df2 = df2.set_index('Sex')
df2 = df2.fillna(df.mean())


if (df2 < 5).any().any():
    df2 = (df2 + 1) * 5

# Realizar el análisis de correspondencias
ca = prince.CA(
    n_components=2,
    n_iter=10,
    copy=True,
    check_input=True,
    engine='sklearn',# Asegúrate de que el motor sea 'fbpca', 'scipy' o 'sklearn'
    random_state=42
)
ca = ca.fit(df2)

# Obtener las coordenadas de las filas y las columnas
row_coords2 = ca.row_coordinates(df)
col_coords2 = ca.column_coordinates(df0)

# Crear una figura y un conjunto de subtramas
fig, ax = plt.subplots()

# Verificar si las coordenadas de las filas tienen más de una dimensión antes de trazarlas

ax.scatter(row_coords[0], row_coords[0], color='red', label='Level', s=1) 

# Verificar si las coordenadas de las columnas tienen más de una dimensión antes de trazarlas

ax.scatter(col_coords[0], col_coords[0], color='blue', label='Sex', s=1) 

# Añadir etiquetas a los puntos
for i, txt in enumerate(df2.index):
    ax.annotate(txt, (row_coords[0][i], row_coords[0][i]), fontsize=3)
for i, txt in enumerate(df2.columns):
    ax.annotate(txt, (col_coords[0][i], col_coords[0][i]), fontsize=3)

# Añadir una leyenda
ax.legend()

# Guardar el gráfico como un archivo PNG
plt.savefig('level_sex_correspondence_analysis.png', dpi=2160)

# Mostrar el gráfico
plt.show()





