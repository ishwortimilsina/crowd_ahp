import numpy as np
import matplotlib.pyplot as plt

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def simulateNewData(requiredValue, size):
	# inputSet = np.array([0.1111, 0.1428, 0.2, 0.3333, 1, 3, 5, 7, 9])

	# ourIndex = find_nearest(inputSet, requiredValue)
	
	# if (requiredValue > inputSet[8]):
	# 	requiredValue = inputSet[8]
	# elif (requiredValue < inputSet[0]):
	# 	requiredValue = inputSet[0]

	# lowerLimit = inputSet[0]
	# upperLimit = inputSet[8]
	
	#k = np.random.triangular(lowerLimit, requiredValue, upperLimit, size)
	#k = np.random.uniform(lowerLimit,upperLimit,size)
	k = np.random.normal(loc=requiredValue, scale=0.7, size=size)

	
	return k

yo = [-1, 2, 3, 3, 4, 1]

for i in yo:
	simulateNewData(-3, 100)
