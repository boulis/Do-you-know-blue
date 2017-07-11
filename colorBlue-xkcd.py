#! /usr/bin/python

from random import uniform, choice
import math, os, numpy, re
from optparse import OptionParser
from libsvm.svmutil import *
	
parser = OptionParser(usage=" %prog [options]\n\tLinear regression with regularization (hand written digits from post codes).")
parser.add_option("-b","--binary", dest="binary", action="store_true", default=False, help="Sets the output to binary 1 or -1")
parser.add_option("-q","--questions", dest="quest", default="1", type="int", help="The questions of HW8 we are addressing")
parser.add_option("-r","--runs", dest="runs", default="10", type="int", help="Number of runs for cross validation")
options,args = parser.parse_args()

x = []; y = []; percentage =[]; Nb = 0; N0=0

# read the data from the files
f = open('satfaces.txt',"r")
lines = f.readlines()
for line in lines[0::10]:

	fields = re.split("[],[]",line)  #splits the line where it finds ] [ ,  The first element is empty
	#print line, fields
	point = [int(fields[1]), int(fields[2]), int(fields[3])]
	x.append(point)
	
	# add an extra point with ALL non zero values but still close enough to the color of the original 
	extra_point = point
	extra_value = 0.3*sum(point)
	zeros = float(sum([i==0 for i in point]))
	extra_point = [ p if p >0 else extra_value/zeros for p in point]
	x.append(extra_point)
	
	# search for the patern blue or cyan at the last field, which is the desription of the colour. re.I means case indifferent, 
	# r in front of the string means raw string (good idea if we are using regex, not really used here) 
	if re.search(r"blue|cyan", fields[-1], re.I):
		y.append(1); y.append(1); Nb += 2
	else:
		y.append(-1); y.append(-1); N0 +=2
		
f.close()

N= Nb+N0
print Nb, N0, N

Y = numpy.array(y)
#Xnl = numpy.array([[1, a[0], a[1], a[2], a[0]*a[1], a[0]*a[2], a[1]*a[2], a[0]*a[0], a[1]*a[1], a[2]*a[2]] for a in x])
#descr = ['1','r', 'g', 'b', 'r*g', 'r*b', 'g*b', 'r*r', 'g*g', 'b*b']
Xnl = numpy.array([[1, a[0], a[1], a[2], a[0]*a[1], a[0]*a[2], a[1]*a[2], a[0]*a[0], a[1]*a[1], a[2]*a[2], a[0]*a[0]*a[0], a[0]*a[0]*a[1], a[0]*a[0]*a[2], a[0]*a[1]*a[2], a[1]*a[1]*a[1], a[1]*a[1]*a[2],a[2]*a[2]*a[2], a[2]*a[2]*a[1]] for a in x])
descr = ['1','r', 'g', 'b', 'r*g', 'r*b', 'g*b', 'r*r', 'g*g', 'b*b', 'r*r*r', 'r*r*g', 'r*r*b', 'r*g*b', 'g*g*g', 'g*g*b', 'b*b*b', 'b*b*g']

Xnl = numpy.array([[1, a[0], a[1], a[2], a[0]*a[1], a[0]*a[2], a[1]*a[2], a[0]*a[0], a[1]*a[1], a[2]*a[2], a[0]*a[0]*a[0], a[0]*a[0]*a[1], a[0]*a[0]*a[2], a[0]*a[1]*a[2], a[1]*a[1]*a[1], a[1]*a[1]*a[2],a[2]*a[2]*a[2], a[2]*a[2]*a[1], a[0]*a[0]*a[0]*a[0], a[0]*a[0]*a[0]*a[1], a[0]*a[0]*a[0]*a[2], a[0]*a[0]*a[1]*a[1], a[0]*a[0]*a[2]*a[2], a[0]*a[0]*a[1]*a[2], a[1]*a[1]*a[1]*a[1], a[1]*a[1]*a[1]*a[2], a[1]*a[1]*a[1]*a[0], a[1]*a[1]*a[0]*a[2], a[1]*a[1]*a[2]*a[2], a[2]*a[2]*a[2]*a[2], a[2]*a[2]*a[2]*a[1], a[2]*a[2]*a[2]*a[1]] for a in x])
descr = ['1','r', 'g', 'b', 'r*g', 'r*b', 'g*b', 'r*r', 'g*g', 'b*b', 'r*r*r', 'r*r*g', 'r*r*b', 'r*g*b', 'g*g*g', 'g*g*b', 'b*b*b', 'b*b*g', 'r*r*r*r','r*r*r*g','r*r*r*b','r*r*g*g','r*r*b*b','r*r*g*b','g*g*g*g','g*g*g*b','g*g*g*r','g*g*r*b','g*g*b*b','b*b*b*b','b*b*b*r','b*b*b*g']

# Run again linear regression
Wnl = numpy.dot( numpy.linalg.pinv(Xnl), Y)
	
# find the Ein for the non linear case. Just checking, the homework does not ask for it.
estimate = [math.copysign(1, numpy.dot(Wnl, Xnl[i])) for i in range(N)]
Ein2 = sum([1 for i in range(N) if y[i]!=estimate[i]])/float(N)
print "Non-linear regression error:", Ein2, "weights:", Wnl

#create an equation string to be copied in the input box of "Do you know blue"
equation = ""
for wi, di in zip(Wnl,descr):
	if wi > 0: equation += '+'
	equation += str(wi) +'*'+ di + ' '
equation += ' >0'
print equation