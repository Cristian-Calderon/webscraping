from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Configuración del driver (usando Chrome como ejemplo)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# URL de la página que quieres scrapear
url = "https://es.dotabuff.com/heroes"  # Reemplaza con la URL real

# Accede a la página
driver.get(url)
time.sleep(5)  # Espera para permitir que la página cargue completamente

# Encuentra los elementos para nombres y rutas de imágenes
nombres = driver.find_elements(By.CSS_SELECTOR, "div.tw-w-full.tw-text-center.tw-text-\[7px\].tw-leading-none.tw-text-white")

imagenes = driver.find_elements(By.CSS_SELECTOR, "img.tw-relative.tw-size-full.tw-rounded-sm")

# Extrae los datos
data = []
for nombre, imagen in zip(nombres, imagenes):
    nombre_texto = nombre.text.strip()  # Obtiene el texto del nombre y elimina espacios innecesarios
    link_imagen = imagen.get_attribute("src")  # Obtiene el atributo src de la imagen
    data.append({"nombre": nombre_texto, "link-Imagen": link_imagen})

# Cierra el navegador
driver.quit()

# Guarda los datos en un archivo CSV
df = pd.DataFrame(data)
df.to_csv("heroes.csv", index=False, encoding="utf-8")

print("Scraping completado. Datos guardados en 'heroes.csv'.")
