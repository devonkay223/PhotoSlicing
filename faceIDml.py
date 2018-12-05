"""
ADAPTED FROM CS121 @ HARVEY MUDD HOMEWORK
Origional files info/credit below
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

INF = float("inf")
User = True
#hardcoding in the proportions for the slices
TopSlice = 0.25
MidSlice = 0.09
BotSlice = 0.48
# variables from users
usernum = 0
iden = [0, 0, 0, 0, 0, 0, 0]
# gender = 0
# pronouns = 0 
# race = 0
# sexuality = 0
# college = 0
# disability = 0
# other = 0
border = 120


######################################################################
# functions
######################################################################
def make_userfolders(username):
    #Make folder in faces directory for current user if it doesnt already exist
    pathname = "data/faces/" + username
    if not os.path.exists(pathname):
        os.mkdir(pathname)
        print("Directory " , pathname ,  " Created ")
        return pathname
    else:    
        print("Directory " , pathname ,  " already exists")
        return pathname



def get_files(path):
    #Get full pathname of all files in path directory.
    fns = []
    for fn in os.listdir(path):
        full_fn = os.path.join(path, fn)
        if os.path.isdir(full_fn):
            continue
        fns.append(full_fn)
    print(len(fns))
    return fns


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
    


# def crop_faces(path, path2):
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

def readData():
    # global gender, pronouns, race, sexuality, college, disability, other
    global iden
    global usernum

    with open('MGTPP.csv') as csv_file:
        print('reading data')
        print(usernum)
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        col_count = 0
        for row in csv_reader:
            if line_count != 0:
                print("not zero")
                print(line_count)
                if line_count == int(usernum):
                    print("user row")
                    print(line_count)
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

def slicing(path, name):
    # get all images (5) from user's file
    imgs = []
    for fn in sorted(get_files(path)):
        if (os.stat(fn).st_size != 0):
            img = cv.imread(fn)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #convert to gray scale
            imgs.append(gray)
            
    img_height, img_width= imgs[0].shape

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
    cv.imwrite(os.path.join("data/finals",name+str(6)+".jpg"), completeImg)


def ImgComb (imgs, imgHeight):
    # global usernum, gender, pronouns, race, sexuality, college, disability, other, border
    global iden

	# create new image of double the width of the original
    height, width = imgs[0].shape
    comboImg = np.full((imgHeight+border*2+35, (width+border*2)), 255) # 35 in H accounts for gaps

	#assign original images pixels to the new image
    totalHeights = 0 #accounts for varied hieghts of slices
    for i, img in enumerate(imgs):
        height, width = img.shape
        gap = 7 # at least 7 pixels gap between each
        if(i == 1 or i == 2 or i == 3):
            print("skewing")
            z = identifier() # skew id
            a = identifier() # gap id
            skewBy = int(iden[z])*(30) # set skew
            if(int(iden[a]) != 0):
                gap = int(iden[a])*(7) # set gap
            for y in range(height):
                for x in range(width):
                        if(x+skewBy < width and y < height - gap): 
                            comboImg[border+y+gap+(totalHeights)-1, x+skewBy+border] = img[y, x-skewBy]                        
        else:
            print("not skewing")
            for y in range(height):
                for x in range(width):
                    comboImg[border+y+gap+(totalHeights)-1, x+border]= img[y, x]
        totalHeights += height
    return comboImg


# def skew(comboImg, img, totalHeights): 
#     global iden
    
#     z = identifier()
    
#     print("identifier")
#     print(iden[z])
#     skewBy = int(iden[z])*(30)
#     height, width = img.shape
#     for y in range(height):
#         for x in range(width):
#             if(i == 1 or i == 2 or i == 3):
#                 if(x+skewBy < width):
#                     comboImg[border+y+(totalHeights)-1, x+skewBy+border] = img[y, x-skewBy]
#     return comboImg 

def identifier(): 
    used = []
    z = random.randint(0, 6)
    #TODO fix this so it works correctly 
    for i in used:
        if z == i:
            print('retry')
            identifier()
    print (z)
    used.append(z)
    return z

# def gap(): 
#     #write gap code

# def vertSlice():
#     #write vertical slices code

# def bits(): 
#     #write bits code???

######################################################################
# main
######################################################################

def main():
    global usernum
    # File Set Up
    # if the faces directory doesn't exist, create it
    faces_dir = os.path.join("data/faces")
    if not os.path.exists(faces_dir):
        os.mkdir(faces_dir)
    # if the finals directory doesn't exist, create it
    finals_dir = os.path.join("data/finals")
    if not os.path.exists(finals_dir):
        os.mkdir(finals_dir)

    # User Input
    if (User == True):
        first = input("What is your first name? ")
        last = input("What is your last name? ")
        name  = first + last
        usernum = input("What user are you? ")
        # make folder for current user
        path = make_userfolders(name)      
    else: 
        #change this to read from csv file
        first = "Huiruo"
        last = "Zhang"
        name = first + last
        usernum = 2
        # make folder for current user
        path = make_userfolders(name)

    readData()
    slicing(path, name)


    

    # img = average_image("data/faces/raw")
    # cv.imshow("naive average", img)
    # cv.imwrite(os.path.join(averages_dir, "avg_naive.jpg"), img)
   
    # ### ========== TODO : START ========== ###
    # ### Uncomment these lines after implementing code

    # # problem a

    # img = average_image("data/faces/raw", resize=True)
    # cv.imshow("naive resized average", img)
    # cv.imwrite(os.path.join(averages_dir, "avg_resized.jpg"), img)

    # # problem b

    # crop_faces("data/faces/raw", "data/faces/cropped")
    # img = average_image("data/faces/cropped", resize=True)
    # cv.imshow("face detection average", img)
    # cv.imwrite(os.path.join(averages_dir, "avg_detect.jpg"), img)
 
    # problem c
    """
    Short Description Here
    """
    ### ========== TODO : END ========== ###

if __name__ == "__main__":
    main()
