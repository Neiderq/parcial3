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
        for ax in axes:
            ax.set_xlabel("mm")
            ax.set_ylabel("mm")

        plt.tight_layout()
        nombre_carpeta = os.path.basename(self.__carpeta.rstrip('/\\'))
        plt.savefig(f"{nombre_carpeta}_cortes.png")
        plt.show()

    def crear_paciente(self):
        if not self._slices or self._volumen is None:
            print("No hay datos cargados.")
            return None
        try:
            nombre = str(self.__slices[0].PatientName)
        except:
            nombre = "Desconocido"
        try:
            edad = str(self.__slices[0].PatientAge)
        except:
            edad = "Desconocida"
        try:
            id_paciente = str(self.__slices[0].PatientID)
        except:
            id_paciente = "Sin ID"
        paciente = Paciente(nombre, edad, id_paciente, self.__volumen)
        print(f"Paciente creado: {nombre}, Edad: {edad}, ID: {id_paciente}")
        return paciente
    
    def aplicar_traslacion(self):
        if self.__volumen is None:
            print("No hay volumen cargado.")
            return
        # Seleccionar un corte (por ejemplo, el corte central axial)
        imagen = self._volumen[self._volumen.shape[0] // 2, :, :]
        # Mostrar opciones de traslación al usuario
        opciones = {
            "1": (200, 100),
            "2": (-30, 100),
            "3": (0, -300),
            "4": (500, -200)
        }
        print("Opciones de traslación:")
        for k, (tx, ty) in opciones.items():
            print(f"{k}: tx={tx}, ty={ty}")

        opcion = input("Elige una opción (1-4): ").strip()
        if opcion not in opciones:
            print("Opción inválida.")
            return
        tx, ty = opciones[opcion]
        # Construir la matriz de traslación
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        rows, cols = imagen.shape
        trasladada = cv2.warpAffine(imagen, M, (cols, rows))
        # Mostrar original vs trasladada
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].imshow(imagen, cmap='gray')
        axs[0].set_title("Original")
        axs[0].axis('off')
        axs[1].imshow(trasladada, cmap='gray')
        axs[1].set_title(f"Trasladada tx={tx}, ty={ty}")
        axs[1].axis('off')
        plt.tight_layout()
        nombre_base = os.path.basename(self.__carpeta.rstrip("/\\"))
        # Guardar imagen trasladada y el subplot
        plt.savefig(f"{nombre_base}_subplot_traslacion.png")
        print("Imágenes guardadas correctamente.")
        plt.show()
class ImagenSencilla:
    def _init_(self, ruta_imagen):
        self.__ruta = ruta_imagen
        self.__imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        if self.__imagen is None:
            raise ValueError("No se pudo cargar la imagen o la ruta es inválida.")
        self.__nombre_tipo = None
        self.__umbral = None
        self.__binarizada = None
        self.__kernel_size = None
        self.__morfologica = None
        self.__resultado = None
    def get_nombre_archivo(self):
        return os.path.splitext(os.path.basename(self.__ruta))[0]
    
    def binarizar(self):
        opciones = {
            "1": ("BINARIO", cv2.THRESH_BINARY),
            "2": ("BINARIO INV", cv2.THRESH_BINARY_INV),
            "3": ("TRUNCADO", cv2.THRESH_TRUNC),
            "4": ("TOZERO", cv2.THRESH_TOZERO),
            "5": ("TOZERO INV", cv2.THRESH_TOZERO_INV)
        }
        print("Opciones de binarización:")
        for k, (nombre, _) in opciones.items():
            print(f"{k}: {nombre}")
        tipo = input("Elige tipo de binarización (1-5): ").strip()
        if tipo not in opciones:
            print("Opción inválida.")
            return None
        
        self.__nombre_tipo, tipo_binarizacion = opciones[tipo]
        self.__umbral = int(input("Ingrese valor de umbral (ej. 127): "))

        _, self.__binarizada = cv2.threshold(self.__imagen, self.__umbral, 255, tipo_binarizacion)
        return self.__binarizada
    
    def transformar_morfologicamente(self):
        self.__kernel_size = int(input("Ingrese tamaño de kernel (ej. 3 o 5): "))
        kernel = np.ones((self.__kernel_size, self.__kernel_size), np.uint8)
        self.__morfologica = cv2.morphologyEx(self.__binarizada, cv2.MORPH_CLOSE, kernel)
        return self.__morfologica
    def dibujar_forma_y_texto(self):
        self.__resultado = cv2.cvtColor(self.__morfologica, cv2.COLOR_GRAY2BGR)
        alto, ancho = self.__resultado.shape[:2]

        # Ahora: forma en la esquina superior izquierda
        forma = input("¿Qué forma quieres dibujar? (circulo/cuadro): ").lower()
        if forma == "circulo":
            centro = (80, 80)  # Cercano al texto
            cv2.circle(self.__resultado, centro, 200, (0, 255, 0), 2)
        elif forma == "cuadro":
            esquina1 = (10, 10)
            esquina2 = (300, 300)
            cv2.rectangle(self.__resultado, esquina1, esquina2, (255, 0, 0), 2)
        texto = f"Imagen binarizada\nUmbral: {self.__umbral}, Kernel: {self.__kernel_size}"
        y0 = 30
        for i, linea in enumerate(texto.split('\n')):
            y = y0 + i * 30
            cv2.putText(self.__resultado, linea, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        return self.__resultado
