import matplotlib.pyplot as plt
from skimage import io, img_as_ubyte
import numpy as np
import cv2
from glob import glob
import os
import interfaz
from celda import Celda

# Función que devuelve la sección de la imagen correspondiente a la muestra en la posición (i, j) de la grilla
def obtener_imagen_celda(img, i, j, alto_celda, ancho_celda): # fila, columna (empieza en 1)
    if len(img.shape) == 3:
        new_img = img[int(alto_celda*(i-1)):int(alto_celda*i), int(ancho_celda*(j-1)):int(ancho_celda*j), :]
    elif len(img.shape) == 2:
        new_img = img[int(alto_celda*(i-1)):int(alto_celda*i), int(ancho_celda*(j-1)):int(ancho_celda*j)]        
    return new_img

# Función que detecta los círculos en la imagen. Se deben tunear param1 y param2 para reducir FN y/o FP. 
# Así mismo, minRadius y maxRadius se tunean dependiendo del tamaño de la grilla y muestras utilizadas. 
def obtener_circulos(imagen, param1=100, param2=8, minRadius=10, maxRadius=16, plotear=False):
    
    # se copia para no alterar la imagen original
    imagen = imagen.copy()
    imagen = img_as_ubyte(imagen)

    circulos = cv2.HoughCircles(imagen, cv2.HOUGH_GRADIENT, 1, 20, 
                                param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    #print(circulos)
    # Si se detectan círculos...
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for i in circulos[0, :]:
            #print(i)
            # Dibujar el círculo y su centro
            cv2.circle(imagen, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(imagen, (i[0], i[1]), 2, (0, 0, 255), 3)

    if plotear:
        plt.imshow(imagen)
        plt.show()

    if len(circulos) > 1:
        print('Se detectaron más de un circulo')
        return None
    elif len(circulos) == 0:
        print('No se detectaron circulos')
        return None

    return circulos[0,0]

def plot(img):
    plt.imshow(img)
    plt.axis('off') 
    plt.show()

def calcular_intensidad(img, circulo, metodo = None):
    i, j, r = circulo
    # se toma la ventana de interes (el cuadrado que enmarca el circulo detectado)
    ventana = img[j-r:j+r, i-r:i+r, 1] # solo se toman las intensidades del canal G (verde)
    #plot(ventana)
    intensidades_ordenadas = np.sort(ventana.flatten())
    intensidad = 0  
    
    if metodo == 'media':    
        intensidad = np.mean(intensidades_ordenadas)
    elif metodo == 'maximo':
        intensidad = intensidades_ordenadas[-1]
    else:
        # se toma el promedio de la mitad mayor de las intensidades ordenadas
        intensidad = np.mean(intensidades_ordenadas[len(intensidades_ordenadas)//2:])

    return intensidad

def graficar_intensidad_tiempo(celdas):
    """
    Función que grafica la intensidad promedio de cada celda en función del tiempo.
    """
    plt.figure(figsize=(12, 8))
    
    # Por cada celda en celdas_datos
    for celda in celdas:
        intensidades = celda.intensidades
        plt.plot(intensidades, label=f"Celda {celda.coordenada}, {celda.tipo}")
    
    plt.title("Intensidad promedio por celda en función del tiempo")
    plt.xlabel("Tiempo")
    plt.ylabel("Intensidad promedio")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()

def sort_key_func(item):
    return int(item.split('_')[-1].split('.png')[0])

def main():

    #PARAMETROS MANUALES
    
    # Para una gradilla 4x8 eran:
    # pixel_x_1, pixel_y_1 = 120, 135 # esquina superior izquierda de la imagen recortada
    # pixel_x_2, pixel_y_2 = 375, 345 # esquina inferior derecha de la imagen recortada
    #img_inicial_gris = img_inicial_gris[135:345, 120:570] # imagen recortada
    pixel_x_1, pixel_y_1 = 120, 80 # esquina superior izquierda de la imagen recortada
    pixel_x_2, pixel_y_2 = 620, 345 # esquina inferior derecha de la imagen recortada
    dimension_x, dimension_y = 9, 5 # dimensiones de la grilla de muestras (8 columnas y 4 filas)

    data = sorted(glob(os.path.join('data', 'data-img_44', 'img*.png')), key=sort_key_func)[1:]


    # ETAPA 1: DETECCION DE CELDAS
    # pedir al usuario las celdas seleccionadas
    coordenadas_seleccionadas = interfaz.main()
    print(coordenadas_seleccionadas)
    
    celdas = []

    for tipo, coordenadas in coordenadas_seleccionadas.items():
        if coordenadas is not None:
            if type(coordenadas) == list:
                for coordenada in coordenadas:
                    nueva_celda = Celda(tipo, coordenada)
                    celdas.append(nueva_celda)
            # esto pasa cuando CP o CN solo puedo tener un valor, y no está en un singleton sino que es una tupla.
            elif type(coordenadas) == tuple:
                nueva_celda = Celda(tipo, coordenadas)
                celdas.append(nueva_celda)

    # se obtiene la imagen inicial en gris porque se requiere para la detección de circulos
    img_inicial_gris = io.imread(data[0], as_gray=True) 
    img_inicial_gris = img_inicial_gris[pixel_y_1:pixel_y_2, pixel_x_1:pixel_x_2] # imagen recortada
    alto_img, ancho_img = img_inicial_gris.shape[0], img_inicial_gris.shape[1] # ancho y alto (en pixeles) de la imagen recortada
    alto_celda, ancho_celda = (alto_img/dimension_y), (ancho_img/dimension_x)
    

    # para cada celda seleccionada, detectar el circulo correspondiente
    for celda in celdas:
        i, j = celda.coordenada
        img_celda = obtener_imagen_celda(img_inicial_gris, i, j, alto_celda, ancho_celda)
        circulo = obtener_circulos(img_celda, plotear=False)
        celda.circulo = circulo
    
    # ETAPA 2: RECOLECCION DE DATOS
    
    #data = glob(os.path.join('data','*.png'))
    #data = sorted(glob(os.path.join('data', 'data-img_44', 'img*.png')), key=sort_key_func)[1:]
    
    # proceso respecto al tiempo
    #for t, ruta_imagen in enumerate(data): # útil en caso de necesitar el tiempo (discreto empezando en 0) de cada imagen en el dataset
    for ruta_imagen in data:
        im = io.imread(ruta_imagen)
        #print(im.shape)
        # se recorta la imagen 

        im = im[pixel_y_1:pixel_y_2, pixel_x_1:pixel_x_2, :] # imagen recortada     
        #print(im.shape)
        # estoy en una imagen especifica en un determinado t
        for celda in celdas:
            # obtener los valores de la imagen consultando el circulo
            circulo = celda.circulo
            i, j = celda.coordenada
            img_celda = obtener_imagen_celda(im, i, j, alto_celda, ancho_celda)
            #print(img_celda.shape)
            valor = calcular_intensidad(img_celda, circulo)
            celda.agregar_intensidad(valor)

    # ETAPA 3: GRAFICAR CADA CELDA CON FUNCIÓN DEL TIEMPO
    graficar_intensidad_tiempo(celdas)


if __name__ == "__main__":
    main()
    
# AL FINAL
# TODO: lanzar como un ejecutable (.exe) para comodidad en vez de tener que instalar librerías y ejecutar desde consola 
# TODO: al final del proyecto: revisar versiones de librerías y colocarlas en requirements.txt
# TODO: añadir licencia

# TODO: tomar solo intensidades mayores
# TODO: calcular y graficar threshold (pedir un porcentaje al usuario)
# TODO: graficar controlPos y controlNeg
# TODO: reducir ruido
# TODO: interfaz sea user-friendly
# TODO: dos CP y dos CN
# TODO: comentar adecuadamente el código
# TODO: comprobar grafica con ejemplo de dataset
# TODO: importar información a Excel
# TODO: permitir múltiples CP y CN
# TODO: garantizar una sola detección en get_circle
# TODO: manejo de errores: si no se detecta un único circulo        
# TODO: permitir nombrar? cada celda seleccionada
# TODO: intensidad en solo canal verde?
