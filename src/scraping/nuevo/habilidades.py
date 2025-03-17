import json
import pandas as pd
import re
from playwright.sync_api import sync_playwright

habilidades_data = []
id_habilidad = 1

heroes = [
    ("Abaddon", "https://www.dota2.com/hero/abaddon"),
    ("Alchemist", "https://www.dota2.com/hero/alchemist"),
    ("Ancient Apparition", "https://www.dota2.com/hero/ancientapparition")
]

def extraer_json(page_content):
    pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    match = re.search(pattern, page_content)
    if match:
        return json.loads(match.group(1))
    return None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    for id_heroe, (nombre_heroe, url_heroe) in enumerate(heroes, start=1):
        print(f"🔍 Scraping habilidades de {nombre_heroe}...")

        page = context.new_page()
        page.goto(url_heroe, timeout=60000)
        page.wait_for_load_state('networkidle')

        html = page.content()
        json_data = extraer_json(html)

        if not json_data:
            print(f"⚠️ No se pudo extraer JSON para {nombre_heroe}")
            continue

        try:
            abilities = json_data['props']['pageProps']['hero']['abilities']
            for habilidad in abilities:
                nombre_habilidad = habilidad.get('name_loc', '').strip()
                descripcion_habilidad = habilidad.get('desc_loc', '').strip()
                imagen_habilidad = f"https://cdn.cloudflare.steamstatic.com{habilidad.get('icon', '')}"
                video_habilidad = habilidad.get('video_mp4', '').strip()

                habilidades_data.append([
                    id_habilidad, id_heroe, nombre_habilidad,
                    descripcion_habilidad, imagen_habilidad, video_habilidad
                ])

                print(f"✅ Habilidad extraída: {nombre_habilidad}")
                id_habilidad += 1

        except Exception as e:
            print(f"⚠️ Error procesando habilidades para {nombre_heroe}: {e}")

    browser.close()

# Guardar en CSV
habilidades_df = pd.DataFrame(habilidades_data, columns=[
    "id_habilidad", "id_heroe", "nombre_habilidad",
    "descripcion_habilidad", "imagen_habilidad", "video_habilidad"
])
habilidades_df.to_csv("habilidades_dota2_playwright.csv", index=False)

print("✅ Scraping finalizado correctamente usando Playwright.")
