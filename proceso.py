import cv2
import numpy as np
from funciones0 import*

def busquedaRepisa(img): #Entra con la imagen de baja calidad
    mensaje, buscando = ubicacionInicial(img)
    return mensaje, buscando
def busquedaObjeto(img1,obj):#Entra con la imagen de alta calidad y un string del objeto deseado
    img_referencia = cv2.imread('./objetos/referencia.jpg')
    img1_referencia = cv2.resize(img_referencia, (1280,720), interpolation = cv2.INTER_AREA)
    esquinas = estanteria(img1, False)
    esquinas_referencia = estanteria(img1_referencia, False)
    puntos = estantes(esquinas)
    puntos_referencia = estantes(esquinas_referencia)
    imgEstantes, posicion,centros = recortes(img1,puntos)
    imgReferencia = referencia(obj)
    objeto, valores = comparacion(imgEstantes,imgReferencia,puntos,puntos_referencia, obj)
    if objeto == -1:
        mensaje = 'No está'
    else:
        mensaje=''
        ubicacion = encontrarUbicacion(objeto, imgEstantes, posicion)
        posicion = posicionEspacial(ubicacion,centros,puntos,posicion)
        mensaje = 'Cm en X: '+ str(posicion[0]) + ', Cm en Y: ' + str(posicion[1])
        #mensaje = 'Estante: '+ str(ubicacion[0]) + ', Objeto: ' + str(ubicacion[1])
    return(mensaje)
