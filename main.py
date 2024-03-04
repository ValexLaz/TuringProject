import cv2
import pickle #propietario de python, esto serializa y deserializa objetos 
import cvzone
import numpy as np 

cap = cv2.VideoCapture('carPark.mp4')

#citamos a los espacios guardados en a imagen
with open('CarParkPos', 'rb') as f:
    posList =  pickle.load(f) #esto para que nos muestre los espacios guardados

#definimos el tamaño de los rectangulos 
width,height=106,47

#definimos una funcion para ver el video con los espacios
def checkParkingSpace(imgPro): 
    #definimos nel contador de espacios

    spaceCounter = 0
    for pos in posList:
        x,y =pos

        imgCrop = imgPro[y:y+height, x:x+width]
        #nos muestra el numero de pixeles que hay en cada rectangulo
        count = cv2.countNonZero(imgCrop)
        #aqui definimos el color y el grosor de los rectangulos
        if count <950:
            color = (0,255,0) #verde
            thickness = 5
            spaceCounter +=1
        else: 
            color = (0,0,255) #rojo
            thickness = 2
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color,thickness)
        #aqui hacemos que nos muestre los espacios disponibles
        cvzone.putTextRect(img, str(count),(x,y+height-3), scale = 1, thickness=2, offset=0 , colorR=color)

    cvzone.putTextRect(img, f'Disponibles: {spaceCounter}/{len(posList)}',(100,50), scale = 3, thickness=5, offset=20, colorR=(0,200,0))


while True: #esto nomas para que tenga un bucle el video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)#se convierte a escala de grises, nota: todo eso hasta la linea 50 son filtros para que se vea mejor
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel =np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    #muestra los rectangulos guardados y selecionados
    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    if cv2.waitKey(10) == ord("q"):
        break
