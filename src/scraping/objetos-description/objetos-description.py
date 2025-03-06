from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Cargar el CSV de ítems
file_path = "../objetos/dota_items.csv"
items_df = pd.read_csv(file_path)

# Limitar a los primeros 5 ítems
items_df = items_df.head(5)

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(30)  # Aumentar el tiempo de espera para cargar la página
driver.maximize_window()  # Abrir el navegador en pantalla completa

# Lista para almacenar los datos extraídos
data = []

print("Scrapeando descripciones de los primeros 5 ítems de Dota 2...")
for index, row in items_df.iterrows():
    id_item = row['id_item']
    item_name = row['Nombre']
    item_url = row['Link']
    
    print(f"Scrapeando datos de {item_name}...")
    
    try:
        driver.get(item_url)
        time.sleep(3)  # Esperar para cargar la página
        
        # Extraer imagen (si existe)
        try:
            item_image = driver.find_element(By.XPATH, "//div[@class='avatar']//img").get_attribute("src")
        except:
            item_image = ""
        
        # Extraer costo del ítem (si existe)
        try:
            item_cost = driver.find_element(By.XPATH, "//div[@class='price']//span[@class='value']/span").text
        except:
            item_cost = "Neutral Item"  # Si no tiene costo, es un objeto neutral
        
        # Extraer descripción del ítem (si existe)
        try:
            item_description = driver.find_element(By.XPATH, "//div[@class='description']//div").text
        except:
            item_description = ""
        
        # Solo guardar si hay descripción
        if item_description:
            data.append({
                "id_item": id_item,
                "Nombre": item_name,
                "Imagen": item_image,
                "Costo": item_cost,
                "Descripción": item_description
            })
        
    except Exception as e:
        print(f"Error al extraer datos de {item_name}: {e}")
    
# Guardar los datos en un nuevo CSV
output_df = pd.DataFrame(data)
output_path = "./dota_items_description.csv"
output_df.to_csv(output_path, index=False)

driver.quit()
print(f"Datos guardados en {output_path}")
