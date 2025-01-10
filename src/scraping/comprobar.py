from selenium import webdriver
from selenium.webdriver.common.by import By

# Configuración del navegador (Chrome en este caso)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Opcional: Ejecuta en modo headless (sin abrir ventana)
options.add_argument("--no-sandbox")  # Para evitar problemas en entornos restringidos
options.add_argument("--disable-dev-shm-usage")  # Mejora la estabilidad en entornos con recursos limitados

# Asegúrate de usar la ruta correcta para ChromeDriver si no está en tu PATH
driver = webdriver.Chrome(options=options)

# URL que vamos a visitar
url = "https://www.google.com"
driver.get(url)

# Obtén el título de la página
titulo = driver.title

# Cierra el navegador
driver.quit()

# Imprime el título
print(f"El título de la página es: '{titulo}'")
