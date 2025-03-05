from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Cargar el CSV
file_path = "../heroes/heroes-spanish.csv"
heroes_df = pd.read_csv(file_path)

# Limitar a los cinco primeros héroes
heroes_df = heroes_df.head(5)

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(30)  # Aumentar el tiempo de espera para cargar la página
driver.maximize_window()  # Abrir el navegador en pantalla completa

# Lista para almacenar los datos extraídos
data = []

# Recorrer los cinco primeros héroes
for index, row in heroes_df.iterrows():
    hero_name = row['nombre']
    hero_url = row['link-Pagina']
    
    print(f"Scrapeando datos de {hero_name}...")
    
    retries = 3  # Número de intentos permitidos
    for attempt in range(retries):
        try:
            driver.get(hero_url)
            time.sleep(3)  # Esperar para cargar la página
            break  # Si la página carga bien, salimos del loop
        except Exception as e:
            print(f"Intento {attempt + 1} fallido al cargar {hero_url}: {e}")
            if attempt == retries - 1:
                print(f"Omitiendo {hero_name} tras {retries} intentos fallidos")
                continue
    
    try:
        # Esperar hasta que el elemento esté presente
        popularity = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='header-content-secondary']//dl[1]/dd"))
        ).text
    except:
        print(f"No se encontró la popularidad para {hero_name}")
        popularity = "N/A"
    
    try:
        # Extraer Porcentaje de Victoria
        winrate_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='header-content-secondary']//dl[2]/dd/span"))
        )
        winrate = winrate_element.text
        winrate_class = winrate_element.get_attribute("class")
        won_or_lost = "won" if "won" in winrate_class else "lost"
    except:
        print(f"No se encontró el porcentaje de victoria para {hero_name}")
        winrate, won_or_lost = "N/A", "N/A"
    
    try:
        # Extraer atributos del héroe
        strength = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tbody[@class='primary-strength']/tr[2]/td[1]"))
        ).text
        agility = driver.find_element(By.XPATH, "//tbody[@class='primary-strength']/tr[2]/td[2]").text
        intelligence = driver.find_element(By.XPATH, "//tbody[@class='primary-strength']/tr[2]/td[3]").text
    except:
        print(f"No se encontraron atributos principales para {hero_name}")
        strength, agility, intelligence = "N/A", "N/A", "N/A"
    
    try:
        attributes = driver.find_elements(By.XPATH, "//table[@class='other']/tbody/tr")
        extra_attributes = {row.find_element(By.XPATH, "td[1]").text: row.find_element(By.XPATH, "td[2]").text for row in attributes}
    except:
        print(f"No se encontraron atributos adicionales para {hero_name}")
        extra_attributes = {}
    
    # Guardar los datos extraídos
    data.append({
        "Héroe": hero_name,
        "Popularidad": popularity,
        "Porcentaje de Victoria": winrate,
        "Resultado": won_or_lost,
        "Fuerza": strength,
        "Agilidad": agility,
        "Inteligencia": intelligence,
        **extra_attributes
    })
    
# Guardar los datos en un nuevo CSV
output_df = pd.DataFrame(data)
output_path = "./dota_heroes_data.csv"
output_df.to_csv(output_path, index=False)

driver.quit()
print(f"Datos guardados en {output_path}")
