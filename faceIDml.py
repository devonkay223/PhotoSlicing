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

INF = float("inf")



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

def slicing(gender, path, name):
    # get all images (5) from user's file
    imgs = []
    for fn in get_files(path):
        if (os.stat(fn).st_size != 0):
            img = cv.imread(fn)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #convert to gray scale
            imgs.append(gray)
            #print(fn)
            #name = str(i) + ".jpg"
            #cv.imwrite(os.path.join("data/finals", name), img)
    #print(len(imgs))    
    
    #imgs = from imgs in get_files(path) orderby file descending select file;

    #var biggest = files.First();
 
    img_height, img_width= imgs[0].shape
    divHeight = img_height//gender # height of horizontal slices
    #crop each image for its respective height
    y = 0 # variable for where the crop should start in the vertical axis
    for i, img in enumerate(imgs):
        upper = y + divHeight
        cropped = img[y:upper]
        imgs[i] = cropped
        #cv.imshow("cropped", cropped)
        y += divHeight
        #cv.imwrite(os.path.join("data/finals", "file.jpg"), cropped)
    completeImg = ImgComb(imgs, divHeight, gender)
    cv.imwrite(os.path.join("data/finals",name+str(gender)+".jpg"), completeImg)

def ImgComb (imgs, divHeight, gender):
	# create new image of double the width of the original
    height, width = imgs[0].shape
    #print(height)
    comboImg = np.zeros((divHeight*gender, (width)), np.uint8)

	#print (ogimg[0, 0])
	#print(ogimg[0, 0, 0])

	#assign original images pixels to the new image
    for i, img in enumerate(imgs):
        for y in range(height):
            for x in range(width):
                comboImg[y+(height*i)-1, x] = img[y, x]
    return comboImg



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
    first = "Devon"#input("What is your first name? ")
    last = "Frost"#input("What is your last name? ")
    name  = first + last
    # make folder for current user
    path = make_userfolders(name)
    #print(path)
    #Devon REWORD THIS -- figure out what this portrays actually though 
    gender = 5 #input("How much do you feel like you dont fit into tech because of your gender, on a scale of 1 -10? ")
    
    slicing(int(gender), path, name)


    

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
