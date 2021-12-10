#Jacob He
#301391374
#CMPT365 2021 July 10th

#For image loading
import tkinter      #for UI interface, buttons, etc
from tkinter import Tk
from tkinter.constants import SEPARATOR #for top layer of widget 
from tkinter.filedialog import askopenfilename #for opening file name
from PIL import Image, ImageTk # For opening images & for opening them in Tk window
import matplotlib.pyplot as plt #for plotting the histogram
import matplotlib.image as mpimg #for loading images aswell 

#For audio files
import scipy.io.wavfile
#import numpy as np
#we already have matplotlib

window = Tk()
window.geometry("1960x800")
window.title("CMPT365 Image Processing")

def greyscale():
    Tk().withdraw() #remove root window
    filename = askopenfilename() #open dialog box
    im = Image.open(filename)
    pixels = im.load()
    imformat = im.format
    width, height = im.size
    im_greyscale = Image.new('L', [width, height], 0)
    grey_pixels = im_greyscale.load()
  
    for x in range(width):
        for y in range(height):
            luma = 0.299*pixels[x,y][0] + 0.587*pixels[x,y][1] + 0.114*pixels[x,y][1]
            grey_pixels[x,y]=int(luma)
            
   
    timage = ImageTk.PhotoImage(im)
    label1 = tkinter.Label(image = timage)
    label1.image = timage
    label1.place(x=0, y=100)

    timage2 = ImageTk.PhotoImage(im_greyscale)
    label2 = tkinter.Label(image = timage2)
    label2.image = timage2
    label2.place(x=800, y=100)
    im_greyscale.save(filename+'_grayscale.'+imformat)

    
def dither():
    Tk().withdraw() #remove root window
    filename = askopenfilename() #open dialog box
    im = Image.open(filename)
    pixels = im.load()
    imformat = im.format
    width, height = im.size
    im_dither = Image.new('L', [width, height], 0)
    dither_pixels = im_dither.load()

    dmatrixsize = 2
    accuracy = 16
    dmatrix4x4 = [[0, 8, 2 ,10], [12, 4 ,14 ,6], [3, 11 ,1 ,9], [15,7,13,5]]
    highdmatrix2x2 = [[12, 9], [8 ,10]]
    lowdmatrix2x2 = [[2, 6], [2 ,1]]
    balanceddmatrix2x2 = [[13, 4], [2 ,7]]
    identicaldmatrix2x2= [[7, 7], [7 ,7]]
    dmatrix8x8 = [[0, 8, 2 ,10, 3 , 12, 7 , 9], [12, 4 ,4 ,6, 15, 5 ,9, 1], [3, 11 ,1 ,9, 5 ,2 ,13 ,3],
     [5,7,13,5,8, 5 ,2, 10], [5,7,3,5,8, 5 ,2, 10], [3, 11 ,1 ,9, 5 ,12 ,3 ,3],  [12, 4 ,14 ,6, 15, 5 ,9, 1],
     [0, 8, 2 ,10, 3 , 2, 7 , 9]]
    
    for x in range(width):
        for y in range(height):
            xval = x%dmatrixsize
            yval = y%dmatrixsize
            luma = 0.299*pixels[x,y][0] + 0.587*pixels[x,y][1] + 0.114*pixels[x,y][1]
            brightval = luma/accuracy
            #print('luma = '+ str(luma) + ' dmaxtrix val = '+ str(dmatrix[xval][yval])) #for debugging
            if brightval>balanceddmatrix2x2 [xval][yval]:
                 dither_pixels[x, y]= 255
            else :
                dither_pixels[x, y] = 0

    timage = ImageTk.PhotoImage(im)
    label1 = tkinter.Label(image = timage)
    label1.image = timage
    label1.place(x=0, y=100)

    timage2 = ImageTk.PhotoImage(im_dither)
    label2 = tkinter.Label(image = timage2)
    label2.image = timage2
    label2.place(x=800, y=100)
    im_dither.save(filename+'_dither.'+imformat)


def autolevel():
    Tk().withdraw() #remove root window
    filename = askopenfilename() #open dialog box
    im = Image.open(filename)
    pixels = im.load()
    imformat = im.format
    width, height = im.size
    im_autolevel = Image.new('RGB', [width, height], 0)
    autolevel_pixels = im_autolevel.load()

    averageVal = 0
    totalRGB = 0
    totalpixelnum = width*height

    #for RED
    for x in range(width):
        for y in range(height):
            totalRGB=totalRGB+pixels[x,y][0]

    averageVal = totalRGB/totalpixelnum
    multiplier = 128/averageVal
    for x in range(width):
        for y in range(height):
            temp = pixels[x,y][0] * (multiplier+((pixels[x,y][0]-averageVal)/128))
            if temp>255:
                temp=245
            if temp<0:
                temp=10
            autolevel_pixels[x,y]= (int(temp), autolevel_pixels[x,y][1],autolevel_pixels[x,y][2] )


    #for GREEN
    totalRGB = 0
    for x in range(width):
        for y in range(height):
            totalRGB=totalRGB+pixels[x,y][1]

    averageVal = totalRGB/totalpixelnum
    multiplier = 128/averageVal
    for x in range(width):
        for y in range(height):
          
            temp = pixels[x,y][1] * (multiplier+((pixels[x,y][1]-averageVal)/128))
            if temp>255:
                temp=245
            if temp<0:
                temp=10
            autolevel_pixels[x,y]= (autolevel_pixels[x,y][0], int(temp), autolevel_pixels[x,y][2] )

    #for BLUE
    totalRGB = 0
    for x in range(width):
        for y in range(height):
            totalRGB=totalRGB+pixels[x,y][2]

    averageVal = totalRGB/totalpixelnum
    multiplier = 128/averageVal
    for x in range(width):
        for y in range(height):
            temp = pixels[x,y][2] * (multiplier+((pixels[x,y][2]-averageVal)/128))
            if temp>255:
                temp=245
            if temp<0:
                temp=10
            autolevel_pixels[x,y]= (autolevel_pixels[x,y][0], autolevel_pixels[x,y][1],int(temp) )
    

    timage = ImageTk.PhotoImage(im)
    label1 = tkinter.Label(image = timage)
    label1.image = timage
    label1.place(x=0, y=100)

    timage2 = ImageTk.PhotoImage(im_autolevel)
    label2 = tkinter.Label(image = timage2)
    label2.image = timage2
    label2.place(x=800, y=100)

    im_autolevel.save(filename+'_autolevel.'+imformat)



def histogram(num ):
    Tk().withdraw() #remove root window
    filename = askopenfilename() #open dialog box
    im = Image.open(filename)
    pixels = im.load()
    width, height = im.size

    img=mpimg.imread(filename)

    colarr=[]
    for x in range(width):
        for y in range(height):
            colarr.append(pixels[x,y][num])


    if num==0:
        plt.title("Red Histogram")
    elif num==1:
        plt.title("Green Histogram")
    elif num==2:
        plt.title("Blue Histogram")
    plt.xlabel("Value (Intensity) ")
    plt.ylabel("Pixels Frequency")
    plt.hist(colarr)
    plt.show()
    plt.clf()

def waveplot():
    Tk().withdraw() #remove root window
    filename = askopenfilename() #open dialog box

    srate, raw = scipy.io.wavfile.read(filename)

    
    plt.title("Waveform Plot - Sample Rate: " + str(srate))
    #plt.title("Waveform Plot - Total Samples: " + str(sframes) + " Sample Rate: " + str(srate))
    plt.plot( raw, color="red")
    
    plt.ylabel("Amplitude (Voltage)")
    plt.xlabel("Samples")
    plt.show()

def fadeinfadeout():
    Tk().withdraw() #remove root window
    filename = askopenfilename() #open dialog box
    srate, raw = scipy.io.wavfile.read(filename)
    


    #Fade In
    for x in range(srate):
        samplesize = len(raw)-1
        pre_Y = -20 + 20*(x/srate)
        final_Y = pre_Y/20
        multiplier_X = pow(10,final_Y)
        raw[samplesize-x]=multiplier_X*raw[samplesize-x]
        raw[x]=multiplier_X*raw[x]
        
    scipy.io.wavfile.write(filename+"_FadeInFadeOut.wav", srate, raw)


bfadeinfadeout = tkinter.Button(window, text = "Fade in fade out", command = fadeinfadeout, height=5, width=12)
bfadeinfadeout.place(x=300, y = 0)

bwaveplot = tkinter.Button(window, text = "Wave Plot", command = waveplot, height=5, width=12)
bwaveplot.place(x=400, y = 0)

bhistr = tkinter.Button(window, text = "Red Histogram", command=lambda: histogram(0), height=2, width=12)
bhistr.place(x=500, y = 0)

bhistg = tkinter.Button(window, text = "Green Histogram", command = lambda:histogram(1), height=2, width=12)
bhistg.place(x=500, y = 30)

bhistb = tkinter.Button(window, text = "Blue Histogram", command = lambda:histogram(2), height=2, width=12)
bhistb.place(x=500, y = 60)

bgrey = tkinter.Button(window, text = "Greyscale", command = greyscale, height=5, width=12)
bgrey.place(x=600, y = 0)

bdither = tkinter.Button(window, text = "Dither", command = dither, height=5, width=12)
bdither.place(x=700, y = 0)

bautolevel = tkinter.Button(window, text = "Autolevel", command = autolevel, height=5, width=12)
bautolevel.place(x=800, y = 0)



window.mainloop()
