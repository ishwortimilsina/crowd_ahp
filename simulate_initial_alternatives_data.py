import numpy as np
import simulate_new_data as smd
import sqlite3

def writeIntoDatabase(column1, column2, data, goal, criteria=None):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	for single in data:
		# if (single < 0):
		# 	continue
		if (criteria):
			query = 'INSERT OR IGNORE INTO {tn} (goal_id, alternative_1_id, alternative_2_id, value, criteria_id) VALUES ({goal}, {column1}, {column2}, {single}, {criteria_id})'.\
							format(tn='alternatives_comparisons', column1=column1, column2=column2, single=single, criteria_id=criteria, goal=goal)
		else:
			query = 'INSERT OR IGNORE INTO {tn} (goal_id, criteria_1_id, criteria_2_id, value) VALUES ({goal}, {column1}, {column2}, {single})'.\
							format(tn='criteria_comparisons', column1=column1, column2=column2, single=single, goal=goal)
		c.execute(query)

	conn.commit()
	conn.close()

#myDict = {"1_2":3, "1_3":5, "1_4":1, "2_3":3, "2_4":0.3333, "3_4":0.2}
#myDict = {"1_2":1, "1_3":2, "1_4":0, "2_3":1, "2_4":-1, "3_4":-2}
#criteria = 1

#myDict = {"1_2":0.3333, "1_3":0.3333, "1_4":3, "2_3":3, "2_4":5, "3_4":5}
#myDict = {"1_2":-1, "1_3":-1, "1_4":1, "2_3":1, "2_4":2, "3_4":2}
#criteria = 2

#myDict = {"1_2":0.2, "1_3":0.3333, "1_4":5, "2_3":3, "2_4":7, "3_4":5}
#myDict = {"1_2":-2, "1_3":-1, "1_4":2, "2_3":1, "2_4":3, "3_4":2}
#criteria = 3

#myDict = {"1_2":0.3333, "1_3":3, "1_4":0.1428, "2_3":5, "2_4":0.2, "3_4":0.1111}
#myDict = {"1_2":-1, "1_3":1, "1_4":-3, "2_3":2, "2_4":-2, "3_4":-4}
#criteria = 4

for key, value in myDict.items() :
    splitKey = key.split('_')
    i = splitKey[0]
    j = splitKey[1]

    newData = smd.simulateNewData(value, 100)
    print (value, np.average(newData))
    
    writeIntoDatabase(i, j, newData, 1, criteria) # alternative_id 1, 2, value, goal_id, criteria_id

#SELECT AVG(value) FROM criteria_comparisons WHERE criteria_1_id=1 and criteria_2_id=2