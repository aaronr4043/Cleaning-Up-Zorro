#################################################
#
# (C) Aaron Renaghan
#
# Student Number: Aaron Renaghan
# Course: DT228
# Competion Date: 10/11/2017
#
# Title: Cleaning Up Zorro
#
# Introduction: This program is improve the picture quality from old movies 
#
# Description:
# The algorithm works by going through the following steps.
# 1. Importing Libraries that maybe be required
# 2. Set control variables for desired output (entire output takes too long)
# 3. Read in our video and create the video outwriter object
# 4. Perform Thresholding and Masking for watermark removal
# 5. Then go frame by frame through the the next steps
# 6. Remove the Watermark.
# 7. Sharpen the image to enhance edges so they are not completely lost with blurring
# 8. Blur the image blurring to reduce the graininess of the image
# 9. Denoise the image tackle some of the static in the image
# 10. Write out the frame to file
#
# My Experimentation: Read about my experimentation and my reflection on results
# on my blog here : https://228aaron.blogspot.com/2017/11/image-processing-assignment-2.html
#
# I have also uploaded videos of my output from differant stages and the final
# version as proessing takes quite a long time on the entire file, these can be found in the blog.

# Importing the Libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image

# Change These To print out frames of your chosing  and set mode True = Full Video mode 
# False works between startFrame and endFrame and write results also as images it current directory
fullVideo = False
startFrame = 130
endFrame = 140

# Change to your zorro file location
video = cv2.VideoCapture("Zorro.mp4")

# Video Capture:
grabbed = True

# Object for writing out the video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
writeout = cv2.VideoWriter('Zorro.wmv',fourcc, 24.0, (854,480))

# Setting video to frame 1 to thresholding on this to find watermark
video.set(1,1)
(grabbed, I) = video.read()	
G = cv2.cvtColor(I,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(G, 0, 255, type = cv2.THRESH_BINARY_INV)
# Getting the reverse mask since we masked out the black in the image not the watermark
watermark_masked = cv2.bitwise_not(mask)

# For use printing progress
frame = 1

if fullVideo == False:
	video.set(1,startFrame)
	frame = startFrame
	
while (video.isOpened()):

	(grabbed, I) = video.read()
	
	# Checks if there are no more frames to process
	if grabbed == False:
		print 'End Of File'
		break

	if grabbed == True:	
		# Printing Progress to the console
		print "Frame", frame, "processing" 
		frame = frame + 1
	
		G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
		
		# Removing The Watermark from the image using mask created earlier 
		G = cv2.inpaint(G,watermark_masked,1,cv2.INPAINT_TELEA)		
		
		# Sharpening the Image
		kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
		G = cv2.filter2D(G, -1, kernel)
		
		# Preforming a erosion to try reduce the noise
		eroded = cv2.erode(G, kernel, iterations=1) 

		# Removes small details but makes the image alot smoother, when played back to back looks significantly better 
		gausblur = cv2.GaussianBlur(eroded,(3,3),0)
		bilatblur = cv2.bilateralFilter(gausblur, 3, 3, 3)
	
		# Denoise
		denoised = cv2.fastNlMeansDenoising(bilatblur,10,10,7,21)
		
		# Writing to my output
		output = cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)
		writeout.write(output)
		key = cv2.waitKey(1)
		
		# Controls for whole video vs certain frames
		if fullVideo == False:
			startFrame = startFrame + 1
			cv2.imwrite('Frame' + str(frame) + '.jpg', output)
			print 'Frame' + str(frame -1) + '.jpg written to file'
		
			if endFrame == startFrame:
				print 'End of subsection'
				break
	
	# if the 'q' key is pressed, quit:
	if key == ord("0"):
		break
		
video.release()
writeout.release()
