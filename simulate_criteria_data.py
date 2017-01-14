import numpy as np
import matplotlib.pyplot as plt

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin()
	return idx

def simulateNewData(requiredValue, size):
	inputSet = np.array([0.1111, 0.1428, 0.2, 0.3333, 1, 3, 5, 7, 9])

	ourIndex = find_nearest(inputSet, requiredValue)

	if int(ourIndex) == 8:
		upperLimit = inputSet[int(ourIndex)]
	else:	
		upperLimit = inputSet[int(ourIndex)+1]

	if int(ourIndex) == 0.1111:
		lowerLimit = inputSet[int(ourIndex)]
	else:
		lowerLimit = inputSet[int(ourIndex)-1]

	if (requiredValue > inputSet[8]):
		requiredValue = inputSet[8]

	k = np.random.triangular(lowerLimit, requiredValue, upperLimit, size)
	#k = np.random.normal(loc=1, scale=1.0, size=100)

	return k

k = simulateNewData(9.03, 1000)
print np.mean(k)
plt.hist(k, bins=200)
plt.show()