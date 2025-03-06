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

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(30)  # Aumentar el tiempo de espera para cargar la página
driver.maximize_window()  # Abrir el navegador en pantalla completa

# Lista para almacenar los datos extraídos
data = []
id_habilidad = 1  # Contador de ID de habilidad

# Recorrer todos los héroes
for hero_id, row in heroes_df.iterrows():
    hero_name = row['nombre']
    abilities_url = row['link-Pagina'] + "/abilities"
    
    print(f"Scrapeando habilidades de {hero_name}...")
    
    try:
        driver.get(abilities_url)
        time.sleep(3)  # Esperar para cargar la página
        
        abilities = driver.find_elements(By.XPATH, "//div[@class='skill-tooltip reborn-tooltip']")
        
        for ability in abilities:
            try:
                ability_name = ability.find_element(By.XPATH, ".//div[@class='bigavatar']//img").get_attribute("alt")
                ability_description = ability.find_element(By.XPATH, ".//div[@class='description']/p").text
                ability_image = ability.find_element(By.XPATH, ".//div[@class='bigavatar']//img").get_attribute("src")
                
                # Guardar los datos extraídos con ID de habilidad
                data.append({
                    "id_habilidad": id_habilidad,
                    "id_heroe": hero_id + 1,  # Asegurar que el ID de héroe empiece en 1
                    "Héroe": hero_name,
                    "Nombre de Habilidad": ability_name,
                    "Descripción": ability_description,
                    "Imagen": ability_image
                })
                id_habilidad += 1  # Incrementar el ID de habilidad
                
            except:
                print(f"Error al extraer una habilidad para {hero_name}")
        
    except:
        print(f"No se pudieron extraer las habilidades para {hero_name}")
    
# Guardar los datos en un nuevo CSV
output_df = pd.DataFrame(data)
output_path = "./dota_heroes_abilities.csv"
output_df.to_csv(output_path, index=False)

driver.quit()
print(f"Datos guardados en {output_path}")
