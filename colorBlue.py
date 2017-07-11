#! /usr/bin/python

from random import uniform, choice
import math, os, numpy, re
from optparse import OptionParser
#from libsvm.svmutil import *
	
parser = OptionParser(usage=" %prog [options]\n\tLinear regression with regularization (hand written digits from post codes).")
parser.add_option("-b","--binary", dest="binary", action="store_true", default=False, help="Sets the output to binary 1 or -1")
parser.add_option("-q","--questions", dest="quest", default="1", type="int", help="The questions of HW8 we are addressing")
parser.add_option("-r","--runs", dest="runs", default="10", type="int", help="Number of runs for cross validation")
options,args = parser.parse_args()

x = []; y = []; percentage =[]; dubl = 0

# read the data from the files
f = open('color blue data - Dan Meyer',"r")
lines = f.readlines()
N = len(lines)
for line in lines:
	# skip empty lines and lines that begin with #
	if line[0]=='\n' or line[0]=='#':
		N -= 1
		continue
	fields = re.split("\s+",line)
	point = [float(fields[0]), float(fields[1]), float(fields[2])]
	if point in x:
		dubl +=1
		#print point
		continue
	x.append(point)
	if fields[3][-1] == '%':
		p = int(fields[3][0:-1])
		if fields[4] == 'not':
			p = 100 - p
		percentage.append(float(p)/100.0)
	else:
		percentage.append(float(fields[3]))
f.close()

if options.binary:
	y = [ 1.0 if y > 0.5 else -1.0 for y in percentage]
else:
	y = [ 2.0*y - 1 for y in percentage]

y_bin = [ 1.0 if p > 0.5 else -1.0 for p in percentage]


print "Read", N, "data points with ", dubl, "dublicates" 
N = N - dubl

s = sum(y_bin)
print "Majority is", s, "Minority is", (N-abs(s))/2.0

# run the perceptron algorithm 
w = [0,0,0,0]  # starting weight vector, use an extra dimension for the bias/threshold 
iterations = 0; Ebest=1; Wbest=[]
estimate = [math.copysign(1, w[0] + w[1]*x[i][0] + w[2]*x[i][1] + w[3]*x[i][2]) for i in range(N)] 
while y_bin != estimate and iterations < 5000:
	iterations += 1
	# pick a random misclassified point
	missclass = [ i for i in range(N) if y_bin[i] != estimate[i] ]
	p = choice(missclass)
	w[0] += y_bin[p]
	w[1] += y_bin[p]*x[p][0]
	w[2] += y_bin[p]*x[p][1]
	w[3] += y_bin[p]*x[p][2]
	estimate = [math.copysign(1, w[0] + w[1]*x[i][0] + w[2]*x[i][1] + w[3]*x[i][2]) for i in range(N)] 
	if Ebest > sum([1 for i in range(N) if y_bin[i]!=estimate[i]])/float(N):
		Ebest = sum([1 for i in range(N) if y_bin[i]!=estimate[i]])/float(N)
		Wbest = w
print "Perceptron error:", Ebest, "weights:", Wbest, "iterations:", iterations


# Run linear regression algorithm using numpy
X = numpy.array([[1, a[0], a[1], a[2]] for a in x]); Y = numpy.array(y)
# there is a special method that calculates the pseudo-inverse directly
W = numpy.dot( numpy.linalg.pinv(X), Y)

# calculate the output returned by our estimation, on the sample points
estimate = [math.copysign(1, W[0] + W[1]*x[i][0] + W[2]*x[i][1] + W[3]*x[i][2]) for i in range(N)] 
# find its disagreement with the true output to find the error Ein
Ein = sum([1 for i in range(N) if y_bin[i]!=estimate[i]])/float(N)
print "Linear regression error:", Ein, "weights:",W

# form a non-linear sample set, based on the linear one
#Xnl = numpy.array([[1, a[0], a[1], a[2], a[0]*a[1], a[0]*a[2], a[1]*a[2], a[0]*a[0], a[1]*a[1], a[2]*a[2]] for a in x])
#descr = ['1','r', 'g', 'b', 'r*g', 'r*b', 'g*b', 'r*r', 'g*g', 'b*b']
Xnl = numpy.array([[1, a[0], a[1], a[2], a[0]*a[1], a[0]*a[2], a[1]*a[2], a[0]*a[0], a[1]*a[1], a[2]*a[2], a[0]*a[0]*a[0], a[0]*a[0]*a[1], a[0]*a[0]*a[2], a[0]*a[1]*a[2], a[1]*a[1]*a[1], a[1]*a[1]*a[2],a[2]*a[2]*a[2], a[2]*a[2]*a[1],] for a in x])
descr = ['1','r', 'g', 'b', 'r*g', 'r*b', 'g*b', 'r*r', 'g*g', 'b*b', 'r*r*r', 'r*r*g', 'r*r*b', 'r*g*b', 'g*g*g', 'g*g*b', 'b*b*b', 'b*b*g']

#Xnl = numpy.array([[1, a[0], a[1], a[2], a[0]*a[1], a[0]*a[2], a[1]*a[2], a[0]*a[0], a[1]*a[1], a[2]*a[2], a[0]*a[0]*a[0], a[0]*a[0]*a[1], a[0]*a[0]*a[2], a[0]*a[1]*a[2], a[1]*a[1]*a[1], a[1]*a[1]*a[2],a[2]*a[2]*a[2], a[2]*a[2]*a[1], a[0]*a[0]*a[0]*a[0], a[0]*a[0]*a[0]*a[1], a[0]*a[0]*a[0]*a[2], a[0]*a[0]*a[1]*a[1], a[0]*a[0]*a[2]*a[2], a[0]*a[0]*a[1]*a[2], a[1]*a[1]*a[1]*a[1], a[1]*a[1]*a[1]*a[2], a[1]*a[1]*a[1]*a[0], a[1]*a[1]*a[0]*a[2], a[1]*a[1]*a[2]*a[2], a[2]*a[2]*a[2]*a[2], a[2]*a[2]*a[2]*a[1], a[2]*a[2]*a[2]*a[1]] for a in x])
#descr = ['1','r', 'g', 'b', 'r*g', 'r*b', 'g*b', 'r*r', 'g*g', 'b*b', 'r*r*r', 'r*r*g', 'r*r*b', 'r*g*b', 'g*g*g', 'g*g*b', 'b*b*b', 'b*b*g', 'r*r*r*r','r*r*r*g','r*r*r*b','r*r*g*g','r*r*b*b','r*r*g*b','g*g*g*g','g*g*g*b','g*g*g*r','g*g*r*b','g*g*b*b','b*b*b*b','b*b*b*r','b*b*b*g']

# Run again linear regression
Wnl = numpy.dot( numpy.linalg.pinv(Xnl), Y)
	
# find the Ein for the non linear case.
estimate = [math.copysign(1, numpy.dot(Wnl, Xnl[i])) for i in range(N)]
Ein2 = sum([1 for i in range(N) if y_bin[i]!=estimate[i]])/float(N)
print "Non-linear regression error:", Ein2, "weights:", Wnl

#create an equation string to be copied in the input box of "Do you know blue"
equation = ""
for wi, di in zip(Wnl,descr):
	if wi > 0: equation += '+'
	equation += str(wi) +'*'+ di + ' '
equation += ' >0'
print equation

lamda = [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 1]
transform_terms = len(descr)
for l in lamda:
	Wreg = numpy.dot( numpy.dot( numpy.linalg.inv(numpy.dot(Xnl.T, Xnl) + l*numpy.identity(transform_terms)), Xnl.T), Y)
	estimate = [math.copysign(1, numpy.dot(Wreg, Xnl[i])) for i in range(N)]
	Ein2 = sum([1 for i in range(N) if y_bin[i]!=estimate[i]])/float(N)
	print "lamda=", l, "Non-linear regression error:", Ein2, "weights:", Wnl
	
	#create an equation string to be copied in the input box of "Do you know blue"
	equation = ""
	for wi, di in zip(Wnl,descr):
		if wi > 0: equation += '+'
		equation += str(wi) +'*'+ di + ' '
	equation += ' >0'
	print equation

#manual hypothesis, the weighs are for constant, and r, g, b coefficients
w = [40, -1, -1, 1]
estimate = [math.copysign(1, w[0] + w[1]*x[i][0] + w[2]*x[i][1] + w[3]*x[i][2]) for i in range(N)] 
Ein = sum([1 for i in range(N) if y_bin[i]!=estimate[i]])/float(N)
print "Manual hypothesis b+40>r+g. Error:", Ein


# try SVM with RBF kernel and hard margin 
prob  = svm_problem(y_bin, x)
for C in [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]:
	param = svm_parameter('-t 2 -g 1 -c '+str(C)+' -q')
	#param = svm_parameter('-t 1 -d 7 -g 1 -r 1 -c '+str(C)+' -q')
	m = svm_train(prob, param)
	p_labs, p_acc, p_vals = svm_predict(y, x, m, '-q')
	Ein = 1 - p_acc[0]/100.0

	nr_sv = m.get_nr_sv()	
	print "SVM C=", C, "-> Ein:", Ein, "Num of SV:", nr_sv
	
# Do non linear with relularization and validation to choose the best lamda:
lamda = [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 1]
transform_terms = len(descr)
for l in lamda:
	Ein =[]; Eout =[]
#	for r in range(options.runs):
	
	Wreg = numpy.dot( numpy.dot( numpy.linalg.inv(numpy.dot(X.T, X) + l*numpy.identity(transform_terms)), X.T), Y)
	#print Wreg
	# calculate the output returned by our estimation, on the sample points
	estimate = [math.copysign(1, sum([Wreg[j]*Xtrans_in[i][j] for j in range(transform_terms)]) ) for i in range(Nin)] 
	# find its disagreement with the true output to find the error Ein
	Ein = sum([1 for i in range(Nin) if yin[i]!=estimate[i]]) / float(Nin)

	# calculate the output returned by our estimation for the OUT of sample points
	estimate = [math.copysign(1, sum([Wreg[j]*Xtrans_out[i][j] for j in range(transform_terms)]) ) for i in range(Nout)] 
	# find its disagreement with the true output to find the error Eout
	Eout = sum([1 for i in range(Nout) if yout[i]!=estimate[i]]) / float(Nout)

	print "lamda:", l, "Ein is:", Ein, "Eout is:", Eout