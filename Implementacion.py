
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

       