import numpy as np

randomIndex = [0.00, 0.00, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.48, 1.56, 1.57, 1.59]

def consistency(originalMatrix, eigenVector):

	originalMat = np.array(originalMatrix)
	eigenVect = np.array(eigenVector)

	consMat = originalMat.dot(eigenVect)

	totalSum = 0
	m = len(eigenVect)

	for i in range(0, m):
		totalSum += consMat[i]/eigenVect[i]

	lambdaMax = totalSum/m

	consIndex = abs(lambdaMax - m)/(m-1)

	consRatio = consIndex/randomIndex[m-1]

	if (consRatio<0.1):
		return (True, consRatio, lambdaMax)
	else:
		return (False, consRatio, lambdaMax)