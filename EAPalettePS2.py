import os
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("palette")
parser.add_argument("-r","--removealpha", action= "store_true", help="Remove alpha")
parser.add_argument("-u","--unswizzle", action= "store_true", help="Unswizzle palette")
args = parser.parse_args()

def swapRB(color):
    newColor = (color & 0xFF00FF00) | ((color >> 16) & 0x000000FF) | ((color << 16) & 0x00FF0000)
    return newColor

if args.removealpha == True and args.unswizzle == False:
    
    f0 = open(args.palette,"rb")
    f1 = open("out-noalpha","wb")
    
    for i in range(0,0x100):
        color = struct.unpack('i', f0.read(4))[0]
        f1.write(struct.pack("i", color))
        f1.seek(-0x01, os.SEEK_CUR)
        f1.write(bytearray([0x80]))
    
    f0.close()
    f1.close()
    
if args.unswizzle == True and args.removealpha == False:
    
    f0 = open(args.palette,"rb")    
    f1 = open("out-unswizzle","wb")
    count = 0
    swapCount = 0
    block0 = []
    block1 = []
    
    while count != 0x100:

        color = struct.unpack('i', f0.read(4))[0]
        f1.write(struct.pack("I", swapRB(color)))
        count += 1
        swapCount += 1

        if count == 8 or swapCount == 16:
            for i in range(0,8):
                color = struct.unpack('i', f0.read(4))[0]
                block0+=[color]

            for i in range(0,8):
                color = struct.unpack('i', f0.read(4))[0]
                block1+=[color]

            for i in range(0,8):
                f1.write(struct.pack("I", swapRB(block1[i])))

            for i in range(0,8):
                f1.write(struct.pack("I", swapRB(block0[i])))

            block0=[]
            block1=[]

            count += 16
            swapCount = 0

    f0.close()
    f1.close()
