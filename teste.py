import numpy as np
import cv2
import argparse


def tratamento_img(imagem):
    img_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    mascara = mog.apply(img_cinza)
    _,img_binarizada = cv2.threshold(mascara,127,255,cv2.THRESH_BINARY)
    erosao = cv2.erode(img_binarizada,kernel,iterations = 1)
    dilatacao = cv2.dilate(erosao,kernel_1,iterations = 1)
    mp_abre = cv2.morphologyEx(dilatacao, cv2.MORPH_OPEN, kernel)
    mp_fecha = cv2.morphologyEx(mp_abre, cv2.MORPH_CLOSE,kernel_2)
    dilatacao = cv2.dilate(mp_fecha,(21,21),iterations = 1)
    return dilatacao

def desenha_retangulos(imagem,imagem_tratada):
    contornos,_ = cv2.findContours(imagem_tratada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key = cv2.contourArea, reverse = True)
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area > 7000:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
parser = argparse.ArgumentParser(description='Teste feito pela olho do dono ')
parser.add_argument('-v','--video', type=str,
                    help='Caminho para o video')


args = vars(parser.parse_args())
cap = cv2.VideoCapture(str(args['video']))
mog = cv2.createBackgroundSubtractorMOG2()
kernel = np.ones((3,3),np.uint8)
kernel_1 = np.ones((12,12),np.uint8)
kernel_2 = np.ones((21,21),np.uint8)

while True:
    ret, imagem = cap.read()
    
    if not ret:
        break
    
    imagem_tratada = tratamento_img(imagem)
    desenha_retangulos(imagem,imagem_tratada)
    cv2.imshow('frame',imagem)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
