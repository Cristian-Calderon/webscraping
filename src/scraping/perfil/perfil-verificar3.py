import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# Ruta del archivo CSV con los héroes
csv_file = "../heroes/heroes.csv"

# Cargar el archivo CSV asegurando que los nombres de las columnas sean correctos
data = pd.read_csv(csv_file)

# Renombrar columnas para evitar problemas
data.rename(columns={'link-Img': 'link_img', 'link-Page': 'link_page'}, inplace=True)

# Agregar un índice basado en la base de datos (hero_id)
data['hero_id'] = range(1, len(data) + 1)

# Configuración del driver de Selenium (modo headless para mayor eficiencia)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome(options=options)

# Ajustar tiempo de espera para evitar timeouts
driver.set_page_load_timeout(300)

# Función para manejar reintentos en caso de fallos al cargar la página
def acceder_url(driver, url, intentos=3):
    for intento in range(intentos):
        try:
            print(f"[DEBUG] Intentando acceder a: {url} (Intento {intento + 1})")
            driver.get(url)
            print(f"[DEBUG] Acceso exitoso a: {url}")
            return True
        except TimeoutException:
            print(f"[DEBUG] Timeout al intentar acceder a: {url} (Intento {intento + 1})")
            time.sleep(5)
    return False

# Lista para almacenar los resultados
resultados = []

# Recorrer cada héroe con su ID asignado
for index, row in data.iterrows():
    hero_id = row['hero_id']
    link_pagina = row['link_page']

    print(f"[DEBUG] Procesando héroe ID {hero_id} con URL: {link_pagina}")

    if not acceder_url(driver, link_pagina):
        print(f"[ERROR] No se pudo cargar la página: {link_pagina}")
        continue

    try:
        popularidad = driver.find_element(By.CSS_SELECTOR, "dd").text
        print(f"[DEBUG] Popularidad obtenida: {popularidad}")
    except Exception as e:
        popularidad = "No disponible"
        print(f"[ERROR] Error extrayendo popularidad para {link_pagina}: {e}")

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

    # Guardar en la lista con hero_id correcto
    resultados.append({
        "hero_id": hero_id,
        "popularidad": popularidad,
        "win_rate": win_rate
    })

    print(f"[DEBUG] Datos guardados para ID {hero_id}: Popularidad - {popularidad}, Win-rate - {win_rate}")

# Cerrar el navegador
driver.quit()

# Guardar los nuevos datos en un archivo CSV
resultados_df = pd.DataFrame(resultados)
output_file = "heroes_stats.csv"
resultados_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"[INFO] Scraping completado. Datos guardados en '{output_file}'.")
