import csv

# Ruta del archivo CSV
input_file = "dota_heroes_abilities_o.csv"

# Parámetros esperados
COLUMNAS_ESPERADAS = 6

# Listas para almacenar errores encontrados
errores_columnas = []
errores_comillas = []
errores_imagenes = []
errores_campos_vacios = []

# Verificación del CSV
with open(input_file, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile, delimiter=",", quotechar='"')
    header = next(reader)  # Saltar la cabecera

    for i, row in enumerate(reader, start=2):  # Comienza desde la fila 2 por la cabecera
        # Comprobar número de columnas
        if len(row) != COLUMNAS_ESPERADAS:
            errores_columnas.append((i, row))

        # Comprobar si las comillas están desbalanceadas
        if row.count('"') % 2 != 0:
            errores_comillas.append((i, row))

        # Verificar si la columna "Imagen" está vacía
        if len(row) == COLUMNAS_ESPERADAS and not row[-1].strip():
            errores_imagenes.append((i, row))

        # Verificar si hay campos vacíos en columnas clave
        columnas_clave = [0, 1, 2, 3]  # ID, Héroe, Nombre de Habilidad
        if any(not row[idx].strip() for idx in columnas_clave):
            errores_campos_vacios.append((i, row))

# Resultado del análisis
print("✅ Verificación completa del archivo CSV")
print(f"🚨 Filas con número incorrecto de columnas: {len(errores_columnas)}")
print(f"🚨 Filas con comillas desbalanceadas: {len(errores_comillas)}")
print(f"🚨 Filas con la columna 'Imagen' vacía: {len(errores_imagenes)}")
print(f"🚨 Filas con campos vacíos en columnas clave: {len(errores_campos_vacios)}")

# Mostrar ejemplos de errores
if errores_columnas:
    print("\n🔎 Ejemplo de error en número de columnas:")
    for error in errores_columnas[:5]:
        print(f"Fila {error[0]}: {error[1]}")

if errores_comillas:
    print("\n🔎 Ejemplo de error en comillas desbalanceadas:")
    for error in errores_comillas[:5]:
        print(f"Fila {error[0]}: {error[1]}")

if errores_imagenes:
    print("\n🔎 Ejemplo de error en imágenes vacías:")
    for error in errores_imagenes[:5]:
        print(f"Fila {error[0]}: {error[1]}")

if errores_campos_vacios:
    print("\n🔎 Ejemplo de error en campos vacíos:")
    for error in errores_campos_vacios[:5]:
        print(f"Fila {error[0]}: {error[1]}")
