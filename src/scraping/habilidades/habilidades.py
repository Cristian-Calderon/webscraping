import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# Leer el archivo CSV
csv_file = "../heroes/heroes.csv"  # Nombre del archivo CSV
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
            print(f"[DEBUG] Intentando acceder a: {url} (Intento {intento + 1})")
            driver.get(url)
            print(f"[DEBUG] Acceso exitoso a: {url}")
            return True  # Salir si se carga correctamente
        except TimeoutException:
            print(f"[DEBUG] Timeout al intentar acceder a: {url} (Intento {intento + 1})")
            time.sleep(5)  # Esperar antes del siguiente intento
    return False

# Crear una lista para almacenar los datos obtenidos de cada página
resultados = []

# Recorrer cada enlace en la columna 'link-Pagina'
for index, row in data.iterrows():
    link_pagina = row['link-Pagina']  # Columna que contiene los enlaces
    print(f"[DEBUG] Procesando el héroe: {row['nombre']} con URL: {link_pagina}")

    # Intentar acceder a la página
    if not acceder_url(driver, link_pagina):
        print(f"[ERROR] No se pudo cargar la página: {link_pagina}")
        continue

    # Extraer popularidad
    try:
        popularidad = driver.find_element(By.CSS_SELECTOR, "dd").text
        print(f"[DEBUG] Popularidad obtenida: {popularidad}")
    except Exception as e:
        popularidad = "No disponible"
        print(f"[ERROR] Error extrayendo popularidad para {link_pagina}: {e}")

    # Extraer win-rate
    try:
        win_rate = ""
        try:
            win_rate = driver.find_element(By.CSS_SELECTOR, "span.won").text
            print(f"[DEBUG] Win-rate obtenido (won): {win_rate}")
        except:
            win_rate = driver.find_element(By.CSS_SELECTOR, "span.lost").text
            print(f"[DEBUG] Win-rate obtenido (lost): {win_rate}")
    except Exception as e:
        win_rate = "No disponible"
        print(f"[ERROR] Error extrayendo win-rate para {link_pagina}: {e}")

    # Extraer habilidades
    habilidades = []
    try:
        habilidades_imgs = driver.find_elements(By.CSS_SELECTOR, "img.image-bigicon.image-skill")
        for img in habilidades_imgs:
            habilidad_nombre = img.get_attribute("alt")
            habilidad_img = img.get_attribute("src")
            habilidades.append({"nombre": habilidad_nombre, "imagen": habilidad_img})
        print(f"[DEBUG] Habilidades extraídas: {habilidades}")
    except Exception as e:
        print(f"[ERROR] Error extrayendo habilidades para {link_pagina}: {e}")

    # Guardar los resultados
    resultados.append({
        "nombre": row['nombre'],  # Puedes usar la columna nombre del CSV original
        "link-Pagina": link_pagina,
        "popularidad": popularidad,
        "win_rate": win_rate,
        "habilidades": habilidades
    })

    print(f"[DEBUG] Datos guardados para {row['nombre']}: Popularidad - {popularidad}, Win-rate - {win_rate}, Habilidades - {habilidades}")

# Cerrar el navegador
driver.quit()

# Guardar los nuevos datos en un archivo JSON (mejor para estructuras complejas como habilidades)
import json
output_file = "habilidades.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(resultados, file, ensure_ascii=False, indent=4)

print(f"[INFO] Scraping completado. Datos guardados en '{output_file}'.")
