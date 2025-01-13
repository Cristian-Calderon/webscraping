import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# Leer el archivo CSV
csv_file = "heroes.csv"  # Nombre del archivo CSV
data = pd.read_csv(csv_file)

# Configuración del driver (usando Chrome como ejemplo)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Ajustar tiempo de espera para evitar timeouts
driver.set_page_load_timeout(300)  # 300 segundos = 5 minutos

# Función para manejar reintentos en caso de fallos al cargar la página
def acceder_url(driver, url, intentos=3):
    for intento in range(intentos):
        try:
            driver.get(url)
            return True  # Salir si se carga correctamente
        except TimeoutException:
            print(f"Intento {intento + 1} fallido para {url}")
            time.sleep(5)  # Esperar antes del siguiente intento
    return False

# Crear una lista para almacenar los datos obtenidos de cada página
resultados = []

# Recorrer cada enlace en la columna 'link-Pagina'
for index, row in data.iterrows():
    link_pagina = row['link-Pagina']  # Columna que contiene los enlaces
    print(f"Accediendo a: {link_pagina}")

    # Intentar acceder a la página
    if not acceder_url(driver, link_pagina):
        print(f"No se pudo cargar la página: {link_pagina}")
        continue

    # Extraer popularidad
    try:
        popularidad = driver.find_element(By.CSS_SELECTOR, "dd").text  # Etiqueta <dd>
    except Exception as e:
        popularidad = "No disponible"
        print(f"Error extrayendo popularidad para {link_pagina}: {e}")

    # Extraer win-rate
    try:
        win_rate = driver.find_element(By.CSS_SELECTOR, "span.lost").text  # Clase "lost" en <span>
    except Exception as e:
        win_rate = "No disponible"
        print(f"Error extrayendo win-rate para {link_pagina}: {e}")

    # Guardar los resultados
    resultados.append({
        "nombre": row['nombre'],  # Puedes usar la columna nombre del CSV original
        "link-Pagina": link_pagina,
        "popularidad": popularidad,
        "win_rate": win_rate
    })

# Cerrar el navegador
driver.quit()

# Guardar los nuevos datos en un archivo CSV
resultados_df = pd.DataFrame(resultados)
resultados_df.to_csv("heroes_detallados.csv", index=False, encoding="utf-8")

print("Scraping completado. Datos guardados en 'heroes_detallados.csv'.")
