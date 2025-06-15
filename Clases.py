import pydicom
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

#Clase para crear objetos tipo paciente extraidos de los archivos tipo DICOM
class Paciente:
    def __init__(self, nombre, edad, id_paciente, imagen_asociada):
        self._nombre = nombre
        self._edad = edad
        self._id_paciente = id_paciente
        self._imagen_asociada = imagen_asociada # Matriz 3D ( volumen DICOM)

    def get_id(self):
        return self._id_paciente
    def get_nombre(self):
        return self._nombre
    def get_edad(self):
        return self._edad
    def get_imageN(self):
        return self._imagen_asociada
    def mostrar_info(self):
        print(f"Nombre: {self._nombre}")
        print(f"Edad: {self._edad}")
        print(f"ID Paciente: {self._id_paciente}") 
       