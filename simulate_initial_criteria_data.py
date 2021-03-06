import numpy as np
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

#myDict = {"1_2":0.3333, "1_3":5, "1_4":7, "2_3":7, "2_4":9, "3_4":3}
#myDict = {"1_2":-1, "1_3":2, "1_4":3, "2_3":3, "2_4":4, "3_4":1}

#myDict = {"1_2":0.3333, "1_3":5, "1_4":7, "1_5":7, "2_3":5, "2_4":9, "2_5":7, "3_4":5, "3_5":5, "4_5":0.3333}
myDict = {"1_2":-1, "1_3":2, "1_4":3, "1_5":3, "2_3":2, "2_4":4, "2_5":3, "3_4":2, "3_5":2, "4_5":-1}

for key, value in myDict.items() :
    splitKey = key.split('_')
    i = splitKey[0]
    j = splitKey[1]

    newData = smd.simulateNewData(value, 100, 0.7)
    
    print (value, np.average(newData))
    
    writeIntoDatabase(i, j, newData, 2)