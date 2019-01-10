import os
import numpy as np
import cv2 as cv
import random
import time

INF = float("inf")
#hardcoding in the proportions for the slices
TopSlice = 0.25
MidSlice = 0.09
BotSlice = 0.48
# variables from surveryed users
border = 0
photos = 5
distortion = 0
path  = "data/faces/Photobooth/"
name = ""
values = [0, 0, 0, 0, 0, 0]

def photobooth():
    print("You will take 5 photos.")
    photoCap()
    fns = getFiles()
    numPop()
    slicing()

def countdown():
    for i in range(5):
        print (i)

def photoCap():
    for i in range(5): 
        print (i)
        camera_port = 0
        camera = cv.VideoCapture(camera_port)
        time.sleep(0.5)  # If you don't wait, the image will be dark
        return_value, image = camera.read()
        cv.imwrite(os.path.join("data/faces/Photobooth/"+str(i)+".jpg"), image)
        del(camera)

def numPop(): 
    upper  = distortion
    if (distortion - 5 < 0): 
        lower = 1
    else: 
        lower = distortion - 5
    for i in range(len(values)):
        values[i] = random.randint(lower, upper)

def getFiles():
    global path
    #Get full pathname of all files in path directory.
    fns = []
    for fn in os.listdir(path):
        full_fn = os.path.join(path, fn)
        if os.path.isdir(full_fn):
            continue
        fns.append(full_fn)
    return fns   

def slicing():
    global batchNum, path, name

    imgs = gray()
    img_height, img_width = imgs[0].shape[:2]
    crops = crop(imgs)
    completeImg = ImgComb(crops, img_height, True, True)

    # save final image to appropriate location
    cv.imwrite(os.path.join("data/finals/Photobooth/"+name+".jpg"), completeImg)

# converts imgs to grayscale
def gray():
    imgs = [] # array for gray scale images
    #converts to grayscale
    for fn in sorted(getFiles()):
        if (os.stat(fn).st_size != 0):
            img = cv.imread(fn)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #convert to gray scale
            imgs.append(gray)
    return imgs  

# BOTH: does initial image slicing on the total number of images 
def crop(imgs):
    img_height, img_width = imgs[0].shape[:2]

    #crop each image for its respective height
    y = 0 # variable for where the crop should start in the vertical axis
    for i, img in enumerate(imgs):
        if (i==0): 
            portion = int(img_height*(TopSlice))
        if (i==1 or i==2 or i==3):
            portion = int(img_height*(MidSlice))
        if (i==4):
            portion = int(img_height*(BotSlice))
        upper = y + portion
        cropped = img[y:upper]
        imgs[i] = cropped
        y += portion
    return imgs

# BOTH: combines slices into a single image
def ImgComb (imgs, imgHeight, horz, vert):
    global values, border

	# create new image of double the width of the original
    height, width = imgs[0].shape[:2]
    print (height)
    print (width)
    border  = int(imgHeight/3)
    print(border)
    comboImg = np.full((imgHeight+border*2+35, (width+border*2)), 255) # 35 in H accounts for gaps
	# assign original images pixels to the new image
    totalHeights = border #accounts for varied hieghts of slices
    for i, img in enumerate(imgs):
        height, width = img.shape[:2]
        gap = 7 # at least 7 pixels gap between each
        #middle slices get skewed
        if(i == 1 or i == 2 or i == 3):
            print("skewing")
            z = random.randint(0, 5) # skew id
            a = random.randint(0, 5) # gap id
            skewBy = int(values[z])*(30) # set skew
            print(skewBy)
            right  = random.choice([True, False])
            print(right)
            if(values[a] != 0):
                print("set gap")
                gap = int(values[a])*(7) # set gap
            for y in range(height):
                for x in range(width):
                        if(x < width and y < height - gap): #check bounds of image
                            if (right == True): #skews slice right
                                comboImg[y+gap+(totalHeights)-1, x+border+skewBy] = img[y, x] 
                            else: #skews slice left
                                comboImg[y+gap+(totalHeights)-1, x+border-skewBy] = img[y, x]
        else:
            print("not skewing")
            for y in range(height):
                for x in range(width):
                    if(y < height - gap):
                        comboImg[y+gap+(totalHeights)-1, x+border] = img[y, x]
        totalHeights += height
    if (vert == True):
        comboImg = vertGlitch(comboImg)
    if (horz == True):
        comboImg = horzGlitch(comboImg)
    return comboImg

# glitch horizontally
def horzGlitch(comboImg):
    global values, border 
    print ("horz") 
    for num in values:
        for i in range(num):
            height, width = comboImg.shape[:2]
            loc = random.randint(0 + border*2, height - border*2)
            sliceWidth = random.randint(num, num*4)
            skew = random.randint(5, 30)
            for y in range(loc, sliceWidth+loc):
                for x in range(width-skew):
                    if (x+skew < width and y < height):
                        comboImg[y, x]= comboImg[y, x+skew]
    return comboImg

# glitch vertically
def vertGlitch(comboImg):
    global values, border
    print("vert")
    for num in values:
        for i in range(num):
            height, width = comboImg.shape[:2]
            loc = random.randint(0 + border*3, width - border*3)
            sliceWidth = random.randint(num, num*4)
            skew = random.randint(10, 50)
            for x in range(loc, sliceWidth+loc):
                for y in range(height-skew):
                    if (y + skew < height and y > 0):
                        comboImg[y, x]= comboImg[y+skew, x]
    return comboImg

def main():
    global usernum, batchNum, distortion, name
    # File Set Up
    # if the faces directory doesn't exist, create it
    faces_dir = os.path.join("data/faces/Photobooth")
    if not os.path.exists(faces_dir):
        os.mkdir(faces_dir)
    # if the finals directory doesn't exist, create it
    finals_dir = os.path.join("data/finals/Photobooth")
    if not os.path.exists(finals_dir):
        os.mkdir(finals_dir)

    if (input("Would you like to use photobooth mode? (yes/no) ") == "yes"): 
        name = input("What is your name? ")
        distortion = int(input("On a scale of 1-15 choose a level of distortion: "))
        while (distortion > 16 or distortion <= 0):
            distortion = int(input("Please input a number on a scale of 1-15 to choose a level of distortion: "))
        photobooth()
        # TODO add auto upload tp drive or auto share (email or insta?) of final image? 

if __name__ == "__main__":
    main()
