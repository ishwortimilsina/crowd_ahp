import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import simulate_new_data as smd
import sqlite3
import extract_new_alternative_comparisons as enac
import extract_new_criteria_comparisons as encc
import calculate_correct_value as ccv
import find_faulty_comparisons as ffc

def writeIntoDatabase(column1, column2, data, goal, criteria=None):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	for single in data:
		if (criteria):
			query = 'INSERT OR IGNORE INTO {tn} (goal_id, alternative_1_id, alternative_2_id, value, criteria_id) VALUES ({goal}, {column1}, {column2}, {single}, {criteria_id})'.\
							format(tn='alternatives_comparisons', column1=column1, column2=column2, single=single, criteria_id=criteria, goal=goal)
		else:
			query = 'INSERT OR IGNORE INTO {tn} (goal_id, criteria_1_id, criteria_2_id, value) VALUES ({goal}, {column1}, {column2}, {single})'.\
							format(tn='criteria_comparisons', column1=column1, column2=column2, single=single, goal=goal)
		c.execute(query)

	conn.commit()
	conn.close()

def correctifyFault(fault_detail, originalMatrix, goal, criteria=None, numOfRecords=None):
	changeIndex = 0

	tempMatrix = originalMatrix

	faultDict = ffc.findFault(originalMatrix)

	while(True):
		# get the index of the comparison to correct
		matIndex = fault_detail[0]

		#get the row and column position of the index
		splitIndex = matIndex.split('_')
		i = int(splitIndex[0])-1
		j = int(splitIndex[1])-1

		## Let's extract additional 10 records from the database table for this particular comparisons
		
		if (criteria):
			newValue = enac.getNextAlternativesComparisons(len(originalMatrix), goal, criteria, i+1, j+1, numOfRecords)
		else:
			newValue = encc.getNextCriteriaComparisons(len(originalMatrix), goal, i+1, j+1, numOfRecords)

		tempMatrix[i][j] = newValue
		tempMatrix[j][i] = 1/float(newValue)

		eigen_vector = ce.calculateEigenVector(tempMatrix)

		consVal = cc.consistency(tempMatrix, eigen_vector)

		print consVal
		if consVal[0] == True:
			return eigen_vector
		else:
			print "********************************Iterating again*************************************"
			# return new eigenvector with consistent comparisons
			if numOfRecords > 60:
				changeIndex += 1
				numOfRecords = 10
				fault_detail = ccv.calculateCorrectValue(originalMatrix, faultDict, changeIndex)
			else:
				fault_detail = ccv.calculateCorrectValue(originalMatrix, faultDict, changeIndex)
			print "NUMBER OF RECORDS ----- " + str(numOfRecords)

			numOfRecords += 10
			'''
			if (criteria):
				return correctifyFault(fault_detail, originalMatrix, goal, criteria, numOfRecords+10)
			else:
				return correctifyFault(fault_detail, originalMatrix, goal, None, numOfRecords+10)
			'''




	# Get new data to overcome the inconsistency
	#newData = smd.simulateNewData(fault_detail[1], 100)

	#write the new data into the database
	#if (criteria):
	#	writeIntoDatabase(i+1, j+1, newData, goal, criteria)
	#else:
	#	writeIntoDatabase(i+1, j+1, newData, goal)


	# recalculate the eigenvectors using the newly gained data
	'''
	if (criteria):
		tempMatrix = am.getAlternativesCriteriaMatrix(goal, criteria, numOfRecords)
	else:
		tempMatrix = cm.getCriteriaMatrix(goal, numOfRecords)

	eigen_vector = ce.calculateEigenVector(tempMatrix)
	'''