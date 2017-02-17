import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import extract_new_alternative_comparisons as enac
import extract_new_criteria_comparisons as encc
import calculate_correct_value as ccv
import find_faulty_comparisons as ffc

def correctifyFault(fault_detail, originalMatrix, goal, criteria=None):
	
	numOfRecords = 2

	tempMatrix = originalMatrix

	faultDict = ffc.findFault(originalMatrix)

	archiveIndex = []

	while(True):
		# get the index of the comparison to correct
		matIndex = fault_detail[0]

		#get the row and column position of the index
		splitIndex = matIndex.split('_')
		i = int(splitIndex[0])-1
		j = int(splitIndex[1])-1

		## Let's extract additional 10 records from the database table for this particular comparisons
		
		if (criteria):
			newValueSet = enac.getNextAlternativesComparisons(len(originalMatrix), goal, criteria, i+1, j+1, numOfRecords)
		else:
			newValueSet = encc.getNextCriteriaComparisons(len(originalMatrix), goal, i+1, j+1, numOfRecords)
			
		newValue = newValueSet[0]
		conf_interval = newValueSet[1]

		tempMatrix[i][j] = newValue
		tempMatrix[j][i] = 1/float(newValue)

		eigen_vector = ce.calculateEigenVector(tempMatrix)

		consVal = cc.consistency(tempMatrix, eigen_vector)

		print consVal
		if consVal[0] == True:
			return eigen_vector
		else:
			print "********************************Iterating again*************************************"

			fault_detail = ccv.calculateCorrectValue(originalMatrix, archiveIndex)

			if fault_detail[0] == matIndex:
				if numOfRecords > 20 and newValueSet[2] == True:
			 		numOfRecords = 1

			 		# to stop the particular comparison being extracted indefinitely
			 		if matIndex not in archiveIndex:
			 			archiveIndex.append(matIndex)

			 		fault_detail = ccv.calculateCorrectValue(originalMatrix, archiveIndex)
				numOfRecords += 1
			else:
				numOfRecords = 1
				numOfRecords += 1

			print "NUMBER OF RECORDS ----- " + str(numOfRecords)