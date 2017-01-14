import numpy as np
import math

# calculating priority vector using eigen vector method
def calculateEigenVector(originalMatrix):
	mat = np.array(originalMatrix)

	count = 0
	while True:
		#square the matrix
		newMat = mat.dot(mat)

		#sum all the element in a row
		sumMat = newMat.sum(axis=1)

		#normalise the vector
		totalSum = 0
		for row in sumMat:
			totalSum += float(row)

		newVector = sumMat/float(totalSum)
		
		#iterate until eigenvector found
		countAllElements = 0;

		if count!=0:

			# check if two consecutive vectors are almost same
			diff = abs(np.subtract(newVector , prevVector))
			
			for element in diff:
				if element < 0.000001:
					countAllElements += 1
					continue
				else:
					break
			
			if (countAllElements == len(diff)):
				return newVector
		else:
			count = 1

		prevVector = newVector
		mat = newMat


# Calculating priority vectors using geometric mean method
'''
def calculateEigenVector(C):
	product_vector = []
	for row in C:
		product = 1
		for element in row:
			product = product*element
		product_vector.append(product)

	#Calculating nth roots of product vector element
	root_vector = []
	sumprod = 0
	for prod in product_vector:
		root = math.pow(prod, 0.25)
		sumprod = sumprod + root
		root_vector.append(root)

	W = []
	#Calculating final eigen vector
	for root in root_vector:
		root = root/sumprod
		W.append(root)

	return np.array(W)
'''