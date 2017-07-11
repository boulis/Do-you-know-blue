#! /usr/bin/python

from PIL import Image
import re
    

# list the image files we will process, along with a flag that shows if they contain blue colors or not
imageFiles = [["Blue is - 4304 colours.png", True],["Blue is Not - 4304 colours.png", False]]

outputFile = open("do_you_know_blue_4304colors.csv", 'w')
outputFile.write('r,g,b,isblue\n')

colorBoxSize = 20  #in pixels, each color box is 20 x 20
boxCentre = colorBoxSize/2

total = 0; blues = 0

for file, isblue in imageFiles:
    im = Image.open(file);
    width, height = im.size
    columns = width/colorBoxSize
    rows = height/colorBoxSize
    print "Image w x h:", width, height, "Rows, columns", rows, columns  
    pixels = list(im.getdata()) # read all the pixels of the image
    # traverse the image box steps to get every box's color 
    offset = boxCentre + width*boxCentre
    for i in range(rows):
        for j in range(columns):
            r, g, b = pixels[offset + i*width*colorBoxSize + j*colorBoxSize]
            if (r==255) and (g==255) and (b==255):
                print "Found white box and stopped with this file. Row, col:", i, j
                break  # this can happen only at the last row. Break and the outer (rows) loop will terminate too.
            outputFile.write('{},{},{},{}\n'.format(r,g,b,isblue))
            total+=1
            if isblue: blues+=1


outputFile.close()
    
print "Images:", blues, "blue points and ", total-blues, "non blue points. Total:", total

# know convert a totally different file

total = 0; blues = 0
outputFile = open("xkcd_colors.csv", 'w')
outputFile.write('r,g,b,color\n')

inputfile = open("satfaces.txt",'r')

lines = inputfile.readlines()
for line in lines:
    # Split the line when you find a '[' or a '] ', or a ', ' 
    # Notice the extra spaces in 2 of the 3 separators. We also need to esc the characters [ ]  
    _, r, g, b, color = re.split("\[|, |\] ",line)  
    outputFile.write('{},{},{},{}'.format(r,g,b,color))   # the newline is already there in the color string
    total+=1
    if 'blue' in color or 'cyan' in color : blues+=1

outputFile.close()
inputfile.close()

print "XKCD:", blues, "blue entries and ", total-blues, "non blue entries. Total:", total


