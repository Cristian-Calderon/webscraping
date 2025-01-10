from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configura el controlador de Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL del sitio web
url = 'https://es.dotabuff.com/heroes'

# Abre la página
driver.get(url)

# Encuentra todos los elementos <a> con el XPath
xpath = "//div[contains(@class,'tw-w-full') and contains(@class,'tw-text-center')]/text()"
heroes = driver.find_elements(By.XPATH, xpath)

# Muestra el texto de cada hero
for hero in heroes:
    print(hero.text)

# Cierra el navegador
driver.quit()
