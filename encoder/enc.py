import cv2.cv as cv
import sys
import os

def main(av):
    fpath = os.path.dirname(os.path.abspath(__file__))
    f = open(fpath + "/inp/secret.txt")
    str = f.read()
    carrier = cv.LoadImage(fpath +"/inp/image.jpg")
    steg = LSBSteg(carrier)
    steg.hideText(str)
    steg.saveImage(fpath + "/out/image_steg.png")
    
class LSBSteg():
    def __init__(self, im):
        self.img = im
        self.w = im.width
        self.h = im.height
        self.size = self.w * self.h
        self.nbchannels = im.channels
        self.mask1Vals = [1,2,4,8,16,32,64,128]
        self.mask1Vals = self.mask1Vals.pop(0)
        self.mask0Vals = [254,253,251,247,239,223,191,127]
        self.mask0 = self.mask0Vals.pop(0)
        self.curw = 0
        self.curh = 0
        self.curchan = 0
     
    def saveImage(self,filename):
        cv.SaveImage(filename, self.img)
        
    def putBinaryValue(self, bits): 
        for c in bits:
            val = list(self.img[self.curh,self.curw]) 
            if int(c) == 1:
                val[self.curchan] = int(val[self.curchan]) | self.mask1Vals 
            else:
                val[self.curchan] = int(val[self.curchan]) & self.mask0 
                
            self.img[self.curh,self.curw] = tuple(val)
            self.nextSpace()
        
    def nextSpace(self):
        if self.curchan == self.nbchannels-1:
            self.curchan = 0
            if self.curw == self.w-1: 
                self.curw = 0
                if self.curh == self.h-1:
                    self.curh = 0
                    if self.mask1Vals == 128: 
                        raise SteganographyException, "Image filled"
                    else: 
                        self.mask1Vals = self.mask1Vals.pop(0)
                        self.mask0 = self.mask0Vals.pop(0)
                else:
                    self.curh +=1
            else:
                self.curw +=1
        else:
            self.curchan +=1

    def byteValue(self, val):
        return self.binValue(val, 8)
        
    def binValue(self, val, bitsize):
        binval = bin(val)[2:]
        if len(binval) > bitsize:
            raise SteganographyException, "binary value larger than the expected size"
        while len(binval) < bitsize:
            binval = "0"+binval
        return binval
       
    def hideText(self, txt):
        l = len(txt)
        binl = self.binValue(l, 16) 
        self.putBinaryValue(binl)
        for char in txt: 
            c = ord(char)
            self.putBinaryValue(self.byteValue(c))
 
if __name__=="__main__":
    from sys import argv as av
    main(av)