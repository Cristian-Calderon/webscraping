from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configuración de opciones para Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Ejemplo: abrir navegador maximizado

# Configurar el servicio de ChromeDriver
service = Service(ChromeDriverManager().install())

# Iniciar el navegador con las opciones configuradas
driver = webdriver.Chrome(service=service, options=chrome_options)

# Abrir Google
driver.get("https://www.dotabuff.com/players/110208369")

# Imprimir el título de la página
print("Título de la página:", driver.title)

# Cerrar el navegador
driver.quit()
