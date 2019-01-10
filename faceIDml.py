"""
ADAPTED FROM CS121 HOMEWORK @ HARVEY MUDD 
Original files info/credit below
Author      : Yi-Chieh Wu, Devon Frost, Amy Sorto, Shannon Steele
Class       : HMC CS 121
Date        : 2018 Sep 04
Description : Homework 1
"""

import os
import numpy as np
import cv2 as cv
import csv
import random

INF = float("inf")
#hardcoding in the proportions for the slices based on og images done by hand
TopSlice = 0.25
MidSlice = 0.09
BotSlice = 0.48
# variables from surveryed users
usernum = 0
iden = [0, 0, 0, 0, 0, 0, 0]
border = 500
batchNum = "f0"


def make_userfolders(username):
    # Make folder in faces directory for current user if it doesnt already exist
    pathname = "data/faces/" + username
    if not os.path.exists(pathname):
        os.mkdir(pathname)
        print("Directory " , pathname ,  " Created ")
        return pathname
        print("Please go populate folder with images.")
        #insert break command
    else:    
        print("Directory " , pathname ,  " already exists")
        return pathname

# Get files from given path
def get_files(path):
    fns = []
    for fn in os.listdir(path):
        full_fn = os.path.join(path, fn)
        if os.path.isdir(full_fn):
            continue
        fns.append(full_fn)
    print(len(fns))
    return fns   

# BATCH: reads data for each line in the CSV file in batch runs
# then checks user folder exists and calls slicing function
def readBatchData():
    global iden
    global usernum

    with open('MGTPP.csv') as csv_file:
        print('reading data')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                usernum = line_count
                name = readName() #gets users name
                SingleUserRun(name) 
            line_count+=1

# BATCH: gets user full name 
def readName():
    global iden
    global usernum

    with open('MGTPP.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        col_count = 0
        first = ""
        last = ""
        for row in csv_reader:
            if line_count == int(usernum):
                for col in row:
                    if col_count == 2: 
                        first = col
                    if col_count == 3:
                        last = col
                    col_count += 1
            line_count += 1
        name = first + last
        print(name)
        return name

# BOTH: completes data collection process and passes into slicing for single user
def SingleUserRun(name):
    path = make_userfolders(name)
    readNumData()
    slicing(path, name)

# BOTH: reads out each line of numeric data for given user and stores numeric values in an array
def readNumData():
    global iden
    global usernum

    with open('MGTPP.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        col_count = 0
        for row in csv_reader:
            if line_count != 0:
                if line_count == int(usernum):
                    for col in row:
                        if col_count == 4:
                            iden[0] = col
                        if col_count == 5:
                            iden[1] = col
                        if col_count == 6:
                            iden[2] = col
                        if col_count == 7:
                            iden[3] = col
                        if col_count == 8:
                            iden[4] = col
                        if col_count == 9:
                            iden[5] = col
                        if col_count == 11:
                            iden[6] = col
                        col_count += 1   
            line_count += 1
        print(iden[0], iden[1], iden[2])

# BOTH: runs images compilation process
def slicing(path, name):
    global batchNum

    imgs = gray(path, name)
    img_height, img_width = imgs[0].shape[:2]
    crops = crop(imgs)
    print(img_height)
    completeImg = ImgComb(crops, img_height, True, True)

    # save final image to appropriate location
    if (batchNum == "f0"):
        cv.imwrite(os.path.join("data/finals/"+name+".jpg"), completeImg)
    else:
        cv.imwrite(os.path.join("data/batchtests/"+batchNum+name+".jpg"), completeImg)

# BOTH: converts imgs to grayscale
def gray(path, name):
    imgs = [] # array for gray scale images
    #converts to grayscale
    for fn in sorted(get_files(path)):
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
        print(portion)
    return imgs

# BOTH: combines slices into a single image
def ImgComb (imgs, imgHeight, horz, vert):
    global iden
    global border

	# create new image of double the width of the original
    height, width = imgs[0].shape[:2]
    comboImg = np.full((imgHeight+border*2+35, (width+border*2)), 255) # 35 in H accounts for gaps
    print(comboImg.shape[:2])
    # print(height)
    # print(width)
	# assign original images pixels to the new image
    totalHeights = border #accounts for varied hieghts of slices
    print(totalHeights)
    for i, img in enumerate(imgs):
        height, width = img.shape[:2]
        print(height)
        gap = 7 # at least 7 pixels gap between each
        #middle slices get skewed
        if(i == 1 or i == 2 or i == 3):
            print("skewing")
            z = random.randint(0, 6) # skew id
            a = random.randint(0, 6) # gap id
            skewBy = int(iden[z])*(30) # set skew
            right  = random.choice([True, False])
            if(int(iden[a]) != 0):
                print("set gap")
                gap = int(iden[a])*(7) # set gap
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
        print(totalHeights)
    if (vert == True):
        comboImg = vertGlitch(comboImg)
    if (horz == True):
        comboImg = horzGlitch(comboImg)
    return comboImg

# OUT OF USE: combos images without gaps
def ImgCombNoGap (imgs, imgHeight):
    global iden

	# create new image of double the width of the original
    height, width = imgs[0].shape[:2]
    comboImg = np.full((imgHeight+border*2, (width+border*2)), 255) # 35 in H accounts for gaps

	#assign original images pixels to the new image
    totalHeights = border #accounts for varied hieghts of slices
    for i, img in enumerate(imgs):
        height, width = img.shape[:2]
        if(i == 1 or i == 2 or i == 3):
            print("skewing")
            z = random.randint(0, 6)() # skew id
            skewBy = int(iden[z])*(30) # set skew
            right  = random.choice([True, False])
            for y in range(height):
                for x in range(width):
                        if(x < width and y < height): #check bounds of image
                            if (right == True): #skews slice right
                                comboImg[y+(totalHeights)-1, x+skewBy+border] = img[y, x] 
                            else: #skews slice left
                                comboImg[y+(totalHeights)-1, x+border-skewBy] = img[y, x]
        else:
            print("not skewing")
            for y in range(height):
                for x in range(width):
                    if(y < height):
                        comboImg[y+(totalHeights)-1, x+border]= img[y, x]
        totalHeights += height
    comboImg = vertGlitch(comboImg)
    return comboImg

# BOTH: glitch horizontally
def horzGlitch(comboImg):
    global iden, border  
    for identity in iden:
        identity = int(identity)
        for i in range(identity):
            height, width = comboImg.shape[:2]
            loc = random.randint(0 + border*2, height - border*2)
            sliceWidth = random.randint(10*identity, 20*identity)
            skew = random.randint(15, 70)
            for y in range(loc, sliceWidth+loc):
                for x in range(width-skew):
                    if (x+skew < width and y < height):
                        comboImg[y, x]= comboImg[y, x+skew]
    return comboImg

# BOTH: glitch vertically
def vertGlitch(comboImg):
    global iden, border

    for identity in iden:
        identity = int(identity)
        for i in range(int(identity)):
            height, width = comboImg.shape[:2]
            loc = random.randint(0 + border*3, width - border*3)
            sliceWidth = random.randint(10*identity, 20*identity)
            skew = random.randint(15, 70)
            for x in range(loc, sliceWidth+loc):
                for y in range(height-skew):
                    comboImg[y, x]= comboImg[y+skew, x]
    return comboImg

def main():
    global usernum
    global batchNum
    # File Set Up
    # if the faces directory doesn't exist, create it
    faces_dir = os.path.join("data/faces")
    if not os.path.exists(faces_dir):
        os.mkdir(faces_dir)
    # if the finals directory doesn't exist, create it
    finals_dir = os.path.join("data/finals")
    if not os.path.exists(finals_dir):
        os.mkdir(finals_dir)

    if (input("Would you like to read in individual csv data? yes/no ") == "yes"):
        first = input("What is your first name? ")
        last = input("What is your last name? ")
        name  = first + last
        usernum = input("What user are you? ")
        # make folder for current user
        SingleUserRun(name)
    elif (input("Would you like to run a batch? yes/no ") == "yes"):
        batchNum = input("What batch folder do you want to save to? ")
        batch_dir = os.path.join("data/batchtests/"+batchNum)
        if not os.path.exists(batch_dir):
            os.mkdir(batch_dir)
        readBatchData()

if __name__ == "__main__":
    main()
