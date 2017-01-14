import csv
import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import find_faulty_comparisons as ffc

def processOneMatrix(goal, criteria=None):
	if (criteria):
		originalMatrix = am.getAlternativesCriteriaMatrix(goal, criteria)
	else:
		originalMatrix = cm.getCriteriaMatrix(goal)

	eigenVector = ce.calculateEigenVector(originalMatrix);

	consistencyRatio = cc.consistency(originalMatrix, eigenVector)

	if consistencyRatio[0] == True:
		return eigenVector
	else:
		return ffc.findFault(originalMatrix)