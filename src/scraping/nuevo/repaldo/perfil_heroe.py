import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Configurar navegador headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Iniciar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Cargar CSV y corregir nombres de columnas
csv_filename = "dota2_heroes.csv"
df_heroes = pd.read_csv(csv_filename)
df_heroes.columns = df_heroes.columns.str.strip()

# Verificar si la columna "Pagina" existe
if "Pagina" not in df_heroes.columns:
    print(f"⚠️ La columna 'Pagina' no existe. Columnas disponibles: {df_heroes.columns}")
    exit()

# Procesar todos los héroes en el CSV
df_heroes = df_heroes

# Lista para almacenar datos de héroes
heroes_data = []

# Función para limpiar HTML y eliminar saltos de línea
def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ")  # Reemplaza los saltos de línea con espacios
    return re.sub(r'\s+', ' ', text).strip()  # Elimina espacios extras

# Iterar sobre los héroes
for index, row in df_heroes.iterrows():
    hero_name = row["Nombre"].strip()
    hero_url = row["Pagina"].strip()

    print(f"🔍 Scraping de {hero_name}: {hero_url}")
    driver.get(hero_url)
    time.sleep(5)  # Esperar carga de la página

    try:
        # Extraer video correcto (.mov)
        video_elements = driver.find_elements(By.CSS_SELECTOR, 'video source')
        hero_video = next((video.get_attribute("src") for video in video_elements if video.get_attribute("src") and video.get_attribute("src").endswith(".mov")), "")

        # Extraer breve descripción
        try:
            breve_element = driver.find_element(By.CSS_SELECTOR, 'div._2r7tdOONJnLw_6bQuNZj5b')
            breve = breve_element.text.strip().replace('"', "'") if breve_element.text.strip() else ""
        except:
            breve = ""

        # Extraer descripción completa y limpiar HTML
        try:
            desc_element = driver.find_element(By.CSS_SELECTOR, 'div._3NVqFQw8f9M_5-dvX4Ws1Z > div')
            descripcion = clean_text(desc_element.get_attribute("innerHTML")) if desc_element else ""
        except:
            descripcion = ""

        # Extraer tipo de ataque
        try:
            attack_type_element = driver.find_element(By.CSS_SELECTOR, 'div._3ce-DKDrVB7q5LsGbJdZ3X')
            attack_type = attack_type_element.text.strip() if attack_type_element.text.strip() else ""
        except:
            attack_type = ""

        # Extraer atributos
        stats_elements = driver.find_elements(By.CSS_SELECTOR, 'div._3Gsggcx9qe3qVMxUs_XeOo')
        strength = stats_elements[0].text.strip() if len(stats_elements) > 0 else "0"
        agility = stats_elements[1].text.strip() if len(stats_elements) > 1 else "0"
        intelligence = stats_elements[2].text.strip() if len(stats_elements) > 2 else "0"

        # Extraer estadísticas de combate y limpiar valores no deseados
        stats = driver.find_elements(By.CSS_SELECTOR, 'div._3783Tb-SbeUvvdBW9iSB_x')
        extracted_stats = [s.text.strip() for s in stats]

        # Filtrar datos correctos y evitar incluir velocidad de proyectil y visión
        filtered_stats = [value for value in extracted_stats if not value.isdigit() or int(value) < 800]

        # Asignar valores asegurando el orden correcto
        damage = filtered_stats[0] if len(filtered_stats) > 0 else "0"
        attack_time = filtered_stats[1] if len(filtered_stats) > 1 else "0"
        attack_range = filtered_stats[2] if len(filtered_stats) > 2 else "0"
        armor = filtered_stats[3] if len(filtered_stats) > 3 else "0"
        magic_resist = filtered_stats[4] if len(filtered_stats) > 4 else "0"
        movement_speed = filtered_stats[5] if len(filtered_stats) > 5 else "0"
        turn_rate = filtered_stats[6] if len(filtered_stats) > 6 else "0"

        # Agregar a la lista
        heroes_data.append([
            hero_name, hero_video, breve, descripcion, attack_type,
            strength, agility, intelligence, damage, attack_time,
            attack_range, armor, magic_resist,
            movement_speed, turn_rate
        ])

        print(f"✅ {hero_name} procesado correctamente.")

    except Exception as e:
        print(f"⚠️ Error en {hero_name}: {e}")

# Guardar en CSV corregido
csv_output = "dota2_heroes_details_completo.csv"
df_output = pd.DataFrame(heroes_data, columns=[
    "Nombre", "Video", "Breve", "Descripción", "Tipo de Ataque",
    "Fuerza", "Agilidad", "Inteligencia", "Daño", "Tiempo de Ataque",
    "Rango de Ataque", "Armadura",
    "Resistencia Mágica", "Velocidad de Movimiento", "Tasa de Giro"
])

# Convertir valores vacíos a None para evitar comillas dobles en CSV
df_output = df_output.where(pd.notna(df_output), None)

# Guardar CSV con formato correcto
df_output.to_csv(csv_output, index=False, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)

# Cerrar el navegador
driver.quit()
print(f"🎯 Scraping completado. Datos guardados en {csv_output}")
