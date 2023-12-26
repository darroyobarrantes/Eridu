import pandas as pd
import openpyxl
import numpy as np
import re
from fuzzywuzzy import fuzz
import math

# Open the Excel file
excel_file = openpyxl.load_workbook('muestra.xlsx')

df = pd.read_excel('muestra.xlsx')
df_safar = pd.read_csv("SafarTombs.csv")

# Select the sheet you want to read (e.g., the first sheet)
sheet = excel_file.active
values = []

def clean_text(text):
    print(text)
    if pd.isna(text):
        return text
    # Remove extra whitespace
    clean_text = ' '.join(text.split())

    # Remove line breaks and other special control characters
    clean_text = clean_text.replace('\n', ' ')
    clean_text = clean_text.replace('\r', '')
    clean_text = clean_text.lower()
    clean_text = clean_text.strip()
    return clean_text

# Iterate cell by cell in columns A to J
for row in sheet.iter_rows(min_col=1, max_col=10):  # Columns A to J are columns 1 to 10
    for cell in row:
        # Get the cell's value
        value = cell.value

        if value is not None:
            value = str(value)
            value = clean_text(value)
            values.append(value)

# Close the Excel file
excel_file.close()

data = []
temp_data = []
i = 1
for value in values:
    temp_data.append(value)
    if i % 9 == 0:
        data.append(temp_data)
        temp_data = []
    i += 1

df = pd.DataFrame(data)

df.columns = df.iloc[0]
df = df.iloc[1:].reset_index(drop=True)
df['grave'] = df['burial'].str.split().str[-1]

def assign_individual(row):
    grave_count = df['grave'].eq(row['grave']).cumsum()
    return chr(64 + grave_count[row.name])

# Create the new "Individual" column
df['individual'] = df.apply(assign_individual, axis=1)
df
def extract_level(sub_phase):
    if "level" in sub_phase:
        return float(sub_phase.split()[1])
    elif sub_phase == "surface":
        return 0
    else:
        return np.nan

# Create the new "Level" column
df['level'] = df['sub phase'].apply(extract_level)

def get_orientation(skeletal_material):
    words = skeletal_material.split()
    if "orientated" in words:
        orientation_index = words.index("orientated")
        if orientation_index < len(words) - 1:
            return words[orientation_index + 1]
    return np.nan

# Create the new "Orientation" column
df['orientation'] = df['skeletal material'].apply(get_orientation)

df = df.drop('age', axis=1)
df.rename(columns={'age cat.': 'age', 'burial method': 'type'}, inplace=True)
df.set_index('grave', inplace=True)
df.replace(['n/a', "not recorded"], np.nan, inplace=True)
df.index = df.index.astype(int)
df
#getting pottery types

patron = r'\b\d{1,2}[A-Za-z]\b'
finds_match = []
other_objects_match = []

# Iterar a través de la columna 'Texto'
for texto in df['finds']:
    if pd.isna(texto):
        finds_match.append(texto)
        other_objects_match.append(texto)
    else:
        coincidencias_finds = re.findall(patron, texto)
        texto_modificado = re.sub(patron, '', texto)
        texto_modificado = re.sub("pottery types:", '', texto_modificado)
        texto_modificado = re.sub("pottery types", '', texto_modificado)
        texto_modificado = re.sub(r'[^\w\s]', '', texto_modificado)
        other_objects_match.append(texto_modificado)
        if len(coincidencias_finds) != 0:
            finds_match.append(', '.join(coincidencias_finds))
        else:
            finds_match.append(float('nan'))
            
df
# crear columnas con los match
df["pottery types"] = finds_match
df["other objects"] = other_objects_match

df["other objects"] = df['other objects'].apply(clean_text)


#ordenar columnas
column_order = ["individual", "level", "orientation", "type", "sex", "age", "skeletal material", "pottery types", "other objects", "spatial context"]
df = df[column_order]

def get_body_specifications(row):
    # Check if the row is a string
    if not isinstance(row, str):
        return row

    # Split the row by ".", and "," characters
    parts = re.split('[.,]', row)

    # Keywords to search for
    keywords_to_search = ["adult?", "adult male", "adult female", "female skeleton", "male skeleton",
                         "orientated nw", "orientated se", "child skeleton", "infant skeleton", "adult? skeleton- bad preservation'"]

    # Initialize a list to store the final parts
    final_parts = []

    # Iterate through the resulting parts
    for part in parts:
         cleaned_part = part.strip()  # Remove leading and trailing whitespace
     
         if cleaned_part != "":
             max_similarity = max([fuzz.ratio(cleaned_part, keyword) for keyword in keywords_to_search])
             if max_similarity <= 65:
                 final_parts.append(cleaned_part)

    # Transformar la lista en una cadena separada por ;
    separated_string = ";".join(final_parts)

    return separated_string

df = df.sort_index(ascending=True)

# Process the example rows
df['skeletal material'] = df['skeletal material'].apply(get_body_specifications)
column_mapping = {
    "individual": "Individual",
    "level": "Level",
    "orientation": "Orientation",
    "type": "Type",
    "sex": "Sex",
    "age": "Age",
    "skeletal material": "Position",
    "pottery types": "Pottery types",
    "other objects": "Other objects",
    "spatial context": "Spatial context"
}

# Renombrar las columnas
df.rename(columns=column_mapping, inplace=True)
df.columns = [col.capitalize() for col in df.columns]
df.to_csv("cleaned_sample.csv")

df2 = pd.DataFrame(columns=["Grave", "Individual", "Level", "Orientation", "Type", "Sex", "Age", "Position", "Size", "Pottery types", "Other objects", "Preservation", "Photo Diagram"])
