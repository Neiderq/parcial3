
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
       

       