import calculate_eigen as ce
import calculate_consistency as cc
import calculate_correct_value as ccv
import create_criteria_matrix as cm
import create_alternatives_matrix as am
import correctify_fault as cf

def processOneMatrix(goal, criteria=None):
	print "\n***************************************************************************************\n"
	print "Stage 1"
	print "______________________________________________________________________________________"
	if (criteria):
		originalMatrix = am.getAlternativesCriteriaMatrix(goal, criteria)
	else:
		originalMatrix = cm.getCriteriaMatrix(goal)

	#calculate eigen vector
	eigenVector = ce.calculateEigenVector(originalMatrix[0])
	
	#calculate consistency
	consistencyRatio = cc.consistency(originalMatrix[0], eigenVector)

	# print originalMatrix[0]
	# print consistencyRatio
	# print "********************************************************************"
	# if consistent, return eigenvector other find faulty comparison and correct
	if consistencyRatio[0] == True:
		print "Consistent, CR = " + str(consistencyRatio[1])
		return eigenVector
	else:
		print "\n"
		print "Stage 2"
		print "______________________________________________________________________________________"
		if consistencyRatio[0] == True:
			print "Consistent, CR = " + str(consistencyRatio[1])
		else:
			print "Inconsistent, CR = " + str(consistencyRatio[1])
		print "\n"
		# find faulty comparison and calculate value that is optimal
		fault_detail = ccv.calculateCorrectValue(originalMatrix, [], consistencyRatio[1])
		
		# return new eigenvector with consistent comparisons
		if (criteria):
			return cf.correctifyFault(fault_detail, originalMatrix, goal, criteria)
		else:
			return cf.correctifyFault(fault_detail, originalMatrix, goal)