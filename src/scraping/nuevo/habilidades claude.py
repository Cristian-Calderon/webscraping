import time
import pandas as pd
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en segundo plano
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")  # Tamaño de ventana más grande
chrome_options.add_argument("--disable-web-security")  # Desactivar restricciones de seguridad web

# Inicializar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)

# Lista para almacenar habilidades extraídas
habilidades_data = []
id_habilidad = 1

# Función para buscar texto en el HTML que contenga posibles nombres de habilidades
def extraer_posibles_nombres_habilidades(html):
    # Buscar patrones que podrían ser nombres de habilidades (en mayúsculas, con espacios)
    # Ejemplos: "MIST COIL", "APHOTIC SHIELD", etc.
    patrones = [
        # Patrón para nombres de habilidades estándar (palabras en mayúsculas)
        r'"ability_name"[^>]*>([A-Z][A-Z\s\']+)<\/div>',
        r'"ability_name"[^>]*>([A-Z][A-Z\s\']+)<\/h',
        r'"skill_name"[^>]*>([A-Z][A-Z\s\']+)<\/div>',
        r'"skill_name"[^>]*>([A-Z][A-Z\s\']+)<\/h',
        r'<div[^>]*class="[^"]*name[^"]*"[^>]*>([A-Z][A-Z\s\']+)<\/div>',
        r'<h\d[^>]*class="[^"]*name[^"]*"[^>]*>([A-Z][A-Z\s\']+)<\/h\d>',
        # Patrón para buscar en etiquetas que podrían contener nombres
        r'<div[^>]*>([A-Z][A-Z\s\']{3,})<\/div>',
        r'<h\d[^>]*>([A-Z][A-Z\s\']{3,})<\/h\d>',
        r'<span[^>]*>([A-Z][A-Z\s\']{3,})<\/span>',
        # Buscar en atributos
        r'alt="([A-Z][A-Z\s\']+)"',
        r'title="([A-Z][A-Z\s\']+)"',
        # Buscar en scripts para datos embebidos
        r'"ability_name"\s*:\s*"([A-Z][A-Z\s\']+)"',
        r'"name"\s*:\s*"([A-Z][A-Z\s\']+)"',
    ]
    
    nombres_encontrados = []
    for patron in patrones:
        matches = re.findall(patron, html)
        for match in matches:
            if 5 < len(match) < 30 and match not in ["ABILITY TOOLTIP", "TALENTS", "AGHANIM'S SHARD", "AGHANIM'S SCEPTER"]:
                nombres_encontrados.append(match)
    
    return nombres_encontrados

# Función para extraer datos JSON embebidos en la página
def extraer_json_embebido(html):
    try:
        # Buscar patrones de datos JSON embebidos
        json_patterns = [
            r'<script\s+id="abilities"\s+type="application/json">(.*?)<\/script>',
            r'<script\s+type="application/json"\s+id="abilities">(.*?)<\/script>',
            r'window\.abilities\s*=\s*({.*?});',
            r'var\s+abilities\s*=\s*({.*?});',
            r'{\s*"abilities"\s*:\s*\[(.*?)\]}'
        ]
        
        for pattern in json_patterns:
            matches = re.search(pattern, html, re.DOTALL)
            if matches:
                json_data = matches.group(1)
                try:
                    # Intentar parsear como JSON
                    return json.loads(json_data)
                except:
                    pass
    except Exception as e:
        print(f"Error al extraer JSON: {e}")
    
    return None

# Lista de héroes y sus URLs en Dota2
heroes = [
    ("Abaddon", "https://www.dota2.com/hero/abaddon"),
    ("Alchemist", "https://www.dota2.com/hero/alchemist"),
    ("Ancient Apparition", "https://www.dota2.com/hero/ancientapparition")
]

# Modo de depuración para ver el HTML
DEBUG = True
DEBUG_OUTPUT_FILE = "dota2_debug_output.txt"

if DEBUG:
    with open(DEBUG_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== INICIO DE DEPURACIÓN ===\n")

# 🔍 Iterar sobre los héroes
for id_heroe, (nombre_heroe, url_heroe) in enumerate(heroes, start=1):
    print(f"🔍 Scraping habilidades de {nombre_heroe}...")

    # Abrir la página del héroe
    driver.get(url_heroe)
    
    # Esperar a que la página cargue completamente
    time.sleep(7)  # Aumentado para asegurar carga completa
    
    # Obtener el HTML completo de la página para análisis inicial
    html_inicial = driver.page_source
    
    if DEBUG:
        with open(DEBUG_OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== HTML INICIAL PARA {nombre_heroe} ===\n")
            f.write(html_inicial[:10000])  # Guardar solo los primeros 10000 caracteres
    
    # Intentar extraer datos JSON embebidos
    json_data = extraer_json_embebido(html_inicial)
    if json_data:
        print("✅ Encontrados datos JSON embebidos en la página.")
        if DEBUG:
            with open(DEBUG_OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== DATOS JSON PARA {nombre_heroe} ===\n")
                f.write(str(json_data)[:2000])
    
    # Buscar nombres de habilidades en el HTML inicial
    posibles_nombres_inicial = extraer_posibles_nombres_habilidades(html_inicial)
    if posibles_nombres_inicial:
        print(f"✅ Nombres extraídos del HTML inicial: {posibles_nombres_inicial}")
        if DEBUG:
            with open(DEBUG_OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== NOMBRES EXTRAÍDOS DEL HTML INICIAL PARA {nombre_heroe} ===\n")
                f.write(str(posibles_nombres_inicial))
    
    # Obtener todos los botones de habilidades
    botones_habilidades = driver.find_elements(By.CSS_SELECTOR, "div._3Chop4A9yz7Af_BwR1r_NW")
    
    if not botones_habilidades:
        print(f"⚠️ No se encontraron habilidades en {url_heroe}.")
        continue

    print(f"✅ {len(botones_habilidades)} botones de habilidades encontrados para {nombre_heroe}.")
    
    # Lista para almacenar información de habilidades detectadas
    habilidades_detectadas = []
    
    # Iterar sobre los botones de habilidades
    for i, boton in enumerate(botones_habilidades):
        try:
            print(f"Procesando botón de habilidad {i+1}...")
            
            # Hacer scroll al botón para asegurarse que es visible
            driver.execute_script("arguments[0].scrollIntoView(true);", boton)
            time.sleep(1)
            
            # Sacar captura del DOM antes del clic para comparar después
            html_antes = driver.page_source
            
            # Hacer clic en el botón
            driver.execute_script("arguments[0].click();", boton)
            time.sleep(3)  # Espera considerable para que se actualice la interfaz
            
            # Obtener el HTML después del clic
            html_despues = driver.page_source
            
            if DEBUG and i == 0:  # Solo guardamos el primer botón para no llenar el archivo
                with open(DEBUG_OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write(f"\n\n=== HTML DESPUÉS DE CLIC EN BOTÓN {i+1} PARA {nombre_heroe} ===\n")
                    f.write(html_despues[:10000])
            
            # Buscar nombres de habilidades en el HTML después del clic
            posibles_nombres = extraer_posibles_nombres_habilidades(html_despues)
            
            # Filtrar nombres que ya estaban en el HTML inicial
            nombres_nuevos = [n for n in posibles_nombres if n not in posibles_nombres_inicial]
            
            print(f"Posibles nombres después del clic: {posibles_nombres}")
            print(f"Nombres nuevos después del clic: {nombres_nuevos}")
            
            if nombres_nuevos:
                nombre_habilidad = nombres_nuevos[0]
                print(f"✅ Nombre extraído después del clic: {nombre_habilidad}")
            else:
                # Si no hay nuevos, usar cualquier nombre disponible
                if posibles_nombres:
                    nombre_habilidad = posibles_nombres[0]
                    print(f"⚠️ Usando nombre existente: {nombre_habilidad}")
                else:
                    nombre_habilidad = f"{nombre_heroe}_Ability_{i+1}"
                    print(f"⚠️ No se encontró nombre. Usando genérico: {nombre_habilidad}")
            
            # Extraer descripción de la habilidad
            descripcion_habilidad = ""
            desc_selectores = [
                "div.CjmI9ZAN4c9C4Rj-IPpzc", 
                "div.ability_description",
                "div.description",
                "//div[contains(@class, 'description')]"
            ]
            
            for selector in desc_selectores:
                try:
                    if selector.startswith("//"):
                        elementos = driver.find_elements(By.XPATH, selector)
                    else:
                        elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elementos and elementos[0].text.strip():
                        descripcion_habilidad = elementos[0].text.strip()
                        break
                except:
                    continue
            
            # Extraer imagen de la habilidad
            imagen_habilidad = ""
            try:
                img_featured = driver.find_element(By.CSS_SELECTOR, "img._171zqqZ6uSu-ZpGvphLmVH")
                imagen_habilidad = img_featured.get_attribute("src")
            except:
                try:
                    # Método alternativo: buscar cualquier imagen relevante
                    imgs = driver.find_elements(By.TAG_NAME, "img")
                    for img in imgs:
                        src = img.get_attribute("src")
                        if "abilities" in src.lower() or "spells" in src.lower():
                            imagen_habilidad = src
                            break
                except:
                    pass
            
            # Extraer video de la habilidad
            video_habilidad = ""
            try:
                videos = driver.find_elements(By.TAG_NAME, "video")
                if videos:
                    sources = videos[0].find_elements(By.TAG_NAME, "source")
                    if sources:
                        video_habilidad = sources[0].get_attribute("src")
            except:
                pass
            
            # Guardar los datos en la lista
            habilidades_data.append([
                id_habilidad, id_heroe, nombre_habilidad, descripcion_habilidad, imagen_habilidad, video_habilidad
            ])
            print(f"✅ Extraída habilidad {i+1}: {nombre_habilidad} para {nombre_heroe}")
            
            habilidades_detectadas.append(nombre_habilidad)
            id_habilidad += 1
        
        except Exception as e:
            print(f"⚠️ Error al procesar botón {i+1}: {str(e)}")
    
    print(f"Habilidades detectadas para {nombre_heroe}: {habilidades_detectadas}")
    
    # Pausa entre héroes
    time.sleep(3)

# Cerrar el navegador
driver.quit()

# Guardar en CSV
habilidades_df = pd.DataFrame(habilidades_data, columns=["id_habilidad", "id_heroe", "nombre_habilidad", "descripcion_habilidad", "imagen_habilidad", "video_habilidad"])
habilidades_df.to_csv("habilidades_3_heroes_avanzado.csv", index=False)

print("✅ Scraping finalizado. Datos guardados en habilidades_3_heroes_avanzado.csv")
print(f"Total de habilidades extraídas: {len(habilidades_data)}")
print(f"✅ Se ha creado un archivo de depuración en {DEBUG_OUTPUT_FILE}")