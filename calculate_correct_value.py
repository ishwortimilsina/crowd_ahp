import csv
import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import find_faulty_comparisons as ffc
import operator

def calculateCorrectValue(originalMatrix):
	faultDict = ffc.findFault(originalMatrix)

	# create a sorted array based on value of all keys in the dictionary
	sorted_fault = sorted(faultDict.items(), key=operator.itemgetter(1))
	
	for key in sorted_fault:
		# get the index of each value
		matIndex = key[0]
		
		# split index to get the row and column position of the value to be changed
		splitIndex = matIndex.split('_')
		i = int(splitIndex[0])-1
		j = int(splitIndex[1])-1
		tempMatrix = np.array(originalMatrix)

		# substitute each i,j and j,j with 0 and corresponding diagonal elements with 2
		tempMatrix[i][j] = 0
		tempMatrix[j][i] = 0
		tempMatrix[i][i] = 2
		tempMatrix[j][j] = 2

		# get the eigen vector
		eigen_vector = ce.calculateEigenVector(tempMatrix)
		# get the consistency
		consVal = cc.consistency(tempMatrix, eigen_vector)

		# if the new matrix is consistent, break the loop otherwise continue
		if (consVal[0] == True):
			break

	if (consVal[0] == False):
		print "\n*****************************************************************************"
		print "The whole matrix is wildly inconsistent. Consider restarting the whole process."
		print "*******************************************************************************\n"

	# return the index of the value to be changed and the value to be changed to
	return (matIndex, eigen_vector[i]/eigen_vector[j])
