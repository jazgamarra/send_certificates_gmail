import os
import csv

# Rutas - Modificar aqui 
carpeta_pdf = r'C:\\ ... \\carpera_certificados'
ruta_csv = r'C:\ ... \\renombrar.csv'


# Leer el archivo CSV y crear un diccionario de correspondencia de nombres
correspondencia_nombres = {}
with open(ruta_csv, 'r') as archivo_csv:
    lector_csv = csv.reader(archivo_csv)
    for fila in lector_csv:
        if len(fila) >= 2:
            nombre_nuevo, nombre_actual = fila
            correspondencia_nombres[nombre_actual] = nombre_nuevo

print(correspondencia_nombres)

# Recorrer los archivos en la carpeta y renombrar según la correspondencia
for nombre_actual in os.listdir(carpeta_pdf):
    if nombre_actual.endswith('.pdf') and nombre_actual.startswith('certificados-'):
        nombre_sin_extension = os.path.splitext(nombre_actual)[0]
        # print(nombre_actual, nombre_sin_extension, correspondencia_nombres[nombre_sin_extension])

        if nombre_sin_extension in correspondencia_nombres:
            nombre_nuevo = correspondencia_nombres[nombre_sin_extension] + '.pdf'
            ruta_antigua = os.path.join(carpeta_pdf, nombre_actual)
            ruta_nueva = os.path.join(carpeta_pdf, nombre_nuevo)
            
            try:
                os.rename(ruta_antigua, ruta_nueva)
                print(f"Renombrado: {nombre_actual} -> {nombre_nuevo}")
            except OSError as e:
                print(f"\033[93m" + "Error al renombrar {nombre_actual}: {e}" + "\033[0m") 

        else:
            print(f"Correspondencia no encontrada para {nombre_actual}")
    else:
        print(f"Archivo no válido: {nombre_actual}")
