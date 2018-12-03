#asi se realiza el proceso
import cv2
from proceso import*
##Proceso de ver si la repisa esta bien posicionada
busqueda = True
while busqueda:
    img = cv2.imread('./imagenes/Picture 1.jpg') #Imagen de baja calidad
    img_busqueda = cv2.resize(img,(320,240), interpolation = cv2.INTER_AREA)
    mensaje, busqueda = busquedaRepisa(img_busqueda)
    print(mensaje)
img = cv2.imread('./imagenes/Picture 1.jpg') #Imagen de baja calidad
img1 = cv2.resize(img, (1280,720), interpolation = cv2.INTER_AREA)
objeto = 'manzana verde' #String del objeto deseado
#----------------------------falta probar tomate y splash-----------------------
#Proceso de buscar el objerp
mensaje = busquedaObjeto(img1, objeto)
print(mensaje)
cv2.imshow('imagen', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
