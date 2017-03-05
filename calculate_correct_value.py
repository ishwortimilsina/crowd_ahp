import operator
import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import find_faulty_comparisons as ffc

def calculateCorrectValue(originalMatrix, archiveIndex=[]):
	
	# print "Archived Indices ---- > " + str(archiveIndex)

	faultDict = ffc.findFault(originalMatrix)
	
	# create a sorted array based on value of all keys in the dictionary
	sorted_fault = sorted(faultDict.items(), key=operator.itemgetter(1), reverse=False)
	
	for key in sorted_fault:
		
		# to make example 3_4_left tp 3_4
		splitKey = key[0].split('_')
		matIndex = splitKey[0]+"_"+splitKey[1]

		# if the key is in the archiveIndex it means we do not want to process this anymore
		# ignore this, continue to next index
		if str(matIndex) in archiveIndex:
			continue

		# split index to get the row and column position of the value to be changed
		# splitIndex = matIndex.split('_')
		# i = int(splitIndex[0])-1
		# j = int(splitIndex[1])-1
		# tempMatrix = np.array(originalMatrix[0])

		# # substitute each i,j and j,j with 0 and corresponding diagonal elements with 2
		# tempMatrix[i][j] = 0
		# tempMatrix[j][i] = 0
		# tempMatrix[i][i] = 2
		# tempMatrix[j][j] = 2

		# # get the eigen vector
		# eigen_vector = ce.calculateEigenVector(tempMatrix)

		# # get the consistency
		# consVal = cc.consistency(tempMatrix, eigen_vector)

		# # if the required value doesn't fall in the confidence interval no need to get more input
		flag = True
		if key[1] >= 0.1:
			flag = False

		# return the index of the value to be changed and the value to be changed to	
		# return (matIndex, eigen_vector[i]/eigen_vector[j], consVal[0], flag)
		return (matIndex, flag)
