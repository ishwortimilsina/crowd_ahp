import operator
import numpy as np
import processOneMatrix as pom
import sqlite3

goal = "Select best Movie - small data - small variance"


#Get all the criteria for the given goal
#######################################################################
sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
query = 'SELECT g.ROWID, cr.criteria_id FROM {tn1} g, {tn2} cr WHERE g.ROWID=cr.goal_id and g.goal="{goal}"'.\
				format(tn1='goals', tn2='criteria', goal=goal)
c.execute(query)
goal_id = 0
allCriteria = []
for row in c.fetchall():
	goal_id = row[0]
	allCriteria.append(row[1])

conn.close()
########################################################################


criteriaWeight = pom.processOneMatrix(goal_id)

allCriteria = np.sort(allCriteria)

for i in allCriteria:
	semiFinalMatrix = np.array(pom.processOneMatrix(goal_id, i))
	break

# combining alternatives weight vectors for each criteria to form a matrix
for i in allCriteria:
	if (i == allCriteria[0]):
		continue
	semiFinalMatrix = np.vstack([semiFinalMatrix, pom.processOneMatrix(goal_id, i)])

finalMatrix = semiFinalMatrix.T # transposing the matrix

finalPreference = finalMatrix.dot(criteriaWeight) # multiply the transpose with the criteria priority vector

print "\n***************************************************************************************\n"
print "Final Ranking\n"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('SELECT a.alternative FROM {tn1} a, {tn2} g WHERE g.ROWID=a.goal_id and g.goal="{goal}"'.\
				format(tn1='alternatives', tn2='goals', goal=goal))
alternativeName = {}
i = 0
for row in c.fetchall():
	alternativeName[row[0]] = str(finalPreference[i])
	i += 1

conn.close()

sorted_rank = sorted(alternativeName.items(), key=operator.itemgetter(1), reverse=True)

for key in sorted_rank:
	print key[0]  + " \t\t\t---> " + key[1]