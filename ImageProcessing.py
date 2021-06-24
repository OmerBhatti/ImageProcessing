import cv2 as cv
from enum import Enum
import numpy

class MODE(Enum):
    IMAGE = 0
    VIDEO = 1
    CAPTURE = 2
class COLOR(Enum):
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
class DIR(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

class ImageProcessing:
    def __init__(self,url, MODE = MODE.IMAGE):
        self.url = url
        self.MODE = MODE
        self.source = None
        self.dimension = None
        self.__read()

    def reScaleSource(self,scale = 0.5):
        height = int(self.source.shape[0]*scale)
        width = int(self.source.shape[1]*scale)
        dimension = (width,height)
        self.dimension = dimension
        self.source = cv.resize(self.source, dimension, interpolation=cv.INTER_AREA)

    def getDimension(self,multipliyer = 1):
        height = int(self.source.shape[0]*multipliyer)
        width = int(self.source.shape[1]*multipliyer)        
        return (width,height)
   
    def reSizeSource(self,dimension = (1280,768)):
        self.dimension = dimension
        self.source = cv.resize(self.source, tuple(dimension), interpolation=cv.INTER_AREA)

    def setSource(self,source):
        self.source=source
    
    def __read(self):
        if(self.MODE == MODE.IMAGE):
            self.source = cv.imread(self.url)
            self.dimension = self.getDimension()
         
    def show(self,WindowName = "RESULT",delay=0):
        """Delay = 0 will wait for keypress else it will wait for delay-ms passed in parameter"""
        if(self.MODE == MODE.IMAGE):
            cv.imshow(WindowName,self.source,)
            cv.waitKey(delay)

    def printPixels(self):
        for i in range(0,self.source.shape[0]):
            for j in range(0,self.source.shape[1]):
                print(self.source[i][j],end="")
            print()

    def getPixel(self,x,y):
        if(x<self.dimension[1] and y<self.dimension[1]):
            return self.source[x][y]
        else:
            return "Invlaid Index"
    
    def getAllUniqueColors(self):
        colors = set({})
        for i in range(0,self.source.shape[0]):
            for j in range(0,self.source.shape[1]):
                colors.add((self.source[i][j][0],self.source[i][j][1],self.source[i][j][2]))
        return colors

    def changeSpecificColor(self,beforeColor,afterColor):
        "Color tuple = (BLUE,GREEN,RED)"
        for i in range(0,self.source.shape[0]):
            for j in range(0,self.source.shape[1]):
                if(self.source[i][j][0] == beforeColor[0]
                   and self.source[i][j][1] == beforeColor[1]
                   and self.source[i][j][2] == beforeColor[2]):
                    self.source[i][j] = afterColor

    def BlackAndWhite(self,MODE = COLOR.RED):
        for i in range(0,self.source.shape[0]):
            for j in range(0,self.source.shape[1]):
                newValue=[]
                if(MODE == COLOR.BLUE):
                    newValue = numpy.array([self.source[i][j][0],self.source[i][j][0],self.source[i][j][0]])
                elif(MODE == COLOR.GREEN):
                    newValue = numpy.array([self.source[i][j][1],self.source[i][j][1],self.source[i][j][1]])
                elif(MODE == COLOR.RED):
                    newValue = numpy.array([self.source[i][j][2],self.source[i][j][2],self.source[i][j][2]])
                self.source[i][j] = newValue
    
    def GausianBlur(self,blurAmount=10):
        if(blurAmount%2==0):
            blurAmount+=1
        cv.GaussianBlur(self.source,(blurAmount,blurAmount),0, dst = self.source)
    
    def erodeFilter(self,iterations = 1):
        cv.erode(self.source,numpy.array([[1,1,1],[1,1,1],[1,1,1]]),self.source,(1,1),iterations)
    
    def customFilter(self,kernel):
        cv.filter2D(self.source,None,numpy.array(kernel),self.source)
    
    def sharpen(self,iteration = 1):
        for i in range(iteration):
            self.customFilter(kernel=[
                [0,-.5,0],
                [-.5,3,-.5],
                [0,-.5,0]
            ])
    
    def blur(self,iteration = 1):
        for i in range(iteration):
            self.customFilter(kernel=[
                [1/9,1/9,1/9],
                [1/9,1/9,1/9],
                [1/9,1/9,1/9]
            ])
    
    def outline(self):
        self.customFilter(kernel=[
            [-1,-1,-1],
            [-1,8,-1],
            [-1,-1,-1]
        ])
    
    def emboss(self,iteration=1):
        for i in range(iteration):
            self.customFilter(kernel=[
                [-2,-1,0],
                [-1,1,1],
                [0,1,2]])
    
    def EdgeDetection(self,DIRECTION = DIR.TOP):
        if(DIRECTION == DIR.TOP):
            kernel = [
                [1,2,1],
                [0,0,0],
                [-1,-2,-1]]
            self.customFilter(kernel=kernel)
        elif(DIRECTION == DIR.BOTTOM):
            kernel = [
                [-1,-2,-1],
                [0,0,0],
                [1,2,1]]
            self.customFilter(kernel=kernel)
        elif(DIRECTION == DIR.LEFT):
            kernel = [
                [1,0,-1],
                [2,0,-2],
                [1,0,-1]]
            self.customFilter(kernel=kernel)
        elif(DIRECTION == DIR.RIGHT):
            kernel = [
                [-1,0,1],
                [-2,0,2],
                [-1,0,1]]
            self.customFilter(kernel=kernel)
    
    def Brightness(self,value):
        for i in range(0,self.dimension[1]):
            for j in range(0,self.dimension[0]):
                self.source[i][j] = (self.__tighten(self.source[i][j][0]+value),self.__tighten(self.source[i][j][1]+value),self.__tighten(self.source[i][j][2]+value))
    
    def Contrast(self,value):
        factor = ((259 * (value +255)) / (255*(259-value)))
        for i in range(0,self.dimension[1]):
            for j in range(0,self.dimension[0]):
                self.source[i][j] = (self.__tighten(factor*(self.source[i][j][0]-128) + 128),self.__tighten(factor*(self.source[i][j][1]-128) + 128),self.__tighten(factor*(self.source[i][j][2]-128) + 128))
    
    def pixelette(self,value = 5):
        """Pixelette current image in source"""
        if(value<0):
            self.sharpen(value*-1)
            return
        elif(value==0):
            return
        else:
            self.reScaleSource(1/value)
            self.reScaleSource(value)
        
    def difference(self,first,second):
        """Get Difference Betwween Two Images"""
        for i in range(0,self.source.shape[0]):
            for j in range(0,self.source.shape[1]):
                diff = (first[i][j][0]-second[i][j][0],first[i][j][1]-second[i][j][1],first[i][j][2]-second[i][j][2])
                self.source[i][j] = diff

    def saveResult(self,path = "./final.jpg"):
        """Saves The image in source at given path"""
        cv.imwrite(path,self.source)
    
    def __tighten(self,value):
        if(value<0):
            return 0
        elif(value>255):
            return 255
        else:
            return value
        
if __name__ == "__main__":
    image = ImageProcessing("C:/Users/OMer/Documents/3scu8q1.jpg")
    
    image.show(delay=1000)
    image.GausianBlur(10)
    image.show(delay=1000)
    image.BlackAndWhite(COLOR.BLUE)
    image.show(delay=1000)
    image.pixelette(10)
    image.show(delay=1000)
    
    image.saveResult()
