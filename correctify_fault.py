import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import simulate_new_data as smd
import sqlite3

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

def correctifyFault(fault_detail, originalMatrix, goal, criteria=None):
	# get the index of the comparison to correct
	matIndex = fault_detail[0]
	
	#get the row and column position of the index
	splitIndex = matIndex.split('_')
	i = int(splitIndex[0])-1
	j = int(splitIndex[1])-1
	#tempMatrix = np.array(originalMatrix)

	# Get new data to overcome the inconsistency
	newData = smd.simulateNewData(fault_detail[1], 10000)

	#write the new data into the database
	if (criteria):
		writeIntoDatabase(i+1, j+1, newData, goal, criteria)
	else:
		writeIntoDatabase(i+1, j+1, newData, goal)

	# change the faulty comparisons to new correct value
	#tempMatrix[i][j] = float(fault_detail[1])
	#tempMatrix[j][i] = 1/float(fault_detail[1]) #reciprocal

	# recalculate the eigenvectors using the newly gained data
	if (criteria):
		tempMatrix = am.getAlternativesCriteriaMatrix(goal, criteria)
	else:
		tempMatrix = cm.getCriteriaMatrix(goal)

	eigen_vector = ce.calculateEigenVector(tempMatrix)
	
	#return the eigen vector
	return eigen_vector