# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:00:52 2024

@author: fabia
"""

# Importar el webdriver de selenium
from selenium import webdriver

# Crear una instancia del navegador Chrome
browser = webdriver.Chrome()

# Definir el URL base
base_url = "https://mc.dlib.nyu.edu/files/books/brill_awdl"

# Definir el rango de números a usar
start = 00 # Número inicial
end = 10 # Número final

# Iterar sobre el rango de números
for i in range(start, end + 1):
  # Formatear el número con seis dígitos y ceros a la izquierda
  num = str(i).zfill(6)
  # Concatenar el número al URL base
  url = base_url + num + "/brill_awdl" + num + "_lo.pdf"
  # Ejecutar un script de javascript para abrir una nueva pestaña con el URL
  browser.execute_script("window.open('" + url + "', '_blank');")
