import numpy as np
import calculate_eigen as ce
import calculate_consistency as cc

def findFault(originalMatrix):
	faultDict = {}
	tempMatrix = np.array(originalMatrix)
	for i in range(0, len(originalMatrix)):
		for j in range(i+1, len(originalMatrix)):
			
			tempMatrix[i][j] = 0
			tempMatrix[j][i] = 0
			tempMatrix[i][i] = 2
			tempMatrix[j][j] = 2

			eigen_vector = ce.calculateEigenVector(tempMatrix)
			
			# find lamdamax of each modified matrix
			faultDict[str(i)+"_"+str(j)] = cc.consistency(tempMatrix, eigen_vector)[2]

			tempMatrix = np.array(originalMatrix)

	#find key with maximum value
	v=list(faultDict.values())
	k=list(faultDict.keys())

	print k[v.index(max(v))]