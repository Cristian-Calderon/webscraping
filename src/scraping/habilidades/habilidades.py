import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Cargar el CSV y tomar solo los primeros 10 héroes
file_path = "../heroes/heroes-spanish.csv"
heroes_df = pd.read_csv(file_path)  # 🔹 CARGAR TODOS LOS HÉROES

# Configurar Selenium en modo sin interfaz gráfica
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(30)

# Lista para almacenar los datos extraídos
data = []
id_habilidad = 1  # Contador de ID de habilidad

# Recorrer los 10 héroes seleccionados
for hero_id, row in heroes_df.iterrows():
    hero_name = row['nombre']
    abilities_url = row['link-Pagina'] + "/abilities"
    
    print(f"Scrapeando habilidades de {hero_name}...")
    
    try:
        driver.get(abilities_url)
        time.sleep(3)  

        abilities = driver.find_elements(By.XPATH, "//div[@class='skill-tooltip reborn-tooltip']")
        
        for ability in abilities:
            try:
                ability_name = ability.find_element(By.XPATH, ".//div[@class='bigavatar']//img").get_attribute("alt")
                ability_description = ability.find_element(By.XPATH, ".//div[@class='description']/p").text
                
                # 🔹 QUITAR SALTOS DE LÍNEA Y ESCAPES
                ability_description = ability_description.replace("\n", " ").replace("\\", "")
                
                # 🔹 AGREGAR COMILLAS SOLO A LA COLUMNA DESCRIPCIÓN
                ability_description = f'"{ability_description}"'
                
                ability_image = ability.find_element(By.XPATH, ".//div[@class='bigavatar']//img").get_attribute("src")
                
                # Guardar los datos extraídos
                data.append({
                    "id_habilidad": id_habilidad,
                    "id_heroe": hero_id + 1,  
                    "Héroe": hero_name,
                    "Nombre de Habilidad": ability_name,
                    "Descripción": ability_description,
                    "Imagen": ability_image
                })
                id_habilidad += 1  
                
            except:
                print(f"Error al extraer una habilidad para {hero_name}")
        
    except:
        print(f"No se pudieron extraer las habilidades para {hero_name}")
    
# Guardar los datos en un nuevo CSV
output_df = pd.DataFrame(data)

# 🔹 Guardar el CSV sin afectar otras columnas con comillas dobles
output_path = "./dota_heroes_abilities.csv"
output_df.to_csv(output_path, index=False, quoting=csv.QUOTE_NONE, sep=",", escapechar="\\") 

driver.quit()
print(f"✅ Datos guardados correctamente en {output_path}")
