#! /usr/bin/python

from random import uniform, choice
import math, os, numpy, re, itertools
from optparse import OptionParser
#from libsvm.svmutil import *
from PIL import Image	
	
parser = OptionParser(usage=" %prog [options]\n\tFinding separating i-degree planes for the Do you know blue contest.")
parser.add_option("-e","--equation", dest="equation", action="store_true", default=False, help="Prints out the inequalities produced by the weights")
parser.add_option("-d","--degree", dest="degree", default="6", type="int", help="Maximum degree polynomial that we will try in the non linear transform")
parser.add_option("-r","--runs", dest="runs", default="10", type="int", help="Number of runs for cross validation")
options,args = parser.parse_args()

# list all the files we will process, along with a flag that shows if they contain blue colors (1) or non blue (-1)
imageFiles = [["Blue is - 4124 colors total.png", 1], ["Blue is Not 1- 4124 colors total.png", -1], ["Blue is Not 2- 4124 colors total.png", -1], ["Blue is Not 3- 4124 colors total.png", -1]]
imageFiles = [["Blue is - 4304 colours.png", 1],["Blue is Not - 4304 colours.png", -1]]


colorBoxSize = 20  #in pixels, each color box is 20 x 20
boxCentre = colorBoxSize/2

x = []; y = []; N = 0

for file, blueValue in imageFiles:
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
			x.append([r/100.0,g/100.0,b/100.0]); y.append(blueValue); N += 1

	
blue = (N + sum(y))/2  #sum(y) is negative as the non blue points are many more
nonBlue = N - blue
print blue, "blue points and ", nonBlue, "non blue points. Total points:", N

# read the values from a text file I created from the list of test colours the website was giving. Use it as an in-sample set
yin = []; xin = []; percentage =[]
# read the data from the files
f = open('color blue data - Dan Meyer',"r")
lines = f.readlines()
Nin = len(lines)
for line in lines:
	# skip empty lines and lines that begin with #
	if line[0]=='\n' or line[0]=='#':
		Nin -= 1; continue
	fields = re.split("\s+",line)
	point = [float(fields[0]), float(fields[1]), float(fields[2])]
	if point in xin:
		Nin -= 1; continue
	xin.append(point)
	if fields[3][-1] == '%':
		p = int(fields[3][0:-1])
		if fields[4] == 'not':
			p = 100 - p
		percentage.append(float(p)/100.0)
	else:
		percentage.append(float(fields[3]))
f.close()

yin = [ 1.0 if p > 0.5 else -1.0 for p in percentage]
blueIn = (Nin + sum(yin))/2
print "In-sample points. Blue", blueIn, "non blue", Nin- blueIn, "total:", Nin

print "=== Non-linear regression errors for varying polynomial degrees ===\n"

for Q in range(options.degree +1):
	# shows a description of the non linear transform we are applying in terms of r,g,b values. Used in the equation string we build
	descr = [reduce(lambda head, tail: head+'*'+tail, subset) for n in range(1, Q+1) for subset in itertools.combinations_with_replacement(['r','g','b'], n)]
	descr.insert(0,'1') 
 
 	print "Degree =",Q, "==> non linear point contains", len(descr), "terms"
 	
	# A nice (and somewhat obsure) way to get all non linear terms of  Many features:
	# Double list comprehension (outer loop goes FIRST)
	# reduce with starting value, so the empty list returns just this value
	Xnl = numpy.array([[reduce(lambda head, tail: head*tail, subset, 1) for n in range(Q+1) for subset in itertools.combinations_with_replacement(point, n)] for point in x])
	Y = numpy.array(y)

	# Run linear regression
	Wnl = numpy.dot( numpy.linalg.pinv(Xnl), Y)

	# find the Ein for the non linear case.
	estimate = [math.copysign(1, numpy.dot(Wnl, Xnl[i])) for i in range(N)]
	E = sum([1 for i in range(N) if y[i]!=estimate[i]])/float(N)
	print "\tALL", N, "points. Error:\t %.5f\t Accuracy: %.5f" % (E, 1-E)

	Wnew = numpy.array(map(float,map(str, Wnl)))
	estimate = [math.copysign(1, numpy.dot(Wnew, Xnl[i])) for i in range(N)]
	E = sum([1 for i in range(N) if y[i]!=estimate[i]])/float(N)
	print "\tALL", N, "pts new. Error:\t %.5f\t Accuracy: %.5f" % (E, 1-E)
	
	if options.equation:
		#create an equation string to be copied in the input box of "Do you know blue"
		equation = ""
		for wi, di in zip(Wnl,descr):
			if wi > 0: equation += '+'
			equation += str(wi) +'*'+ di +'/1'+ '0'*(len(di)+1) +'.0 '
		equation += ' >0'
		print equation


	# do it again for a limited number of samples (in sample) and test the results against all samples
	Xnl_in = numpy.array([[reduce(lambda head, tail: head*tail, subset, 1) for n in range(Q+1) for subset in itertools.combinations_with_replacement(point, n)] for point in xin])
	Y = numpy.array(yin)	
	# Run linear regression
	Wnl_in = numpy.dot( numpy.linalg.pinv(Xnl_in), Y)

	# find the Ein for the non linear case.
	estimate = [math.copysign(1, numpy.dot(Wnl_in, Xnl_in[i])) for i in range(Nin)]
	Ein = sum([1 for i in range(Nin) if yin[i]!=estimate[i]])/float(Nin)
	print '\t', Nin, "points only. Ein:\t %.5f\t Accuracy: %.5f" % (Ein, 1-Ein)
	# find the Ein for the non linear case.
	estimate = [math.copysign(1, numpy.dot(Wnl_in, Xnl[i])) for i in range(N)]
	Eout = sum([1 for i in range(N) if y[i]!=estimate[i]])/float(N)
	print '\t', Nin, "points only. Eout:\t %.5f\t Accuracy: %.5f" % (Eout, 1-Eout)

	if options.equation:
		#create an equation string to be copied in the input box of "Do you know blue"
		equation = ""
		for wi, di in zip(Wnl_in,descr):
			if wi > 0: equation += '+'
			equation += str(wi) +'*'+ di + ' '
		equation += ' >0'
		print equation

	print '\n'