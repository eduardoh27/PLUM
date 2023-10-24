import matplotlib.pyplot as plt
from skimage import io, img_as_ubyte
import numpy as np
import cv2
from glob import glob
import os
import interfaz


# Función que devuelve la sección de la imagen correspondiente a la muestra en la posición (i, j) de la grilla
def obtener_celda(img, i, j, alto_celda, ancho_celda): # fila, columna (empieza en 1)
    if len(img.shape) == 3:
        new_img = img[int(alto_celda*(i-1)):int(alto_celda*i), int(ancho_celda*(j-1)):int(ancho_celda*j), :]
    elif len(img.shape) == 2:
        new_img = img[int(alto_celda*(i-1)):int(alto_celda*i), int(ancho_celda*(j-1)):int(ancho_celda*j)]        
    return new_img


# Función que detecta los círculos en la imagen. Se deben tunear param1 y param2 para reducir FN y/o FP. 
# Así mismo, minRadius y maxRadius se tunean dependiendo del tamaño de la grilla y muestras utilizadas. 
def obtener_circulos(imagen, param1=100, param2=8, minRadius=10, maxRadius=16, imprimir=False):
    
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

    if imprimir:
        plt.imshow(imagen)
        plt.show()

    return circulos[0,0]

def plot(img):
    plt.imshow(img)
    plt.axis('off') 
    plt.show()

def calcular_intensidad_promedio(img, circulo):
    i, j, r = circulo
    segmento = img[j-r:j+r, i-r:i+r]    
    #plot(segmento)
    return np.mean(segmento) # canal G

def graficar_intensidad_tiempo(celdas_datos):
    """
    Función que grafica la intensidad promedio de cada celda en función del tiempo.
    """
    plt.figure(figsize=(12, 8))
    
    # Por cada celda en celdas_datos
    for celda, datos in celdas_datos.items():
        intensidades = datos[1]
        plt.plot(intensidades, label=f"Celda {celda}")
    
    plt.title("Intensidad promedio por celda en función del tiempo")
    plt.xlabel("Tiempo")
    plt.ylabel("Intensidad promedio")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

def sort_key_func(item):
    return int(item.split('_')[-1].split('.png')[0])


def main():

    # ETAPA 1: DETECCION DE CELDAS
    # pedir al usuario las celdas seleccionadas
    celdas_seleccionadas = interfaz.main()['Celdas']
    print(celdas_seleccionadas)
    #celdas_seleccionadas = [(1,1), (1,2)]
    # se inicializa la estructura con la información de cada celda en el tiempo
    celdas_datos = {celda:[None,[]] for celda in celdas_seleccionadas} #celdas_data = {(1,1):[None,[]], (1,2):[None,[]]}
 
    # se obtiene la imagen inicial en gris porque se requiere para la detección de circulos
    img_inicial_gris = io.imread('img_44.PNG', as_gray=True) 
    img_inicial_gris = img_inicial_gris[135:345, 120:570] # imagen recortada
    dimension_x, dimension_y = 8, 4 # dimensiones de la grilla de muestras (8 columnas y 4 filas)
    alto_img, ancho_img = img_inicial_gris.shape[0], img_inicial_gris.shape[1] # ancho y alto (en pixeles) de la imagen recortada
    alto_celda, ancho_celda = (alto_img/dimension_y), (ancho_img/dimension_x)
    

    # para cada celda seleccionada, detectar el circulo correspondiente
    for celda in celdas_datos.keys():
        i, j = celda
        img_celda = obtener_celda(img_inicial_gris, i, j, alto_celda, ancho_celda)
        circulo = obtener_circulos(img_celda, imprimir=False)
        celdas_datos[celda][0] = circulo
    
    
    # ETAPA 2: RECOLECCION DE DATOS
    
    #data = glob(os.path.join('data','*.png'))
    data = sorted(glob(os.path.join('data', 'data-img_44', 'img*.png')), key=sort_key_func)[1:]
    #print(data)
    
    # proceso respecto al tiempo
    for t, ruta_imagen in enumerate(data):
        im = io.imread(ruta_imagen)
        # se recorta la imagen
        im = im[135:345, 120:570, :] # imagen recortada     
        
        # estoy en una imagen especifica en un determinado t
        for celda in celdas_datos.keys():
            # obtener los valores de la imagen consultando el circulo
            circulo = celdas_datos[celda][0]
            i, j = celda
            img_celda = obtener_celda(im, i, j, alto_celda, ancho_celda)
            valor = calcular_intensidad_promedio(img_celda, circulo)
            celdas_datos[celda][1].append(valor)

    # ETAPA 3: GRAFICAR CADA CELDA CON FUNCIÓN DEL TIEMPO
    graficar_intensidad_tiempo(celdas_datos)



if __name__ == "__main__":
    celdas_seleccionadas = '' 
    celdas_datos = '' # variable que con la infomración de cada celda # {(i1,j1): [circulo, []], (i2,j2): [], ...]
    data = '' # variable que representa el set de imagenes
    main()
    
# TODO: garantizar una sola detección en get_circle
# TODO: intensidad en solo canal verde?

# TODO: tomar solo intensidades mayores
# TODO: calcular y graficar threshold (pedir un porcentaje al usuario)
# TODO: graficar controlPos y controlNeg
# TODO: reducir ruido
# TODO: requirements.txt
# TODO: interfaz sea user-friendly