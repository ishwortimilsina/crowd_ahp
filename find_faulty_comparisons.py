import operator
import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc
import map_to_scale as mts

# def findFault(originalMatrix):
# 	faultDict = {}
# 	tempMatrix = np.array(originalMatrix)
# 	for i in range(0, len(originalMatrix)):
# 		for j in range(i+1, len(originalMatrix)):
			
# 			# replace each element and its recriprocal element by zero 
# 			# and corresponding diagonal elements by two
# 			tempMatrix[i][j] = 0
# 			tempMatrix[j][i] = 0
# 			tempMatrix[i][i] = 2
# 			tempMatrix[j][j] = 2

# 			# find the eigen vector
# 			eigen_vector = ce.calculateEigenVector(tempMatrix)
			
# 			# find lamdamax of each modified matrix and store it in the dict with modified index
# 			faultDict[str(i+1)+"_"+str(j+1)] = cc.consistency(tempMatrix, eigen_vector)[2]

# 			tempMatrix = np.array(originalMatrix)

# 	return faultDict

def findFault(originalMatrix):
	countDict = {1: "first", 2:"second", 3:"third", 4:"fourth", 5:"fifth", 6:"sixth"}

	tempMatrix = np.array(originalMatrix[0])
	
	cells = originalMatrix[1]

	crDict = {}

	for key in cells:
		# get the index of each value
		matIndex = key

		# split index to get the row and column position of the value to be changed
		splitIndex = matIndex.split('_')
		i = int(splitIndex[0])-1
		j = int(splitIndex[1])-1

		checkInterval = (cells[key][1][1] - cells[key][1][0])/4
		x = cells[key][1][0]
		
		count = 1
		while (True):

			# replace each element and its recriprocal element by 
			# left_confidence of the current mean distribution of cell
			tempMatrix[i][j] = mts.mappingToRequiredScale(x)
			tempMatrix[j][i] = 1/tempMatrix[i][j]

			# find the eigen vector
			eigen_vector = ce.calculateEigenVector(tempMatrix)
			
			# find lamdamax of each modified matrix and store it in the dict with modified index
			crDict[str(i+1)+"_"+str(j+1)+"_"+countDict[count]] = cc.consistency(tempMatrix, eigen_vector)[1]

			tempMatrix = np.array(originalMatrix[0])

			# calculate CR for each five values in the confidence interval
			if checkInterval>0:
				x = x + checkInterval
			else:
				x = x - checkInterval

			if x > cells[key][1][1]:
				x = cells[key][1][1]

			if count == 5:
				break
			
			count += 1

	return crDict