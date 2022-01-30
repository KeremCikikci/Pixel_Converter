from __future__ import print_function
import cv2
import numpy as np
import binascii
import struct
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import time
from colorama import *
import os

init(convert=True)

def split():
    print(Fore.YELLOW + 'The image is split into parts...')
    croppedPieces = []
    for yPiece in range(yPieces):
        for xPiece in range(xPieces):           
            croppedPieces.append(img[heightOfPieces * yPiece: heightOfPieces * (yPiece + 1), widthOfPieces * xPiece: widthOfPieces * (xPiece + 1)])
    return croppedPieces

def findDominantColor():

    totalTime = 0

    underscoreCount = 0

    for image in range(len(croppedPieces)):
        
        time1 = time.time()
        
        ar = np.asarray(croppedPieces[image])
        shape = ar.shape
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = np.histogram(vecs, len(codes))    # count occurrences

        index_max = np.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        dominantColors.append(colour)

        time2 = time.time()

        totalTime += time2 - time1
        
        gaugeLength = 50

        underscoreCount = int(gaugeLength - gaugeLength * image / len(croppedPieces))

        print(Fore.CYAN + str(len(croppedPieces)) + ' Pieces ' + Fore.LIGHTYELLOW_EX + '|' + Fore.GREEN + '█' * (gaugeLength - underscoreCount) + Fore.LIGHTYELLOW_EX + '_' * underscoreCount + Fore.LIGHTYELLOW_EX + '| %' + str(round(100 * image / len(croppedPieces), 2)) + ' --->' + Fore.CYAN + ' time: '+ str(round(totalTime, 2)) + 's', end="\r")
    
    print(Fore.CYAN + str(len(croppedPieces)) + ' Pieces ' + Fore.LIGHTYELLOW_EX + '|' + Fore.GREEN + '█' * gaugeLength + Fore.LIGHTYELLOW_EX + '| %100' + Fore.CYAN + ' time: '+ str(round(totalTime, 2)) + 's                                            ')
    

def drawRectangle():
    for i in range(len(dominantColors)):
        h = str(dominantColors[i])
        
        image_rectangle = cv2.rectangle(img, (i % xPieces * widthOfPieces, int(i / xPieces) * heightOfPieces), (widthOfPieces * (i + 1), heightOfPieces * int(i / xPieces + 1)), tuple(int(h[i:i+2], 16) for i in (0, 2, 4)), -1)

    return image_rectangle


print(Fore.GREEN + '')
imageName = input("Enter the name of the image (it should be in the same directory with the executable program): ")

img = cv2.imread('./' + imageName)

widhtOfImage = img.shape[1]
heightOfImage = img.shape[0]

print(Fore.YELLOW + 'Image size is ' + str(widhtOfImage) + 'x' + str(heightOfImage))
xPieces, yPieces = int(input("number of pieces divided horizontally: ")), int(input("number of pieces divided vertically: "))
if ((xPieces > widhtOfImage) or (yPieces > heightOfImage)):
    print(Fore.RED + 'You must select the number of parts less than or equal to the resolution of the image!')
    sys.exit("")

print('\n')

widthOfPieces, heightOfPieces = int(widhtOfImage / xPieces), int(heightOfImage / yPieces)

print(Fore.GREEN + 'Image is being read...')

croppedPieces = split()

dominantColors = []

NUM_CLUSTERS = 1

findDominantColor()
image_rectganle = drawRectangle()

print(Fore.GREEN + '')

pixelatedImage = input('Enter your pixelated Image name: ')

if ((pixelatedImage.find('.png') == False) and (pixelatedImage.find('.jpeg') == False) (pixelatedImage.find('.jpg') == False)): 
    cv2.imwrite(pixelatedImage, image_rectganle) 
else:
    cv2.imwrite(pixelatedImage + '.png', image_rectganle) 


print('New image saved successfully!')
