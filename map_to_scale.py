import numpy as np
from scipy import stats

def mappingToRequiredScale(value):
	np.set_printoptions(suppress=True)
	
	newValue = 0
	if value>=0:
		newValue = 1 + (2 * value)
	else:
		newValue = 1 + (2 * (0-value))
		newValue = 1/newValue

	if newValue < 0.1111:
		newValue = 0.1111
	elif newValue > 9:
		newValue = 9

	return round(newValue, 4)