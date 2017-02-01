import numpy as np
import simulate_new_data as smd
import sqlite3

def writeIntoDatabase(column1, column2, data, goal, criteria=None):
	sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

	# Connecting to the database file
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	for single in data:
		if (single < 0):
			continue
		if (criteria):
			query = 'INSERT OR IGNORE INTO {tn} (goal_id, alternative_1_id, alternative_2_id, value, criteria_id) VALUES ({goal}, {column1}, {column2}, {single}, {criteria_id})'.\
							format(tn='alternatives_comparisons', column1=column1, column2=column2, single=single, criteria_id=criteria, goal=goal)
		else:
			query = 'INSERT OR IGNORE INTO {tn} (goal_id, criteria_1_id, criteria_2_id, value) VALUES ({goal}, {column1}, {column2}, {single})'.\
							format(tn='criteria_comparisons', column1=column1, column2=column2, single=single, goal=goal)
		c.execute(query)

	conn.commit()
	conn.close()

myDict = {"1_2":0.3333, "1_3":5, "1_4":7, "2_3":7, "2_4":9, "3_4":3}

for key, value in myDict.items() :
    splitKey = key.split('_')
    i = splitKey[0]
    j = splitKey[1]

    newData = smd.simulateNewData(value, 100)
    print (value, np.average(newData))
    
    writeIntoDatabase(i, j, newData, 1)

#SELECT AVG(value) FROM criteria_comparisons WHERE criteria_1_id=1 and criteria_2_id=2