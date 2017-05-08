import operator
import find_faulty_comparisons as ffc

def calculateCorrectValue(originalMatrix, archiveIndex=[], consVal=0):
	# print "Archived Indices ---- > " + str(archiveIndex)
	faultDict = ffc.findFault(originalMatrix)
	
	# create a sorted array based on value of all keys in the dictionary
	sorted_fault = sorted(faultDict.items(), key=operator.itemgetter(1), reverse=False)
	# print sorted_fault
	for key in sorted_fault:
		
		# to make example 3_4_left tp 3_4
		splitKey = key[0].split('_')
		matIndex = splitKey[0]+"_"+splitKey[1]

		# if the key is in the archiveIndex it means we do not want to process this anymore
		# ignore this, continue to next index
		if str(matIndex) in archiveIndex:
			continue

		# # if the required value doesn't fall in the confidence interval no need to get more input
		flag = True

		if key[1] >= consVal:
			flag = False

		# return the index of the value to be changed and the value to be changed to	
		# return (matIndex, eigen_vector[i]/eigen_vector[j], consVal[0], flag)
		return (matIndex, flag)
