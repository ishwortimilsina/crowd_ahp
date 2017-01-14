import numpy as np
import processOneMatrix as pom
import sqlite3

goal = "Select the best movie"


#Get all the criteria for the given goal
#######################################################################
sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('SELECT cr.criteria_id FROM {tn1} g, {tn2} cr WHERE g.ROWID=cr.goal_id and g.goal="{goal}"'.\
				format(tn1='goals', tn2='criteria', goal=goal))
allCriteria = []
for row in c.fetchall():
	allCriteria.append(row[0])

conn.close()

########################################################################


criteriaWeight = pom.processOneMatrix(goal)

allCriteria = np.sort(allCriteria)

for i in allCriteria:
	semiFinalMatrix = np.array(pom.processOneMatrix(goal, i))
	break

# combining alternatives weight vectors for each criteria to form a matrix
for i in allCriteria:
	if (i == allCriteria[0]):
		continue
	semiFinalMatrix = np.vstack([semiFinalMatrix, pom.processOneMatrix(goal, i)])

finalMatrix = semiFinalMatrix.T # transposing the matrix

finalPreference = finalMatrix.dot(criteriaWeight) # multiply the transpose with the criteria priority vector

# This is the final ranking
print finalPreference