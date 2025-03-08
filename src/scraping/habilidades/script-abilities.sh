#!/bin/bash

# Verifica si se proporciona un archivo CSV como argumento
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <archivo_entrada.csv> <archivo_salida.csv>"
    exit 1
fi

input_file="$1"
output_file="$2"

# Usar awk para procesar el CSV y eliminar las barras invertidas dentro de las comillas dobles
awk -F, '{
    for (i=1; i<=NF; i++) {
        gsub(/\\/, "", $i)  # Elimina la barra invertida "\"
    }
    print $0
}' OFS=',' "$input_file" > "$output_file"

echo "Archivo procesado guardado en: $output_file"
