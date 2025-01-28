import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configurar Selenium
options = Options()
options.add_argument('--headless')  # Ejecutar en modo sin interfaz
options.add_argument('--disable-gpu')  # Deshabilitar uso de GPU
options.add_argument('--no-sandbox')  # Prevención de errores en servidores
service = Service('/path/to/chromedriver')  # Reemplaza con la ruta de tu chromedriver
driver = webdriver.Chrome(service=service, options=options)

# Leer el CSV original
input_csv_path = '../heroes/heroes.csv'  # Reemplaza con la ruta de tu archivo
heroes = pd.read_csv(input_csv_path)

# Añadir la columna "abilities"
heroes['link-abilities'] = heroes['link-Pagina'] + '/abilities'

# Lista para almacenar los resultados
data = []

# Recorrer los héroes y hacer scraping de habilidades
for _, row in heroes.iterrows():
    hero_name = row['nombre']
    abilities_url = row['link-abilities']
    driver.get(abilities_url)
    time.sleep(2)  # Esperar a que cargue la página
    
    try:
        # Seleccionar los nombres de las habilidades
        abilities = driver.find_elements(By.CSS_SELECTOR, '.ability-tooltip > div:nth-child(1)')
        ability_names = [ability.text for ability in abilities]
        
        # Crear una fila con las habilidades
        hero_data = {'nombre': hero_name}
        for i, ability in enumerate(ability_names, start=1):
            hero_data[f'nombre-habilidad-{i:02d}'] = ability
        
        data.append(hero_data)
    except Exception as e:
        print(f"Error procesando {hero_name}: {e}")

# Cerrar el navegador
driver.quit()

# Crear un DataFrame con los resultados
output_df = pd.DataFrame(data)

# Guardar en un nuevo archivo CSV
output_csv_path = '../description/heroes_abilities.csv'  # Reemplaza con la ruta de salida
output_df.to_csv(output_csv_path, index=False)

print(f"Scraping completado. Datos guardados en {output_csv_path}")
