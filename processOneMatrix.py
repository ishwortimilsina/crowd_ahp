import csv
import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import find_faulty_comparisons as ffc
import calculate_correct_value as ccv

def processOneMatrix(goal, criteria=None):
	if (criteria):
		originalMatrix = am.getAlternativesCriteriaMatrix(goal, criteria)
	else:
		originalMatrix = cm.getCriteriaMatrix(goal)

	#calculate eigen vector
	eigenVector = ce.calculateEigenVector(originalMatrix);

	#calculate consistency
	consistencyRatio = cc.consistency(originalMatrix, eigenVector)

	# if consistent, return eigenvector other find faulty comparison and correct
	if consistencyRatio[0] == True:
		return eigenVector
	else:
		# find faulty comparison and calculate value that is optimal
		fault_detail = ccv.calculateCorrectValue(originalMatrix)

		matIndex = fault_detail[0]
		
		splitIndex = matIndex.split('_')
		i = int(splitIndex[0])-1
		j = int(splitIndex[1])-1
		tempMatrix = np.array(originalMatrix)

		# change the faulty comparisons to new correct value
		tempMatrix[i][j] = float(fault_detail[1])
		tempMatrix[j][i] = 1/float(fault_detail[1]) #reciprocal

		eigen_vector = ce.calculateEigenVector(tempMatrix)
		
		#return the eigen vector
		return eigen_vector



