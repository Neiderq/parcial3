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
class DICOM:
    def _init_(self, carpeta):
        self.__carpeta = carpeta #Carpeta donde están almacenados los archivos
        self.__slices = [] #Almacena cada archivo tipo DICOM (corte)
        self.__volumen = None #Reconstrucción 3d a partir de imágenes 2d

    def cargar_cortes(self):
        archivos = [f for f in os.listdir(self.__carpeta) if f.endswith('.dcm')]
        # Leer todos los archivos DICOM dirRemove-Item -Recurse -Force .gitectamente
        self._slices = [pydicom.dcmread(os.path.join(self._carpeta, archivo)) for archivo in archivos]
    # Ordenar los cortes por posición Z
        self._slices = sorted(self._slices, key=lambda x: float(x.ImagePositionPatient[2]))
        # Apilar las imágenes para construir el volumen 3D
        self._volumen = np.stack([s.pixel_array for s in self._slices], axis=0)
        print("Carga y reconstrucción 3D completadas.")
    
    def procesar_y_guardar(self, diccionario_imagenes):
        self.cargar_cortes()
        clave = os.path.basename(self.__carpeta)
        diccionario_imagenes[clave] = self
        print(f"Guardado en el diccionario con clave '{clave}'.")

    def get_volumen(self):
        return self.__volumen

    def get_slices(self):
        return self.__slices
    
    def mostrar_cortes(self):
        if self.__volumen is None:
            print("Volumen no cargado.")
            return
         try:
            spacing_xy = self.__slices[0].PixelSpacing  # [dy, dx]
            spacing_z = float(self.__slices[0].SliceThickness)
        except:
            spacing_xy = [1.0, 1.0]
            spacing_z = 1.0
        dz, dy, dx = spacing_z, spacing_xy[0], spacing_xy[1]
        medio_z = self.__volumen.shape[0] // 2
        medio_y = self.__volumen.shape[1] // 2
        medio_x = self.__volumen.shape[2] // 2
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Corte transversal (Z)
        axes[0].imshow(
            self.__volumen[medio_z, :, :],
            cmap='gray',
            extent=[0, dx * self._volumen.shape[2], 0, dy * self._volumen.shape[1]])
        axes[0].set_title("Transversal")

        # Corte coronal (Y)
        axes[1].imshow(
            self.__volumen[:, medio_y, :],
            cmap='gray',
            extent=[0, dx * self._volumen.shape[2], 0, dz * self._volumen.shape[0]]
        )
        axes[1].set_title("Coronal")

        # Corte sagital (X)
        axes[2].imshow(
            self.__volumen[:, :, medio_x],
            cmap='gray',
            extent=[0, dy * self._volumen.shape[1], 0, dz * self._volumen.shape[0]]
        )
        axes[2].set_title("Sagital")


    
       