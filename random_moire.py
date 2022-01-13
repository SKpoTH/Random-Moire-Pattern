# --------------------------> Import Official Libraries <---------------------------
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
# ---------------------------> Import Local Libraries <-----------------------------

# ---------------------------> ______Sub Script______ <-----------------------------
def readGrayImage(input_file):
    '''
        Read image from given file path + name, and Convert to Grayscale Image
    '''
    # -> Read an image
    read_img = cv.imread(input_file)
    # -> Convert image BGR-to-Grayscale
    read_img = cv.cvtColor(read_img, cv.COLOR_BGR2GRAY)

    output_img = read_img

    return output_img

def convertRange(input_img, min_val, max_val):
    '''
        Convert from any range into [min_val, max_val]
    '''
    # -> Convert to [0, 1]
    norm_img = (input_img - input_img.min()) / (input_img.max() - input_img.min())
    # -> Convert to [min_val, max_val]
    output_img = (norm_img * (max_val - min_val)) + min_val

    return output_img

def moirePattern2D(size, A, rad_x, rad_y):
    '''
        Generate Moire Pattern by sin wave (2-axis)
    '''
    IMG_HEIGHT, IMG_WIDTH = size

    # -> Create Function Input
    y = np.arange(IMG_HEIGHT)
    x = np.arange(IMG_WIDTH)
    xv, yv = np.meshgrid(x, y)

    # -> Apply Sin-based noise
    moire_noise = A * np.sin(xv*rad_x + yv*rad_y)

    return moire_noise

def addMoireNoise(input_img):
    '''
        Add Moire Pattern with Random...
    '''
    output_img = input_img.copy()

    ### -> Random Parameter
    # - Settting / Number of Pattern Random
    parameter_set = []
    A_base = min([input_img.shape[0], input_img.shape[1]])
    num_set = np.random.randint(2, 4)
    # - Parameter Random
    for i in range(num_set):
        A = np.random.randint(int(A_base*0.05), int(A_base*0.15))
        rad_x = np.pi * (0.05 * np.random.randint(-10, 10))
        rad_y = np.pi * (0.05 * np.random.randint(-10, 10))
        parameter_set.append((A, rad_x, rad_y))

    ### -> Add Moire Pattern following the setting one
    for parameter in parameter_set:
        moire_noise = moirePattern2D(input_img.shape, parameter[0], parameter[1], parameter[2])
        output_img = output_img + moire_noise

    return output_img

# ---------------------------> _____Main Script_____  <-----------------------------
INPUT_PATH = "images/input/"
OUTPUT_PATH = "images/output/"

if __name__ == "__main__":
    # -> Get All Image Files
    files = glob(INPUT_PATH + '*')

    for i in range(len(files)):
        ### => Read "input_img"
        input_file = files[i]
        input_img = readGrayImage(input_file)

        ### => Add Moire Noise (Random)
        output_img = addMoireNoise(input_img)

        ### => Save Add Moire Noise
        # -> Convert Range
        output_img = convertRange(output_img, 0, 255)
        output_img = output_img.astype(np.uint8)
        # -> Save Image
        filename = os.path.basename(input_file)
        output_file = filename.split('.')[0] + "_moire" + "." + filename.split('.')[1]
        cv.imwrite(OUTPUT_PATH + output_file, output_img)

# ----------------------------> _____End Script_____ <-----------------------------