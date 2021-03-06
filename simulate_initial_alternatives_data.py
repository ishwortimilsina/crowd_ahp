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

myDict = {"1_2":-2, "1_3":-3, "1_4":0, "1_5":-1, "1_6":4, "1_7":0, "1_8":1, "1_9":-1, "1_10":-2,
"2_3":-1, "2_4":1, "2_5":0, "2_6":4, "2_7":2, "2_8":3, "2_9":0, "2_10":0,
"3_4":2, "3_5":1, "3_6":4, "3_7":2, "3_8":3, "3_9":1, "3_10":1,
"4_5":-2,  "4_6":4, "4_7":1, "4_8":2, "4_9":-1, "4_10":-1,
"5_6":4, "5_7":2, "5_8":2, "5_9":0, "5_10":0,
"6_7":-2, "6_8":-1, "6_9":-3, "6_10":-3,
"7_8":1, "7_9":-2, "7_10":-2,
"8_9":0.5, "8_10":-3,
"9_10":0}


for key, value in myDict.items() :
    splitKey = key.split('_')
    i = splitKey[0]
    j = splitKey[1]

    newData = smd.simulateNewData(value, 100, 1.5)
    print (value, np.average(newData))
    
    writeIntoDatabase(i, j, newData, 4, 5) # alternative_id 1, 2, value, goal_id, criteria_id