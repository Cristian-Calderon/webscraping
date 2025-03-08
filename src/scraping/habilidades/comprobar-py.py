import csv
import sys
import re

# Verificar que se proporciona un archivo CSV como argumento
if len(sys.argv) != 2:
    print("Uso: python validar_csv.py <archivo.csv>")
    sys.exit(1)

archivo_csv = sys.argv[1]
errores = 0

# Expresión regular para validar URLs de imágenes
regex_url = re.compile(r'^https?://.*\.(jpg|jpeg|png|gif|webp)$')

with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, quotechar='"')
    
    # Leer encabezado y omitirlo
    encabezado = next(reader)
    if len(encabezado) != 6:
        print("❌ Error: El encabezado no tiene 6 columnas.")
        sys.exit(1)

    # Validar filas
    for numero_linea, fila in enumerate(reader, start=2):  # Empieza en la línea 2
        if len(fila) != 6:
            print(f"Error en línea {numero_linea}: Faltan columnas o hay un problema con la estructura.")
            errores += 1
            continue

        id_habilidad, id_heroe, heroe, nombre_habilidad, descripcion, imagen = fila

        # Verificar si id_habilidad e id_heroe son números enteros
        if not id_habilidad.isdigit():
            print(f"Error en línea {numero_linea}: id_habilidad ('{id_habilidad}') no es un número válido.")
            errores += 1

        if not id_heroe.isdigit():
            print(f"Error en línea {numero_linea}: id_heroe ('{id_heroe}') no es un número válido.")
            errores += 1

        # Verificar si imagen tiene formato de URL válida
        if not regex_url.match(imagen):
            print(f"Error en línea {numero_linea}: La imagen ('{imagen}') no es una URL válida.")
            errores += 1

# Mostrar resumen de errores
if errores == 0:
    print("✅ Archivo correcto. Todas las filas cumplen con la estructura esperada.")
else:
    print(f"❌ Se encontraron {errores} errores en el archivo.")
