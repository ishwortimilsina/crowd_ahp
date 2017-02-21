import csv
import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import find_faulty_comparisons as ffc
import operator

def calculateCorrectValue(originalMatrix, archiveIndex=[]):
	
	#print "Archived Indices ---- > " + str(archiveIndex)

	faultDict = ffc.findFault(originalMatrix)

	# create a sorted array based on value of all keys in the dictionary
	sorted_fault = sorted(faultDict.items(), key=operator.itemgetter(1), reverse=True)
	
	for key in sorted_fault:
		
		# if the key is in the archiveIndex it means we do not want to process this anymore
		# ignore this, continue to next index
		if str(key[0]) in archiveIndex:
			continue
			
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

		# return the index of the value to be changed and the value to be changed to

		return (matIndex, eigen_vector[i]/eigen_vector[j], consVal[0])
