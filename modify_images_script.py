#!/usr/bin/env python
"""
a Python Script to :
    1) convert all images to JGP with 3 channels i.e. no transperancy
    2) unify all images size to 256x256 while keeping ratio
    3) remove black background resulting from converting the PNG to JPG
"""
from PIL import Image
import os, sys


def clear_black_background(im):
    im_pixels = im.getdata()
    new_pixels = []
    for pixel in im_pixels :
        if type(pixel) == tuple and len(pixel)== 4 and pixel[3] ==0 :
            new_pixels.append((255,255,255))
        elif type(pixel) == tuple :
            new_pixels.append((pixel[0],pixel[1],pixel[2]))
        else :
            print "bala7"
    im.putdata(new_pixels)
    return im

def modifyImage(input_dir,infile, output_dir, size=(256,256)):
     outfile = os.path.splitext(infile)[0]
     extension = os.path.splitext(infile)[1]

     if infile != outfile:
        try :
            im = Image.open(input_dir+"/"+infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.convert("RGBA")
            if extension != 'jpg' :
                im = clear_black_background(im)

            base = Image.new("RGB", size, (255,255,255))
            base.paste( im , ( (256 - im.width)/2 ,( 256 -im.height)/2) )
            base.save(output_dir+"/"+outfile+".jpg","JPEG")

        except IOError as e:
            print  e.strerror

# main function
if __name__=="__main__":

    # output directory that will be created
    output_dir = "resized"
    # input directory of the dataset
    input_dir = "data_birds"
    dir = os.getcwd()

    # create output_dir if it is not found
    if not os.path.exists(os.path.join(dir,output_dir)):
        os.mkdir(output_dir)

    # loop over all images of the dataset and modify
    for file in os.listdir(dir+"/"+input_dir):
        modifyImage(input_dir,file,output_dir)
