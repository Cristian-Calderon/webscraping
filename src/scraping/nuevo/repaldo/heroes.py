import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de Chrome en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Descargar y configurar ChromeDriver automáticamente
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Cargar la página de héroes
url = "https://www.dota2.com/heroes"
driver.get(url)

# Esperar carga de la página
time.sleep(5)

# Extraer lista de héroes
heroes = driver.find_elements(By.CSS_SELECTOR, 'a._7szOnSgHiQLEyU0_owKBB')

# Lista para almacenar datos
heroes_data = []

for hero in heroes:
    try:
        # Obtener el nombre del héroe correctamente
        name_element = hero.find_element(By.CSS_SELECTOR, 'div._3N-bh9taW0W_prRSK7IMzC')
        name = name_element.get_attribute('textContent').strip().replace("\u00a0", " ")  # Reemplazar &nbsp; por un espacio normal

        # Obtener la URL del atributo del héroe
        attribute_img = hero.find_element(By.CSS_SELECTOR, 'img._12etdsZfZbhUB46YDOgrB8').get_attribute('src')

        # Obtener imagen del héroe
        style_attr = hero.get_attribute("style")
        hero_img = style_attr.split('url("')[1].split('")')[0] if 'url("' in style_attr else ""

        # Obtener enlace sin duplicación
        link_page = hero.get_attribute("href")
        if not link_page.startswith("https"):
            link_page = "https://www.dota2.com" + link_page

        # Agregar a la lista
        heroes_data.append([name, attribute_img, hero_img, link_page])
    except Exception as e:
        print(f"⚠️ Error al procesar un héroe: {e}")

# Guardar en un archivo CSV con pandas
csv_filename = "dota2_heroes.csv"
df = pd.DataFrame(heroes_data, columns=["Nombre", "Atributo", "Imagen", "Pagina"])
df.to_csv(csv_filename, index=False, encoding="utf-8")

# Cerrar navegador
driver.quit()

print(f"✅ Scraping completado. Datos guardados en {csv_filename}")
