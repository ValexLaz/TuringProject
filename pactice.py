#esto se usa para entrenar el procesamiento de imagen
import cv2
import pickle

#definimos el tamaño de los rectangulos
width, height = 52, 22

#creamos y guardamos los rectangulos en un archivo
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

#creanos una funcion para seleccionar los espacios con el mause
def mouseClick(events, x, y, flags, params):
    
    #aqui hacemos que aparezcan los rectangulos con el click izquierdo 
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    
    #aqui definimos que con click derecho eliminamos cada rectangulo
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1,y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)  

    #finaliza guardando los rectanguos que añadimos y eliminamos en el archivo "CarParkPos"
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

#citamos la imagen para que aparezca en pantalla
while True:

    img = cv2.imread('carpark6.png') #cambiar dependiendo de que imagen se use
    
    #definimos los parametros de cada rectangulo (color,tamaño,borde)
    for pos in posList:
        cv2.rectangle(img,pos,(pos[0] + width,pos[1] + height),(105,200,150),2)
    
    #hacemos que podamos utilizar la funcion del mause en la imagen
    cv2.imshow("image",img)
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)

