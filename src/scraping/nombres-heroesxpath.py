from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# Configuración del driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximiza la ventana para cargar todos los elementos
driver = webdriver.Chrome(options=options)

# URL de la página
url = "https://es.dotabuff.com/heroes"  # Cambia a la URL real
driver.get(url)
time.sleep(5)  # Espera para cargar la página completamente

# Aceptar el cuadro de privacidad si existe
try:
    agree_button = driver.find_element(By.XPATH, "//button[span[text()='AGREE']]")
    agree_button.click()
    print("Botón 'AGREE' encontrado y clicado.")
    time.sleep(2)
except Exception as e:
    print("No se encontró el botón de privacidad o ya fue aceptado:", e)

# Encuentra los elementos de nombres y enlaces de imágenes
try:
    # Modificamos el XPath para seleccionar el nombre directamente
    nombres_divs = driver.find_elements(By.XPATH, "//div[contains(@class,'tw-w-full') and contains(@class,'tw-text-center')]")
    # Imágenes asociadas
    imagenes = driver.find_elements(By.CSS_SELECTOR, "img.tw-relative.tw-size-full.tw-rounded-sm")

    # Verifica si se encontraron elementos
    print(f"Se encontraron {len(nombres_divs)} nombres y {len(imagenes)} imágenes.")

    data = []
    for index, (nombre_div, imagen) in enumerate(zip(nombres_divs, imagenes)):
        # Intenta obtener el texto del nombre
        nombre_texto = nombre_div.text.strip()

        # Verifica si el nombre está vacío
        if not nombre_texto:
            print(f"Elemento {index + 1}: Nombre vacío, intentando nuevamente...")
            nombre_texto = nombre_div.text.strip()

        # Obtenemos el enlace de la imagen
        link_imagen = imagen.get_attribute("src")

        # Depuración: imprime lo que encuentra
        print(f"Elemento {index + 1}: Nombre = '{nombre_texto}', Imagen = '{link_imagen}'")

        # Si los valores son válidos, los agrega a los datos
        if nombre_texto and link_imagen:
            data.append({"nombre": nombre_texto, "link-Imagen": link_imagen})

    # Guarda los datos en un CSV si se encontraron héroes
    if data:
        df = pd.DataFrame(data)
        df.to_csv("heroes.csv", index=False, encoding="utf-8")
        print("Scraping completado. Datos guardados en 'heroes.csv'.")
    else:
        print("No se encontraron datos válidos para guardar.")

except Exception as e:
    print("Ocurrió un error durante el scraping:", e)

# Cierra el navegador
driver.quit()
