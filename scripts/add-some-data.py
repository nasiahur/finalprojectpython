import numpy as np
import cv2
from PIL import Image
import scipy

def convert_to_RGB(kelas):
    if kelas=='fire': n_image=71
    if kelas=='grass': n_image=102
    if kelas=='water': n_image=138
    for i in range(n_image):
        img = Image.open('dataset/'+kelas+'.'+str(i)+'.png')
        img = img.resize((120,120))
        img.convert("RGB").save('dataset/'+kelas+'.'+str(i)+'.png')
        i+=1
		

def geser_pixel(kelas):
    n= 0
    if kelas=='fire': n_image=71
    if kelas=='grass': n_image=102
    if kelas=='water': n_image=138

    for i in range(n_image):
        file = 'dataset/'+kelas+'.'+str(i)+'.png'
        img = cv2.imread(file)
        img = cv2.resize(img, (90,90))
        for j in range(6):
            x,y=0,0
            if j==0 or j==4:  #geser 15 pixel ke kanan
                x=15
            if j==1 or j==5:  #geser 30 pixel ke kanan
                x=30
            if j==2 or j==4:  #geser 15 pixel kebawah
                y=15
            if j==3 or j==5:  #geser 30 pixel ke bawah
                y=30

            M=np.float32([[1,0,x],[0,1,y]])
            img_new = cv2.warpAffine(img,M,(120,120))
            cv2.imwrite('datasets/'+kelas+'.'+ str(n) + '.png',img_new)
            img_ = cv2.flip(img_new,1)
            cv2.imwrite('datasets/'+kelas+'.'+ str(n+1) + '.png',img_)
            print(i, j)
            j+=1
            n+=2
        i+=1

convert_to_RGB('fire')
geser_pixel('fire')


convert_to_RGB('grass')
geser_pixel('grass')


convert_to_RGB('water')
geser_pixel('water')
