import csv
import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import find_faulty_comparisons as ffc
import calculate_correct_value as ccv
import correctify_fault as cf

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
		print "Matrix is inconsistent. Trying to resolve this"
		# find faulty comparison and calculate value that is optimal
		fault_detail = ccv.calculateCorrectValue(originalMatrix)

		# return new eigenvector with consistent comparisons
		if (criteria):
			return cf.correctifyFault(fault_detail, originalMatrix, goal, criteria)
		else:
			return cf.correctifyFault(fault_detail, originalMatrix, goal)