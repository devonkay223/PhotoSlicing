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

INF = float("inf")
User = False
#hardcoding in the proportions for the slices
TopSlice = 0.25
MidSlice = 0.09
BotSlice = 0.48
# variables from users
usernum = 0
gender = 0
pronouns = 0 
race = 0
sexuality = 0
college = 0
disability = 0
other = 0


######################################################################
# functions
######################################################################
def make_userfolders(username):
    """ Make folder in faces directory for current user if it doesnt already exist

    Parameters
    --------------------
        first   -- user first name, str
        last    -- user last name, str

    Return
    --------------------
        pathname    -- path anme for current user's files, str
    """
    pathname = "data/faces/" + username
    if not os.path.exists(pathname):
        os.mkdir(pathname)
        print("Directory " , pathname ,  " Created ")
        return pathname
    else:    
        print("Directory " , pathname ,  " already exists")
        return pathname



def get_files(path):
    """Get full pathname of all files in path directory.

    Parameters
    --------------------
        path   -- directory path, str

    Return
    --------------------
        fns    -- list of filenames, each of type str
    """

    fns = []
    for fn in os.listdir(path):
        full_fn = os.path.join(path, fn)
        if os.path.isdir(full_fn):
            continue
        fns.append(full_fn)
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
    global usernum
    global gender
    global pronouns
    global race
    global sexuality
    global college
    global disability
    global other

    with open('MGTPP.csv') as csv_file:
        print('reading data')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        col_count = 0
        for row in csv_reader:
            if line_count != 0:
                if line_count == usernum:
                    for col in row:
                        if col_count == 4:
                            gender = col
                        if col_count == 5:
                            pronouns = col
                        if col_count == 6:
                            race = col
                        if col_count == 7:
                            sexuality = col
                        if col_count == 8:
                            college = col
                        if col_count == 9:
                            disability = col
                        if col_count == 10:
                            other = col
                        col_count += 1   
            line_count += 1
        #print(gender, pronouns, race)

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
    cv.imwrite(os.path.join("data/finals",name+str(4)+".jpg"), completeImg)


def ImgComb (imgs, imgHeight):
	# create new image of double the width of the original
    height, width = imgs[0].shape
    comboImg = np.zeros((imgHeight, (width)), np.uint8)

	#assign original images pixels to the new image
    totalHeights = 0 #accounts for varied hieghts of slices
    for i, img in enumerate(imgs):
        height, width = imgs[i].shape
        for y in range(height):
            for x in range(width):
                comboImg[y+(totalHeights)-1, x] = img[y, x]
        totalHeights += height
    return comboImg

# def skew(): 
#     #code
#     # vars: extremity, slice? 

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
        usernum = input("What user are you?")
        # make folder for current user
        path = make_userfolders(name)
        #Devon REWORD THIS -- figure out what this portrays actually though 
        #gender = input("How much do you feel like you dont fit into tech because of your gender, on a scale of 1-5? ")
    else: 
        #change this to read from csv file
        first = "Huiruo"
        last = "Zhang"
        name = first + last
        global usernum
        usernum = 2
        # make folder for current user
        path = make_userfolders(name)
        #gender = 5

    readData()
    #slicing(path, name)


    

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
