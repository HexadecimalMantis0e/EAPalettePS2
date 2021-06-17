import os
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("palette")
args = parser.parse_args()

def swapRB(color):
    newColor = (color & 0xFF00FF00) | ((color >> 16) & 0x000000FF) | ((color << 16) & 0x00FF0000)
    return newColor

count = 0
swapCount = 0
block0 = []
block1 = []
f0 = open(args.palette, "rb")
f1 = open("out", "wb")
print("Unswizzling palette...")

while count != 0x100:
    color = struct.unpack('I', f0.read(4))[0]
    f1.write(struct.pack('I', swapRB(color)))
    count += 1
    swapCount += 1

    if count == 8 or swapCount == 16:
        for i in range(0, 8):
            color = struct.unpack('I', f0.read(4))[0]
            block0 += [color]

        for i in range(0, 8):
            color = struct.unpack('I', f0.read(4))[0]
            block1 += [color]

        for i in range(0, 8):
            f1.write(struct.pack('I', swapRB(block1[i])))

        for i in range(0, 8):
            f1.write(struct.pack('I', swapRB(block0[i])))

        block0 = []
        block1 = []
        count += 16
        swapCount = 0

print("Done!...")
f0.close()
f1.close()
