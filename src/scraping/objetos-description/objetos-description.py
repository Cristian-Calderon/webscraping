from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Cargar el CSV de ítems
file_path = "../objetos/dota_items.csv"
items_df = pd.read_csv(file_path)

# Configurar Selenium (modo sin interfaz gráfica)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar en modo sin cabeza
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(30)  # Aumentar el tiempo de espera para cargar la página

# Lista para almacenar los datos extraídos
data = []

print("Scrapeando descripciones de todos los ítems de Dota 2...")
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
            item_cost_element = driver.find_element(By.XPATH, "//div[@class='price']")
            if "Sin Coste" in item_cost_element.text or "Neutral Item" in item_cost_element.text:
                item_cost = "Neutral Item"
            else:
                item_cost = item_cost_element.find_element(By.XPATH, "./span[@class='value']/span").text
        except:
            item_cost = "Neutral Item"  # Si no tiene costo, es un objeto neutral
        
        # Extraer descripción del ítem (si existe, dejar vacío si no la tiene)
        try:
            description_blocks = driver.find_elements(By.XPATH, "//div[@class='description']//div | //div[@class='description-block']")
            item_description = " ".join([block.text for block in description_blocks if block.text.strip()])
        except:
            item_description = ""
        
        # Manejar el caso donde la descripción se encuentra dentro de un bloque con class 'cooldown-and-cost'
        try:
            if not item_description:
                cooldown_blocks = driver.find_elements(By.XPATH, "//div[@class='cooldown-and-cost']//div")
                item_description = " ".join([block.text for block in cooldown_blocks if block.text.strip()])
        except:
            pass
        
        # Manejar el caso de elementos con encabezados en la descripción
        try:
            if not item_description:
                header_blocks = driver.find_elements(By.XPATH, "//div[@class='description']//h1 | //div[@class='description']//div[@class='description-block-header']")
                item_description = " ".join([block.text for block in header_blocks if block.text.strip()])
        except:
            pass
        
        # Guardar los datos, incluso si no tiene descripción
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
