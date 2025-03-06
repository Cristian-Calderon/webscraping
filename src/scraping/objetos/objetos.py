from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# URL de la página de ítems
items_url = "https://es.dotabuff.com/items"

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(30)  # Aumentar el tiempo de espera para cargar la página
driver.maximize_window()  # Abrir el navegador en pantalla completa

# Lista para almacenar los datos extraídos
data = []

print("Scrapeando ítems de Dota 2...")
try:
    driver.get(items_url)
    time.sleep(3)  # Esperar para cargar la página
    
    items = driver.find_elements(By.XPATH, "//tbody/tr")
    id_item = 1  # Contador de ID de ítem
    
    for item in items:
        try:
            item_name = item.find_element(By.XPATH, ".//td[@class='cell-xlarge']/a").text
            item_link_suffix = item.find_element(By.XPATH, ".//td[@class='cell-xlarge']/a").get_attribute("href")
            item_link = "https://es.dotabuff.com" + item_link_suffix.replace("https://es.dotabuff.com", "")
            
            # Guardar los datos extraídos con ID de ítem
            data.append({
                "id_item": id_item,
                "Nombre": item_name,
                "Link": item_link
            })
            id_item += 1  # Incrementar el ID de ítem
            
        except:
            print("Error al extraer un ítem")
    
except:
    print("No se pudieron extraer los ítems")

# Guardar los datos en un nuevo CSV
output_df = pd.DataFrame(data)
output_path = "./dota_items.csv"
output_df.to_csv(output_path, index=False)

driver.quit()
print(f"Datos guardados en {output_path}")
