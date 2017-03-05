import numpy as np

randomIndex = [0.00, 0.00, 0.525, 0.880, 1.109, 1.248, 1.342, 1.406, 1.450, 1.485, 1.514, 1.537, 1.555, 1.571, 1.584]

def consistency(originalMatrix, eigenVector):
	np.set_printoptions(suppress=True)

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

	consRatio = round(consRatio, 5)
	
	if (consRatio<0.1):
		return (True, consRatio, lambdaMax)
	else:
		return (False, consRatio, lambdaMax)