import cv2.cv as cv
import sys
import os

def main(av):
    fpath = os.path.dirname(os.path.abspath(__file__))
    f = open(fpath + "/out/secret.txt", "w")
    im = cv.LoadImage(fpath + "/inp/image_steg.png")
    steg = LSBSteg(im)
    f.write(steg.unhideText())
    
class LSBSteg():
    def __init__(self, im):
        self.img = im
        self.w = im.width
        self.h = im.height
        self.size = self.w * self.h
        self.nbchannels = im.channels
        self.mask1Vals = [1,2,4,8,16,32,64,128]
        self.mask1 = self.mask1Vals.pop(0)
        self.mask0Vals = [254,253,251,247,239,223,191,127]
        self.mask0 = self.mask0Vals.pop(0)
        self.curw = 0
        self.curh = 0
        self.curchan = 0
     
    def saveImage(self,filename):
        cv.SaveImage(filename, self.img)
                    
    def nextSpace(self):
        if self.curchan == self.nbchannels-1:
            self.curchan = 0
            if self.curw == self.w-1: 
                self.curw = 0
                if self.curh == self.h-1:
                    self.curh = 0
                    if self.mask1 == 128: 
                        raise SteganographyException, "Image filled"
                    else:
                        self.mask1 = self.mask1Vals.pop(0)
                        self.mask0 = self.mask0Vals.pop(0)
                else:
                    self.curh +=1
            else:
                self.curw +=1
        else:
            self.curchan +=1

    def readBit(self):
        val = self.img[self.curh,self.curw][self.curchan]
        val = int(val) & self.mask1
        self.nextSpace()
        if val > 0:
            return "1"
        else:
            return "0"
    
    def readByte(self):
        return self.readBits(8)
    
    def readBits(self, nb):
        bits = ""
        for i in range(nb):
            bits += self.readBit()
        return bits  
    def unhideText(self):
        ls = self.readBits(16) 
        l = int(ls,2)
        i = 0
        unhideTxt = ""
        while i < l:
            tmp = self.readByte()
            i += 1
            unhideTxt += chr(int(tmp,2))
        return unhideTxt
 
if __name__=="__main__":
    from sys import argv as av
    main(av)