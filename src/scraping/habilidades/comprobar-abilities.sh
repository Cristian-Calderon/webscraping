#!/bin/bash

# Verifica que se proporcione un archivo CSV como argumento
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <archivo.csv>"
    exit 1
fi

input_file="$1"
error_count=0

# Leer el archivo línea por línea usando awk para manejar correctamente las comas dentro de comillas
awk -F, 'NR > 1 {  # Ignorar la primera línea (encabezado)
    # Concatenar la línea actual con la anterior si hay un número impar de comillas dobles
    line = $0
    while (gsub(/"/, "\"", line) % 2 == 1 && (getline next_line > 0)) {
        line = line "\n" next_line
    }
    
    # Aplicar FPAT para dividir correctamente en 6 columnas
    split(line, fields, /,|("[^"]*")/)

    # Verificar que haya exactamente 6 campos
    if (length(fields) != 6) {
        print "Error en línea " NR ": Faltan columnas o hay un problema con la estructura."
        error_count++
        next
    }

    id_habilidad = fields[1]
    id_heroe = fields[2]
    heroe = fields[3]
    nombre_habilidad = fields[4]
    descripcion = fields[5]
    imagen = fields[6]

    # Eliminar comillas dobles alrededor de la descripción e imagen
    gsub(/^"|"$/, "", descripcion)
    gsub(/^"|"$/, "", imagen)

    # Verificar si id_habilidad e id_heroe son números enteros
    if (!(id_habilidad ~ /^[0-9]+$/)) {
        print "Error en línea " NR ": id_habilidad ('" id_habilidad "') no es un número válido."
        error_count++
    }
    if (!(id_heroe ~ /^[0-9]+$/)) {
        print "Error en línea " NR ": id_heroe ('" id_heroe "') no es un número válido."
        error_count++
    }

    # Verificar si imagen tiene formato de URL válida
    if (!(imagen ~ /^https?:\/\/.*\.(jpg|jpeg|png|gif|webp)$/)) {
        print "Error en línea " NR ": La imagen ('" imagen "') no es una URL válida."
        error_count++
    }

} END {
    # Mostrar resumen de errores
    if (error_count == 0) {
        print "✅ Archivo correcto. Todas las filas cumplen con la estructura esperada."
    } else {
        print "❌ Se encontraron " error_count " errores en el archivo."
    }
}' "$input_file"
