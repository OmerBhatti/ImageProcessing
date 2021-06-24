from library import *

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
