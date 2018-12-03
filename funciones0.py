import cv2
import numpy as np
from matplotlib import pyplot as plt
def estanteria(img1,ubicacion):# Encuentra las esquinas del estante. Ubicacion = True, si está en el proceso de busqueda. Ubicacion = False, si está en el clasificacdor
    Lower = 15
    Upper = 64
    total = len(img1)
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv1 = hsv[:,:,0]
    if ubicacion:
        kernel = np.ones((3,3),np.uint8())
        th = cv2.inRange(hsv1, Lower, Upper)
        th = cv2.erode(th,kernel,iterations=4)
        th = cv2.dilate(th,kernel,iterations=5)
    else:
        kernel = np.ones((3,3),np.uint8())
        th = cv2.inRange(hsv1, Lower, Upper)
        th = cv2.dilate(th,kernel,iterations=8)
        kernel = np.ones((5,5),np.uint8())
        th = cv2.erode(th,kernel,iterations=3)
    cnt = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1]
    comparador = 0
    a = len(cnt)
    i = 0
    while i < a:
        if comparador < len(cnt[i]):
            comparador = len(cnt[i])
            mayor = i
        i = i+1
    contornoFullNoFake = cnt[mayor]
    epsilon = 0.01*cv2.arcLength(contornoFullNoFake,True)
    approx = cv2.approxPolyDP(contornoFullNoFake,epsilon,True)
    numeroPuntos = len(approx)
    i = 0
    min1 = 10000
    max1 = 0
    min2 = 1000
    max2 = 0
    while i < numeroPuntos:
        if (approx[i][0][0]+approx[i][0][1] < min1):
            min1 = approx[i][0][0]+approx[i][0][1]
            esquina1 = approx[i]
        if (max1 < approx[i][0][0]+approx[i][0][1]):
            max1 = approx[i][0][0]+approx[i][0][1]
            esquina4 = approx[i]
        if (abs(approx[i][0][1]-total)+approx[i][0][0] < min2):
            min2 = approx[i][0][0]+abs(approx[i][0][1]-total)
            esquina3 = approx[i]
        if (max2 < abs(approx[i][0][1]-total)+approx[i][0][0]):
            max2 = approx[i][0][0]+abs(approx[i][0][1]-total)
            esquina2 = approx[i]
        i = i+1
    esquinas = [esquina1,esquina2,esquina3,esquina4]
    return esquinas
def estantes(esquinas): #Hace la separacion para tener las esquinas de los estantes
    i = 0
    puntos = []
    while i < 2:
        j = 0
        espacio1 =  abs(esquinas[i][0][0]-esquinas[i+2][0][0])/6.4
        espacio2 =  abs(esquinas[i][0][1]-esquinas[i+2][0][1])/6.4
        while j < 7:
            punto = esquinas[i].copy()
            if min(esquinas[i][0][0],esquinas[i+2][0][0]) == esquinas[i][0][0]:
                punto[0][0] = esquinas[i][0][0]+(j*espacio1)
            else:
                punto[0][0] = esquinas[i][0][0]-(j*espacio1)
            if min(esquinas[i][0][1],esquinas[i+2][0][1]) == esquinas[i][0][1]:
                punto[0][1] = esquinas[i][0][1]+(j*espacio2)
            else:
                punto[0][1] = esquinas[i][0][1]-(j*espacio2)
            puntos.append(punto)
            j = j + 2
        i = i + 1
    columna1 = [puntos[0],puntos[1],puntos[2],puntos[3]]
    columna2 = []
    columna3 = []
    columna4 = [puntos[4],puntos[5],puntos[6],puntos[7]]
    i=0
    while i < 4:
        j = 1
        espacio1 =  abs(columna1[i][0][0]-columna4[i][0][0])/3
        espacio2 =  abs(columna1[i][0][1]-columna4[i][0][1])/3
        while j < 3:
            punto = esquinas[i].copy()
            if min(columna1[i][0][0],columna4[i][0][0]) == columna1[i][0][0]:
                punto[0][0] = columna1[i][0][0]+(j*espacio1)
            else:
                punto[0][0] = columna1[i][0][0]-(j*espacio1)
            if min(columna1[i][0][1],columna4[i][0][1]) == columna1[i][0][1]:
                punto[0][1] = columna1[i][0][1]+(j*espacio2)
            else:
                punto[0][1] = columna1[i][0][1]-(j*espacio2)
            if j == 1:
                columna2.append(punto)
            else:
                columna3.append(punto)
            j = j + 1
        i=i+1
    puntos = [columna1,columna2,columna3,columna4]
    return puntos
def recortes(img,puntos): #Saca los recortes de todos los objetos
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    min_imagen=10
    kernel1 = np.ones((3,3),np.uint8())
    kernel2 = np.ones((5,5),np.uint8())
    Lower = (0, 0, 0)
    Upper = (255, 80, 180)
    estante = []
    centro = []
    objetos = []
    posicion = []
    recortar = []
    i = 0
    while i < 3:
        j = 0
        while j < 3:
            img1 = hsv[puntos[i][j][0][1]:puntos[i+1][j+1][0][1],puntos[i][j+1][0][0]:puntos[i+1][j+1][0][0]]
            mask = cv2.inRange(img1, Lower, Upper)
            mask = cv2.bilateralFilter(mask,9,75,75)
            #mask = cv2.erode(mask, kernel1, iterations=3)
            #mask = cv2.dilate(mask, kernel1, iterations=5)
            imagen = np.transpose(mask)
            #cv2.imshow('mask', mask)
            #cv2.waitKey(0)
            banderaObjeto1 = 0
            banderaObjeto2 = 0
            pixelesY = len(imagen)
            pixelesX = len(imagen[0])
            pixelesRecorrer = int(5*pixelesX/6)
            valorReferencia = pixelesRecorrer*255
            inicio = int(pixelesX/12)
            final = inicio+pixelesRecorrer
            numeroObjetos = 0
            punto = []
            k = 0
            puntoInicial = 0
            while k < pixelesY:
                suma = 0
                l = inicio
                while l < final:
                    suma = suma + imagen[k][l]
                    l=l+1
                if ((valorReferencia-(15*255)) < suma):
                    if banderaObjeto2 == 1:
                        puntoFinal = k
                        punto.append([puntoInicial, puntoFinal])
                        numeroObjetos = numeroObjetos + 1
                        banderaObjeto1 = 0
                        banderaObjeto2 = 0
                    elif banderaObjeto1 == 1:
                        banderaObjeto2 = 1
                else:
                    if k == (pixelesY-1):
                        punto.append([puntoInicial, k])
                    if banderaObjeto1 == 0:
                        puntoInicial = k
                    banderaObjeto1 = 1
                k=k+1
            if numeroObjetos != 0:
                max = len(punto)
                h = 0
                cosas = []
                centrosCosa = []
                while h < max:
                    if min_imagen<(punto[h][1]-punto[h][0]):
                        cosas.append(img1[0:len(imagen[0]),punto[h][0]:punto[h][1]])
                        centrosCosa.append((punto[h][0]+punto[h][1])/2)
                        #cv2.imshow('imagen2', img1[0:len(imagen[0]),punto[h][0]:punto[h][1]])
                        #cv2.waitKey(0)
                        #cv2.destroyWindow('imagen2')
                    h = h+1
                centro.append(centrosCosa)
                estante.append(cosas)
                posicion.append((3*i)+j)
            j = j + 1
            #cv2.destroyWindow('mask')
        i = i+1
    return estante, posicion,centro
def clasificador(img,img_referencia): #Parte de histogramas del clasificador
    RGB = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    espacio = [RGB, cv2.cvtColor(RGB, cv2.COLOR_RGB2GRAY)]
    espacio_referencia = [img_referencia, cv2.cvtColor(img_referencia, cv2.COLOR_RGB2GRAY)]
    a = len(espacio)
    comparacion = 0
    maximo = 0
    i = 0
    while i < a:
        j = 0
        if i == 1:
            hist1 = cv2.calcHist([espacio_referencia[i]],[0],None,[256],[0,256])
            hist2 = cv2.calcHist([espacio[i]],[0],None,[256],[0,256])
            comparacion = comparacion + cv2.compareHist(hist1, hist2, 2)
        else:
            b = len(espacio[i][0][0])
            while j < b:
                hist1 = cv2.calcHist([espacio_referencia[i][:,:,j]],[0],None,[256],[0,256])
                hist2 = cv2.calcHist([espacio[i][:,:,j]],[0],None,[256],[0,256])
                comparacion = comparacion + cv2.compareHist(hist1, hist2, 2)
                j=j+1
        i=i+1
    return comparacion
def clasificador2(estantes, referencia,puntos,puntos_referencia,obj): #Parte de anchos del clasificador
    if obj == 'smirnoff':
        minima_diferencia = 0.5
    elif obj == 'citrus':
        minima_diferencia = 1.5
    else:
        minima_diferencia = 1.12
    relacion = relacionPixelDistancia(puntos,'X')
    relacion_referencia = relacionPixelDistancia(puntos_referencia,'X')
    cm_referencia = len(referencia[0])*relacion_referencia
    valores = []
    for estante in estantes:
        for objeto in estante:
            cm = len(objeto[0])*relacion
            if abs(cm-cm_referencia)<minima_diferencia:
                valores.append(1)
            else:
                valores.append(0)
    return valores
def referencia(condicional): #Dependiendo de la entrada saca una imagen de referencia del objeto
    if condicional == 'BBQ':
        referencia = './objetos/bbq_recorte.jpg'
    elif condicional == 'BEpower':
        referencia = './objetos/BEpower_recorte.jpg'
    elif condicional == 'casquitos':
        referencia = './objetos/casquitos_recorte.jpg'
    elif condicional == 'chocoramo':
        referencia = './objetos/chocoramo_recorte.jpg'
    elif condicional == 'citrus':
        referencia = './objetos/citrus_recorte.jpg'
    elif condicional == 'coca-cola':
        referencia = './objetos/coca-cola_recorte.jpg'
    elif condicional == 'mix':
        referencia = './objetos/mix_recorte.jpg'
    elif condicional == 'natural':
        referencia = './objetos/natural_recorte.jpg'
    elif condicional == 'pringles':
        referencia = './objetos/pringles_recorte.jpg'
    elif condicional == 'quatro':
        referencia = './objetos/quatro_recorte.jpg'
    elif condicional == 'manzana roja':
        referencia = './objetos/roja_recorte.jpg'
    elif condicional == 'rojos':
        referencia = './objetos/rojos_recorte.jpg'
    elif condicional == 'smirnoff':
        referencia = './objetos/smirnoff_recorte.jpg'
    elif condicional == 'splash':
        referencia = './objetos/splash_recorte.jpg'
    elif condicional == 'tomate':
        referencia = './objetos/tomate_recorte.jpg'
    elif condicional == 'manzana verde':
        referencia = './objetos/verde_recorte.jpg'
    RGB_referencia = cv2.imread(referencia)
    #cv2.imshow('imagen1', RGB_referencia)
    return RGB_referencia
def invertir(img): # Invierte los valores de un threshold
    Y = len(img)
    X = len(img[0])
    i = 0
    while i < Y:
        j = 0
        while j < X:
            if img[i][j] == 0:
                img[i][j] = 255
            else:
                img[i][j] = 0
            j = j+1
        i = i+1
    return img
def relacionPixelDistancia(puntos,eje): #Encuentra una relacion de cm/pixeles
    if eje == 'Y':
        pixeles = abs(puntos[0][3][0][1]-puntos[0][0][0][1])
        cm = 15 + 30 + 30 + 30
    if eje == 'X':
        pixeles = abs(puntos[0][0][0][0]-puntos[3][0][0][0])
        cm = 30 + 30 + 30
    relacion = cm/pixeles
    return relacion
def comparacion(estantes,referencia,puntos,puntos_referencia, obj): #Realiza el proceso de clasificacion
    i = 0
    maximo = 0
    imax = 0
    valores = []
    parecido = clasificador2(estantes, referencia,puntos,puntos_referencia,obj)
    for imagenes in estantes:
        for imagen in imagenes:
            if parecido[i] == 0:
                valores.append(0)
            else:
                if obj == 'manzana roja':
                    valor = clasificador(imagen,referencia)
                    if 6000 < valor:
                        hist = cv2.calcHist([imagen],[0],None,[256],[0,256])
                        maximoHist = max(hist)
                        if maximo < maximoHist:
                            maximo = maximoHist
                            imax = i
                        valores.append(valor)
                    else:
                        valores.append(0)
                else:
                    valores.append(clasificador(imagen,referencia))
            i = i+1
    if obj == 'manzana roja':
        valores[imax] = valores[imax]*2
    valorMaximo = noHayObjeto(obj,max(valores))
    if valorMaximo == 0:
        masParecido = -1
    else:
        masParecido = valores.index(valorMaximo)
    return masParecido, valores
def encontrarUbicacion(numero,estantes,posicion): #Encuentra la ubicacion del objeto con respecto a las estantes y los objetos en dicho estante
    i = 0
    k = 0
    a = len(estantes)
    while i < a:
        j = 0
        b = len(estantes[i])
        while j < b:
            if k == numero:
                coeficientes = [i,j]
                i = 1000
                j = 1000
            k = k+1
            j = j+1
        i = i+1
    numeroEstante = posicion[coeficientes[0]]
    numeroObjeto = coeficientes[1]
    return numeroEstante, numeroObjeto
def posicionEspacial(ubicacion,centros,puntos,posicion): #Da la posicion espacion en cm
    Y = 5
    relacion = relacionPixelDistancia(puntos,'X')
    estanteY = 2-(ubicacion[0]%3)
    estanteX = ubicacion[0]//3
    Y_cm = 15+(estanteY*30)+Y
    X_cm_esquina = (estanteX*30) + (centros[posicion.index(ubicacion[0])][ubicacion[1]]*relacion)
    X_cm_centro_esquina = abs(puntos[0][3][0][0]-639)*relacion
    X_cm = X_cm_esquina-X_cm_centro_esquina
    return X_cm,Y_cm
def correcciones(esquinas,img): #Determina si la estanteria esta bie posicionada
    errorGiro = 20
    atras = False
    izquierda = False
    derecha = False
    giroContraManecillas = False
    giroManecillas = False
    if esquinas[0][0][1] == 0 or esquinas[1][0][1] == 0 or (esquinas[2][0][1] == len(img)-1) or (esquinas[3][0][1] == len(img)-1) :
        atras = True
    if esquinas[0][0][0] == 0 or esquinas[2][0][0] == 0:
        izquierda = True
    if (esquinas[1][0][0] == len(img[0])-1) or (esquinas[3][0][0] == len(img[0])-1):
        derecha = True
    if abs(esquinas[2][0][1]-esquinas[3][0][1])>errorGiro:
        if esquinas[2][0][1]-esquinas[3][0][1]>0:
            giroContraManecillas = True
        else:
            giroManecillas = True
    return atras, izquierda, derecha, giroContraManecillas, giroManecillas
def ubicacionInicial(img): #Determina si la posicion inicial esta mal o bien (da un mensaje que determina que accion se deberia hacer)
    buscando = True
    mensaje = ''
    esquinas = estanteria(img, buscando)
    correccion = correcciones(esquinas,img)
    if correccion[0] == False and correccion[1] == False and correccion[2] == False and correccion[3] == False and correccion[4] == False:
        mensaje = 'Continuar'
        buscando = False
    else:
        mensaje = 'Mala posición'
        if correccion[0] == True:
            mensaje = mensaje + ', Atras'
        if correccion[1] == True:
            mensaje = mensaje + ', Izquierda'
        if correccion[2] == True:
            mensaje = mensaje +  ', Derrecha'
        if correccion[3] == True:
            mensaje = mensaje + ', Giro contra las manecillas del reloj'
        if correccion[4] == True:
            mensaje = mensaje + ', Giro con las manecillas del reloj'
    return mensaje, buscando
def noHayObjeto(obj,valor):
    if obj == 'BBQ':
        if valor < 27900:
            valor = 0
    elif obj == 'BEpower':
        if valor < 7400:
            valor = 0
    elif obj == 'casquitos':
        if valor < 18000:
            valor = 0
    elif obj == 'chocoramo':
        if valor < 15000:
            valor = 0
    elif obj == 'citrus':
        if valor < 8500:
            valor = 0
    elif obj == 'coca-cola':
        if valor < 11000:
            valor = 0
    elif obj == 'mix':
        if valor < 10300:
            valor = 0
    elif obj == 'natural':
        if valor < 20000:
            valor = 0
    elif obj == 'pringles':
        if valor < 10500:
            valor = 0
    elif obj == 'quatro':
        if valor < 13000:
            valor = 0
    elif obj == 'manzana roja':
        if valor < 10000:
            valor = 0
    elif obj == 'rojos':
        if valor < 9000:
            valor = 0
    elif obj == 'smirnoff':
        if valor < 4500:
            valor = 0
    elif obj == 'splash':
        if valor < 19000:
            valor = 0
    elif obj == 'tomate':
        if valor < 25000:
            valor = 0
    elif obj == 'manzana verde':
        if valor < 9000:
            valor = 0
    return valor
