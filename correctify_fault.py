import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import extract_new_alternative_comparisons as enac
import extract_new_criteria_comparisons as encc
import calculate_correct_value as ccv
import find_faulty_comparisons as ffc

def printAndReturn (consVal, indexDict, originalDetails):
	totalSum = printFinalDetail(indexDict, originalDetails)
	print "\n"
	if consVal[0] == True:
		print "Consistent, CR = " + str(consVal[1])
	else:
		print "Inconsistent, CR = " + str(consVal[1])

	print "\n"
	print "Total number of inputs : " + str(totalSum)

def printFinalDetail(indexDict, originalDetails):
	sumx = 0
	
	for key in indexDict:
		print "Cell "+key+"--> Inputs: " + str(indexDict[key][0]) + "; Mean: " + str(indexDict[key][1]) + "; Confidence Interval: " + str(indexDict[key][2])
		sumx = sumx + indexDict[key][0] - originalDetails[key][2]

	totalSum = 0
	for key in originalDetails:
		if key in indexDict:
			totalSum = totalSum + indexDict[key][0]
		else:
			totalSum = totalSum + originalDetails[key][2]

	print "Stage 2 inputs : " + str(sumx)
	return str(totalSum)

def correctifyFault(fault_detail, originalMatrix, goal, criteria=None):

	originalDetails = dict(originalMatrix[1])

	tempMatrix = originalMatrix[0]
	tempCellDetails = originalMatrix[1]

	faultDict = ffc.findFault(originalMatrix)

	archiveIndex = []

	indexDict = {}

	numOfRecords = originalMatrix[1][fault_detail[0]][2]+1

	while(True):
		# print "Calculating correct value for " + fault_detail[0]
		
		# get the index of the comparison to correct
		matIndex = fault_detail[0]

		# update number of records for this index 
		indexDict[matIndex] = [numOfRecords]
		
		#get the row and column position of the index
		splitIndex = matIndex.split('_')
		i = int(splitIndex[0])-1
		j = int(splitIndex[1])-1

		## Let's extract additional 10 records from the database table for this particular comparisons
		if (criteria):
			newValueSet = enac.getNextAlternativesComparisons(len(tempMatrix), goal, criteria, i+1, j+1, numOfRecords)
		else:
			newValueSet = encc.getNextCriteriaComparisons(len(tempMatrix), goal, i+1, j+1, numOfRecords)
			
		newValue = newValueSet[0]
		conf_interval = newValueSet[1]

		tempMatrix[i][j] = newValue
		tempMatrix[j][i] = 1/float(newValue)

		# update the detail of the particular cell/index 
		tempCellDetails[matIndex] = (newValue, conf_interval, numOfRecords)
		
		eigen_vector = ce.calculateEigenVector(tempMatrix)

		consVal = cc.consistency(tempMatrix, eigen_vector)

		indexDict[matIndex].append(newValueSet[3]) # add mean to the indexDict
		indexDict[matIndex].append(conf_interval) # add conf_interval to the indexDict

		if consVal[0] == True: # The matrix is resolved. return the eigen vector
			printAndReturn (consVal, indexDict, originalDetails)
			return eigen_vector

		else: # The matrix is not resolved yet. Keep trying
			
			# print "\n********************************Iterating again*************************************\n"

			# If the lowest CR in the CRdict is not less than the mean CR of the matrix
			# there's no point carrying on
			if fault_detail[1] == False:
				printAndReturn (consVal, indexDict, originalDetails)
				return eigen_vector

			if (newValueSet[2] == True):

		 		# to stop the particular comparison being extracted indefinitely
		 		if matIndex not in archiveIndex:
		 			archiveIndex.append(matIndex)

		 		# calculate fault detail again with updated archiveIndex
		 		fault_detail = ccv.calculateCorrectValue([tempMatrix, tempCellDetails], archiveIndex, consVal[1])
		 	

	 		# if the index was already taken atleast once before, take num of records from indexDict
	 		if fault_detail != None:
		 		if fault_detail[0] in indexDict:
					numOfRecords = indexDict[fault_detail[0]][0]
				else:
		 			numOfRecords = originalMatrix[1][fault_detail[0]][2]
		 	else:
		 		break

			numOfRecords += 1

	printAndReturn (consVal, indexDict, originalDetails)
	return eigen_vector