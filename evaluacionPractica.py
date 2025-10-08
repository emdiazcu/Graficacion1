import cv2 as cv 

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(1)
radio_pupila = 1
direccion_pupila = 1  
velocidad_pupila = 0.5

#lengua:
radio_lengua = 20
direccion_lengua = 1
velocidad_lengua = 1
desplazamiento_lengua = 0
direccion_desplazamiento = 1




while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    for(x,y,w,h) in rostros:
        radio_lengua = h*0.6
        radio_pupila += velocidad_pupila * direccion_pupila
        
        
        radio_max_pupila = int((w + h) / 70)  
        if radio_max_pupila < 5: radio_max_pupila = 5 
        
        if radio_pupila >= radio_max_pupila:
            direccion_pupila = -1
        elif radio_pupila <= 1:
            direccion_pupila = 1

        radio_lengua += velocidad_lengua * direccion_lengua
        if radio_lengua >= 40 or radio_lengua <= 15:
            direccion_lengua *= -1
    
        desplazamiento_lengua += velocidad_lengua * direccion_desplazamiento
        if desplazamiento_lengua >= 10 or desplazamiento_lengua <= -10:
            direccion_desplazamiento *= -1 


           
        res = int((w+h)/8)
        img = cv.rectangle(img, (x,y), (x+w, y+h), (234, 23,23), 5)
        img = cv.rectangle(img, (x,int(y+h/2)), (x+w, y+h), (0,255,0),5 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 21, (0, 0, 0), 2 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 21, (0, 0, 0), 2 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 20, (255, 255, 255), -1 )
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , int(radio_pupila), (0, 0, 255), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , int(radio_pupila), (0, 0, 255), -1 )
        img = cv.circle(img, (x + int(w*0.5), y + int(h*0.6)) , 20, (0, 0, 255), -1 )
        #lengua
        img = cv.ellipse(
            img,
            (x + int(w*0.5), y + int(h*0.8) + int(desplazamiento_lengua)),  # traslación vertical
            (int(radio_lengua), 5),                                         # escalado eje horizontal
            0, 0, 360,                                                       # startAngle, endAngle
            (0, 0, 200),                                                     # color
            -1
        )
   



    cv.imshow('img', img)
    if cv.waitKey(1)== ord('q'):
        break
    
cap.release
cv.destroyAllWindows()