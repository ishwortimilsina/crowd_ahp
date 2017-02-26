import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import extract_new_alternative_comparisons as enac
import extract_new_criteria_comparisons as encc
import calculate_correct_value as ccv
import find_faulty_comparisons as ffc

def printFinalDetail(indexDict):
	print "After resolving incosistency"
	print "______________________________________________________________________________________"
	for key in indexDict:
		print "Total numbers of inputs needed for " + key + " ---->  " + str(indexDict[key][0]) + " ---> Reformed Mean ---> " + str(indexDict[key][1]) + " ---> Reformed Confidence Interval ---> " + str(indexDict[key][2]) 
	print "______________________________________________________________________________________"
	print "***************************************************************************************\n"

def correctifyFault(fault_detail, originalMatrix, goal, criteria=None):
	
	numOfRecords = 4

	tempMatrix = originalMatrix[0]

	faultDict = ffc.findFault(originalMatrix[0])

	archiveIndex = []

	indexDict = {}

	numOfRecords = originalMatrix[1][fault_detail[0]][2]+1

	while(True):
		print "Calculating correct value for " + fault_detail[0]
		
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

		eigen_vector = ce.calculateEigenVector(tempMatrix)

		consVal = cc.consistency(tempMatrix, eigen_vector)

		indexDict[matIndex].append(newValueSet[3])
		indexDict[matIndex].append(newValueSet[1])

		if consVal[0] == True:
			print "\n"
			printFinalDetail(indexDict)
			print "\n"
			# print tempMatrix
			# print "\n"
			return eigen_vector
		else:
			# print "\n********************************Iterating again*************************************\n"

			fault_detail = ccv.calculateCorrectValue(tempMatrix, archiveIndex, newValueSet[1][0], newValueSet[1][1])
			
			if fault_detail[0] == matIndex:
				
				if (numOfRecords > 20 and newValueSet[2] == True) or fault_detail[3]==False:

			 		# to stop the particular comparison being extracted indefinitely
			 		if matIndex not in archiveIndex:
			 			archiveIndex.append(matIndex)

			 		# calculate fault detail again with updated archiveIndex
			 		fault_detail = ccv.calculateCorrectValue(tempMatrix, archiveIndex, newValueSet[1][0], newValueSet[1][1])
			 		
			 		# if the index was already taken atleast once before, take num of records from indexDict
			 		if fault_detail[0] in indexDict:
						numOfRecords = indexDict[fault_detail[0]][0]
					else:
			 			numOfRecords = originalMatrix[1][fault_detail[0]][2]

				numOfRecords += 1
			else:
				if fault_detail[0] in indexDict:
					numOfRecords = indexDict[fault_detail[0]][0]
				else:
		 			numOfRecords = originalMatrix[1][fault_detail[0]][2]
				
				numOfRecords += 1


	return eigen_vector
