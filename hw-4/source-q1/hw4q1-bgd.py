#!/usr/bin/python

import os, sys, time
import numpy as np
from numpy import linalg
import timeit

# derivative of hinge by wj 
def hinge(X, Y, w, b, j):
	return 100*sum([0 if Y[i]*(np.dot(X[i], w)+b) >= 1 else -X[i][j]*Y[i] for i in range(len(X))]) # C=100

# compute cost function --- iterates over the whole dataset
def f(X, Y, w, b):
	return linalg.norm(w)**2/2 + 100*sum([max(0, 1.0-Y[i]*(np.dot(w, X[i])+b)) for i in range(len(X))]) # C=100

# derivative of f by b 
def grad_b(X, Y, w, b):
	return 100*sum([0 if Y[i]*(np.dot(X[i], w)+b) >= 1 else -Y[i] for i in range(len(X))]) # C=100

# batch gradient descent
def bgd(X, Y, w, b, ni = 0.0000003, eps = 0.25):
	assert len(X) == len(Y), "Counts do not match"
	k = 0
	crr_f = prev_f = f(X, Y, w, b)
	delta_cost = 1.0
	print "crr_cost: ", crr_f
	while True:
		start = time.time()
		# do the update 
		tw = list(w)
		for j in range(len(X[0])):
			tw[j] = w[j] - ni*(w[j] + hinge(X, Y, w, b, j))
		b = b - ni * grad_b(X, Y, w, b)
		w = list(tw)
		end = time.time()
		print "secs: ", end-start
		print "iter: ", k
		print  "-"*80
		k = k+1
		crr_f = f(X, Y, w, b)
		print "crr_cost: ", crr_f
		delta_cost = (abs(prev_f - crr_f))*100/(prev_f)
		print "delta_cost: ", delta_cost
		if delta_cost < eps:
			print "Converged after", k, "steps!"
			break
		prev_f = crr_f
	print "w=", w
	print "b=", b
	return (w, b)

def load_train(fname):
	return [[int(el) for el in line.split(',')] for line in open(fname).read().split()]

def load_test(fname):
	return [int(el) for el in open(fname).read().split()]

# entry point 
if __name__ == '__main__':
	#X = load_train('features.txt')
	#Y = load_test('target.txt')
	#w = [0 for x in range(len(X[0]))]
	#b = 0
	#(w, b) = bgd(X, Y, w, b)
	s = "	X = load_train('features.txt')\n\
	Y = load_test('target.txt')\n\
	w = [0 for x in range(len(X[0]))]\n\
	b = 0\n\
	(w, b) = bgd(X, Y, w, b)"
	print(timeit.timeit(s, setup="from __main__ import *", number=1))
