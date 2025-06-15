
from Clases import *
import pydicom
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# Diccionarios globales
diccionario_pacientes = {}
diccionario_imagenes = {}

def main():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Procesar carpeta DICOM")
        print("2. Crear paciente desde DICOM cargado")
        print("3. Cargar imagenes JPG o PNG")
        print("4. Trasladar imágen DICOM")
        print("5. Realizar transformación geométrica (cierre)")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            carpeta = input("Ingrese la ruta de la carpeta DICOM: ").strip()
            if not os.path.isdir(carpeta):
                print("Ruta inválida.")
                continue
            dicom_obj = DICOM(carpeta)
            dicom_obj.procesar_y_guardar(diccionario_imagenes)
            print(diccionario_imagenes)

            # Mostrar cortes reconstruidos en un subplot
            dicom_obj.mostrar_cortes()

        elif opcion == '2':
            if not diccionario_imagenes:
                print("Primero debe procesar una carpeta DICOM (opción 1).")
                continue
            print("Claves disponibles en diccionario de imágenes:")
            for clave in diccionario_imagenes.keys():
                print(f" - {clave}")
            clave = input("Ingrese la clave del DICOM para crear el paciente: ").strip()
            if clave not in diccionario_imagenes:
                print("Clave no encontrada.")
                continue
            dicom_obj = diccionario_imagenes[clave]
            paciente = dicom_obj.crear_paciente()
            if paciente:
                diccionario_pacientes[paciente.get_id()] = paciente
                print(f"Paciente guardado con ID: {paciente.get_id()}")    
                print(diccionario_pacientes)

        elif opcion == '3':
            ruta = input("Ingrese la ruta de la imagen JPG o PNG: ").strip()
            if not os.path.isfile(ruta):
                print("Ruta no válida.")
                continue

            try:
                imagen = ImagenSencilla(ruta)  # Crea el objeto de la clase ya definida
                clave = imagen.get_nombre_archivo()  # Nombre de archivo como clave
                diccionario_imagenes[clave] = imagen
                print(f"Imagen cargada y almacenada con la clave '{clave}' en el diccionario de imágenes.")
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
        elif opcion == '4':
            if not diccionario_imagenes:
                print("Primero debe procesar una carpeta DICOM (opción 1).")
                continue

            print("Claves disponibles en el diccionario de imágenes:")
            for clave in diccionario_imagenes.keys():
                print(f" - {clave}")

            clave = input("Ingrese la clave de la imagen para aplicar traslación: ").strip()
            if clave not in diccionario_imagenes:
                print("Clave no encontrada.")
                continue

            dicom_obj = diccionario_imagenes[clave]
            dicom_obj.aplicar_traslacion()
        elif opcion == '5':
            ruta = input("Ingrese la ruta de la imagen JPG o PNG: ").strip()
            if not os.path.isfile(ruta):
                print("Ruta inválida o archivo no encontrado.")
                continue

            try:
                imagen_obj = ImagenSencilla(ruta)
                imagen_obj.procesar_completo()

                clave = input("Ingrese una clave para guardar esta imagen en el diccionario: ").strip()
                diccionario_imagenes[clave] = imagen_obj
                print(diccionario_imagenes)
                print(f"Imagen procesada y guardada bajo la clave '{clave}'.")
                continue
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
            break
        elif opcion == '6':
            break
            
        else:
            print("Opción inválida.")
            continue

if __name__ == "__main__":
    main()