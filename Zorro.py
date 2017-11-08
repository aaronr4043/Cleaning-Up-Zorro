#################################################

# (C) Aaron Renaghan
#
# Student Number: Aaron Renaghan
# Course: DT228
# Date: 10/11/2017
#
# Title: Cleaning Up Zorro
#
# Introduction: This program is improve the picture quality from old movies 
#
# To Do: 1) Fix the Contrast
# 2) Stabalise the image
# 3) Remove Noise
# 4) Try Colour?
# 5) Remove the audio from the silent film
#
# Description:
# The algorithm works by going through the following steps.
# 1. Reading in the image and resizing the background to fit the signature image
# 2. Creating a mask by preforming adaptive thresholding to extract the signature
# 3. Eroding and Dilating the mask to smooth out the signature and remove noise
# 4. Creating a reverse mask and then combining masks to create our output images
# 5. Brighten up the extracted signature to try get a more true pen colour
# 6. Showing and saving the output image.
#
# My Experimentation:

#Importing the Libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image

I = cv2.imread('zorro.png')
G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

# Capturing an image from a webcam:
capture = cv2.VideoCapture('zorro.mp4')

# saving the video to a file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Zorro_Out.mp4',fourcc, 20.0, (640,480))


while(capture.isOpened()):
	ret, frame = capture.read()
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	cv2.imshow('frame', gray)
	
	out.write(frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
capture.release()
cv2.destroyAllWindows()







# Values = G.ravel()
# plt.hist(Values,bins=256,range=[0,256]); 
# plt.show()

# H = cv2.equalizeHist(G)
# cv2.imshow("Fella", H)
# cv2.imshow("OG", I)

# Values = H.ravel()
# plt.hist(Values,bins=256,range=[0,256]); 
# plt.show()

# cv2.waitKey(0)












##################################################