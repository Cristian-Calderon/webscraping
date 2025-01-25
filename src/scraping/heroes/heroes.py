from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configuración del driver (usando Chrome como ejemplo)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# URL de la página que quieres scrapear
url = "https://www.dotabuff.com/heroes"  # Reemplaza con la URL real

# Accede a la página
driver.get(url)
time.sleep(5)  # Espera para permitir que la página cargue completamente

# Encuentra los elementos para rutas de imágenes
imagenes = driver.find_elements(By.CSS_SELECTOR, "img.tw-relative.tw-size-full.tw-rounded-sm")

# Extrae los datos
data = []
for imagen in imagenes:
    link_imagen = imagen.get_attribute("src")  # Obtiene el atributo src de la imagen
    if link_imagen:  # Verifica que el enlace no sea None
        # Extrae la última palabra del enlace eliminando la extensión del archivo
        nombre_hero = link_imagen.split("/")[-1].replace(".jpg", "").replace("-", " ").title()
        # Construye el enlace de la página
        link_pagina = "https://www.dotabuff.com/heroes/" + link_imagen.split("/")[-1].replace(".jpg", "")
        data.append({"name": nombre_hero, "link-Img": link_imagen, "link-Page": link_pagina})

# Cierra el navegador
driver.quit()

# Guarda los datos en un archivo CSV
df = pd.DataFrame(data)
df.to_csv("heroes.csv", index=False, encoding="utf-8")

print("Scraping completado. Datos guardados en 'heroes.csv'.")
