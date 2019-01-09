"""
ADAPTED FROM CS121 @ HARVEY MUDD HOMEWORK
Original files info/credit below
Author      : Yi-Chieh Wu, Devon Frost, Amy Sorto, Shannon Steele
Class       : HMC CS 121
Date        : 2018 Sep 04
Description : Homework 1
"""


import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import csv
import random
import time

INF = float("inf")
#hardcoding in the proportions for the slices
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
        #print(usernum)
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            #print(row)
            if line_count != 0:
                usernum = line_count
                #print(usernum)
                name = readName() #gets users name
                readNumData() #gets users data
                path = make_userfolders(name) #checks path to users image folder existsx
                slicing(path, name) #completes users slicing
            line_count+=1

# BATCH: gets user full name 
def readName():
    # global gender, pronouns, race, sexuality, college, disability, other
    global iden
    global usernum

    with open('MGTPP.csv') as csv_file:
        #print('reading data')
        #print(usernum)
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        col_count = 0
        first = ""
        last = ""
        for row in csv_reader:
            #print(row)
            if line_count == int(usernum):
                #print(True)
                for col in row:
                    if col_count == 2: 
                        first = col
                        #(first)
                    if col_count == 3:
                        last = col
                    col_count += 1
            line_count += 1
        name = first + last
        print(name)
        return name

# BOTH: reads out each line of numeric data for given user and stores numeric values in an array
def readNumData():
    # global gender, pronouns, race, sexuality, college, disability, other
    global iden
    global usernum

    with open('MGTPP.csv') as csv_file:
        #print('reading data')
        #print(usernum)
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        col_count = 0
        for row in csv_reader:
            if line_count != 0:
                #print("not zero")
                #print(line_count)
                if line_count == int(usernum):
                    #print("user row")
                    #print(line_count)
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

# BOTH: does initial image slicing on the total number of images (set up to be 5 rn)
def slicing(path, name):
    global batchNum
    # get all images (5) from user's file
    imgs = [] # array for images once gray
    #i=0 # 
    #print(path)
    #converts to grayscale
    for fn in sorted(get_files(path)):
        if (os.stat(fn).st_size != 0):
            #print(i)
            #print(fn)
            img = cv.imread(fn)
            #gray = cv.imread(img, cv.IMREAD_GRAYSCALE)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #convert to gray scale
            imgs.append(gray)
            #i+=1
        print(img[0, 0])
            
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
    completeImg = ImgComb(imgs, img_height)
    if (batchNum == "f0"):
        cv.imwrite(os.path.join("data/finals/"+name+".jpg"), completeImg)
    else:
        cv.imwrite(os.path.join("data/batchtests/"+batchNum+name+".jpg"), completeImg)


# BOTH: combines slices into a single image
def ImgComb (imgs, imgHeight):
    # global usernum, gender, pronouns, race, sexuality, college, disability, other, border
    global iden

	# create new image of double the width of the original
    height, width = imgs[0].shape[:2]
    comboImg = np.full((imgHeight+border*2+35, (width+border*2)), 255) # 35 in H accounts for gaps

	# assign original images pixels to the new image
    totalHeights = border #accounts for varied hieghts of slices
    for i, img in enumerate(imgs):
        height, width = img.shape[:2]
        gap = 7 # at least 7 pixels gap between each
        #print(height)
        #middle slices get skewed
        if(i == 1 or i == 2 or i == 3):
            print("skewing")
            z = random.randint(0, 6) # skew id
            a = random.randint(0, 6) # gap id
            skewBy = int(iden[z])*(30) # set skew
            right  = random.choice([True, False])
            print(right)
            #print(gap)
            if(int(iden[a]) != 0):
                print("set gap")
                gap = int(iden[a])*(7) # set gap
            for y in range(height):
                for x in range(width):
                        if(x < width and y < height - gap): #check bounds of image
                            if (right == True): #skews slice right
                                #print("right")
                                comboImg[y+gap+(totalHeights)-1, x+skewBy+border] = img[y, x] 
                            else: #skews slice left
                                comboImg[y+gap+(totalHeights)-1, x+border-skewBy] = img[y, x]
        else:
            print("not skewing")
            for y in range(height):
                for x in range(width):
                    if(y < height - gap):
                        #print(y)
                        #print(x)
                        #print(img[y, x])
                        comboImg[y+gap+(totalHeights)-1, x+border] = img[y, x]
                        #comboImg[y, x] = img[y, x]
        totalHeights += height
        #print(totalHeights)
    comboImg = vertGlitch(comboImg)
    comboImg = horzGlitch(comboImg)
    return comboImg

# OUT OF USE: combos images without gaps
def ImgCombNoGap (imgs, imgHeight):
    # global usernum, gender, pronouns, race, sexuality, college, disability, other, border
    global iden

	# create new image of double the width of the original
    height, width = imgs[0].shape[:2]
    comboImg = np.full((imgHeight+border*2, (width+border*2)), 255) # 35 in H accounts for gaps

	#assign original images pixels to the new image
    totalHeights = border #accounts for varied hieghts of slices
    for i, img in enumerate(imgs):
        height, width = img.shape[:2]
        #gap = 7 # at least 7 pixels gap between each
        #print(height)
        #middle slices get skewed
        if(i == 1 or i == 2 or i == 3):
            print("skewing")
            z = random.randint(0, 6)() # skew id
            #a = random.randint(0, 6) # gap id
            skewBy = int(iden[z])*(30) # set skew
            right  = random.choice([True, False])
            print(right)
            #print(gap)
            # if(int(iden[a]) != 0):
            #     print("set gap")
            #     gap = int(iden[a])*(7) # set gap
            for y in range(height):
                for x in range(width):
                        if(x < width and y < height): #check bounds of image
                            if (right == True): #skews slice right
                                #print("right")
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
        #print(totalHeights)
    comboImg = vertGlitch(comboImg)
    #comboImg = horzGlitch(comboImg)
    return comboImg

# BOTH: glitch horizontally
def horzGlitch(comboImg):
    global iden, border 
    #print("horz")  
    for identity in iden:
        identity = int(identity)
        for i in range(identity):
            height, width = comboImg.shape[:2]
            loc = random.randint(0 + border*2, height - border*2)
            sliceWidth = random.randint(10*identity, 20*identity)
            #print(loc)
            #print(sliceWidth)
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
            #print(loc)
            sliceWidth = random.randint(10*identity, 20*identity)
            #print(sliceWidth)
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
        path = make_userfolders(name)
        readNumData()
        slicing(path, name) 
    elif (input("Would you like to run a batch? yes/no ") == "yes"):
            batchNum = input("What batch folder do you want to save to? ")
            batch_dir = os.path.join("data/batchtests/"+batchNum)
            if not os.path.exists(batch_dir):
                os.mkdir(batch_dir)
            readBatchData()
    

# def crop_images(imgs, resize=False):
#     """Crop images.

#     Parameters
#     --------------------
#         imgs   -- list of images, each of type np.ndarray
#         resize -- flag to resize images, bool
#     """

#     # resize images
#     if resize:
#         ### ========== TODO : START ========== ###
#         # problem a
#         # determine average image size
#         avgHeight, avgWidth = 0, 0 
#         length = len(imgs)
#         for img in imgs: 
#             heightOut, widthOut = img.shape[:2]
#             avgHeight += heightOut
#             avgWidth += widthOut
#         avgHeight = avgHeight / length #calc avg heigh
#         avgWidth = avgWidth / length #calc avg width


#         # resize to average width while maintaining aspect ratio
#         for i, img in enumerate(imgs):
#             heightOut, widthOut = img.shape[:2]
#             dim = (int(avgWidth), int(heightOut*(avgWidth/widthOut))) #calc new dimensions of image
#             res = cv.resize (img, dim, interpolation = cv.INTER_CUBIC) #resize img
#             imgs[i] = res


#         ### ========== TODO : END ========== ###

#     # get minimum image size
#     height, width = INF, INF
#     for img in imgs:
#         img_height, img_width = img.shape[:2]
#         if img_height < height:
#             height = img_height
#         if img_width < width:
#             width = img_width

#     # crop
#     for i, img in enumerate(imgs):
#         img_height, img_width = img.shape[:2]
#         x = img_width//2 - width//2
#         y = img_height//2 - height//2
#         roi = img[y:y+height, x:x+width, :]
#         imgs[i] = roi


# def average_image(path, resize=False):
#     """Compute average of several images.

#     Parameters
#     --------------------
#         path -- directory path, str
#     """

#     # read images
#     imgs = []
#     for fn in get_files(path):
#         img = cv.imread(fn)
#         imgs.append(img)

#     # crop images
#     crop_images(imgs, resize=resize)

#     # average
#     height, width = imgs[0].shape[:2]
#     avg_img = np.zeros((height,width,3), np.float32())
#     for img in imgs:
#         avg_img += img 
#     avg_img = avg_img / len(imgs)
#     avg_img = np.rint(avg_img).astype(np.uint8)  # convert to uint8

#     return avg_img
    


# def findeyes():
#     """Crop faces using face detection.

#     Parameters
#     --------------------
#         path  -- directory path of input faces, str
#         path2 -- directory path of output faces, str
#     """

#     ### ========== TODO : START ========== ###
#     # problem b
#     # https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html
#     # http://gregblogs.com/computer-vision-cropping-faces-from-images-using-opencv2/
#     # make directory
#     cropped = os.path.join(path2)
#     if not os.path.exists(cropped):
#         os.mkdir(cropped)

#     #process images
#     face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

#     for fn in get_files(path):
#         img = cv.imread(fn)  #define array imgs for sake of ease
#         gray = cv.imread("yjw.png", cv.IMREAD_GRAYSCALE) 
#         gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #convert to gray scale
#         plt.imshow(gray, cmap="gray", vmin=0, vmax = 255)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#         baseName = os.path.basename(path+ '/' + fn) 
#         for (x,y,w,h) in faces:     #recognizing the boundries created by OpenCV
#             cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) 
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = img[y:y+h, x:x+w]
#         minisize = (img.shape[1],img.shape[0])
#         for f in faces:
#             x, y, w, h = [ v for v in f ]
#             cv.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
#             sub_face = img[y:y+h, x:x+w]
#         cv.imwrite(os.path.join("data/faces/cropped", baseName), sub_face) #take indivudual baseName rather than a static name
#     ### ========== TODO : END ========== ###

#def findEyes():
    # face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    # #eye_cascade = cv.CascadeClassifier('frontalEyes.xml') 

    # img = cv.imread('sachin.jpg')
    # #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # for (x,y,w,h) in faces:
    #     cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    #     roi_gray = gray[y:y+h, x:x+w]
    #     roi_color = img[y:y+h, x:x+w]
    #     # eyes = eye_cascade.detectMultiScale(roi_gray)
    #     # for (ex,ey,ew,eh) in eyes:
    #     #     cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    ### ========== TODO : END ========== ###

if __name__ == "__main__":
    main()
