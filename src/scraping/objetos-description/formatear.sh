#!/bin/bash

# Nombre del archivo CSV de entrada y salida
INPUT_FILE="item.csv"
OUTPUT_FILE="output.csv"

# Crear el archivo de salida vacío
> "$OUTPUT_FILE"

# Procesar línea por línea
while IFS= read -r line || [[ -n "$line" ]]; do
    # Extraer la última columna correctamente, manejando comillas existentes
    last_column=$(echo "$line" | awk -F, '{print $NF}')
    
    # Verificar si la última columna ya tiene comillas al inicio y al final
    if [[ "$last_column" =~ ^\".*\"$ ]]; then
        echo "$line" >> "$OUTPUT_FILE"
    else
        # Agregar comillas a la última columna sin afectar las demás columnas
        modified_line=$(echo "$line" | sed -E 's/(.*),([^,]*)$/\1,"\2"/')
        echo "$modified_line" >> "$OUTPUT_FILE"
    fi

done < "$INPUT_FILE"

echo "Proceso completado. Se ha generado el archivo $OUTPUT_FILE con las correcciones necesarias."
