import cv2
from proceso import*
i = 1
resultados = []
etiquetas = ['BBQ', 'BEpower', 'casquitos', 'chocoramo', 'citrus', 'coca-cola', 'mix', 'natural', 'pringles', 'quatro', 'manzana roja', 'rojos', 'smirnoff', 'splash', 'tomate', 'manzana verde']
while i < 21:
    img = cv2.imread('./imagenes/Banco_Pruebas/'+str(i)+'.jpg')#Imagen de alta calidad
    img1 = cv2.resize(img, (1280,720), interpolation = cv2.INTER_AREA)
    resultado = 'Imagen '+ str(i) + ', '
    #for obj in etiquetas:
    #    resultado = resultado + obj + ', '
    resultados.append(resultado)
    for obj in etiquetas:
        resultados.append(obj+ ', ' + busquedaObjeto(img1, obj))
    print(i)
    i=i+1
with open('resultados.txt', 'w+') as f:
    for a in resultados:
        f.write("%s\n" % a)
