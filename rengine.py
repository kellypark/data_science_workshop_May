import math

RATINGS_FILE = 'data/ratings.txt'
MOVIES_FILE = 'data/movies.txt'
USERS_FILE = 'data/users.txt'
TRAINING_FILE = 'trainting.txt'
TESTING_FILE = 'testing.txt'
SIMILARITY_FILE = 'similarity.txt'
DELIMITER = '::'
DEFAULT_VALUE = -2

def divideDataSet():	
	f = open(RATINGS_FILE, 'r')
	training = []
	testing = []
	testingfile = open(TESTING_FILE, 'w+')
	trainingfile = open(TRAINING_FILE, 'w+')
	count = 0
	for line in f:
		if count%3==0:
			testing.append(line)
			testingfile.write(line)
		else :
			training.append(line)
			trainingfile.write(line)
		count+=1

	testingfile.close()
	trainingfile.close()

def getMovieCount():
	movieFile = open(MOVIES_FILE, 'r')
	movieCount = 0;
	for line in movieFile:
		lineSplit = line.split(DELIMITER)
		movieId = int(lineSplit[0])
		if movieId > movieCount:
			movieCount = movieId
	return movieCount


def getUserCount():
	userFile = open(USERS_FILE, 'r')
	userCount = 0;
	for line in userFile:
		lineSplit = line.split(DELIMITER)
		userId = int(lineSplit[0])
		if userId > userCount:
			userCount = userId
	return userCount

def createUserMovieArray(movieCount,userCount):
	userMovieArray = [[0 for x in range(movieCount)] for x in range(userCount)] 
	trainingfile = open(TRAINING_FILE, 'r+')
	for line in trainingfile:
		lineSplit = line.split(DELIMITER)
		userMovieArray[int(lineSplit[0])][int(lineSplit[1])] = int(lineSplit[2])
	return userMovieArray
	
def createSimilarityMatix(userMovieArray,movieCount,userCount):
	similarityMatrix = [[-2 for x in range(userCount)] for x in range(userCount)]
	similarityFile = open(SIMILARITY_FILE,'w+')

	for user1 in range(1, userCount):
		for user2 in range(user1+1, userCount):
			dotProduct = 0
			user1NormSum = 0
			user2NormSum = 0
			for movieId in range(1, movieCount):
				movieRating1 = userMovieArray[user1][movieId]
				movieRating2 = userMovieArray[user2][movieId]
				if movieRating1 != 0 and movieRating2 !=0:
					dotProduct += movieRating1 * movieRating2
					user1NormSum += math.pow(movieRating1,2)
					user2NormSum += math.pow(movieRating2,2)
			if user1NormSum !=0 and user2NormSum!=0 :
				user1Norm = math.sqrt(user1NormSum)
				user2Norm = math.sqrt(user2NormSum)
				cosSimilarity = dotProduct / (user1Norm * user2Norm)
				similarityMatrix[user1][user2] = cosSimilarity
		print str(user1)
		similarityFile.write("".join(str(similarityMatrix[user1])))
	similarityFile.close()
	return similarityMatrix

def getSimilarityMatrix(userCount):
	similarityMatrix = [[-2 for x in range(userCount)] for x in range(userCount)]
	similarity1File = open(SIMILARITY_FILE, 'r').read()
	simimarity = simimarityFile.split('][')
	count = 1
	for line in simimarity:
		similarityMatrix[count] = line.replace('[','').replace(']','').split(',')
		count+=1
	return similarityMatrix

def copySymmetricMatrix(similarityMatrix):
	for user1 in range(1, (len(similarityMatrix)/2)+1):
		for user2 in range(user1+1, len(similarityMatrix)):
			if(similarityMatrix[user2][user1]==-2):
				similarityMatrix[user2][user1] = similarityMatrix[user1][user2]
	return similarityMatrix

def getAllIndexOf(elem,list):
	return [i for i, x in enumerate(list) if x == elem]
	
def getKClosestNeighbours(k, list):
	filteredList = filter(lambda a: a != -2, reversed(sorted(list)))
	kSimilimarityValues = filteredList[:k]
	result = []
	for v in kSimilimarityValues:
		vIndex = list.index(v)
		if vIndex in result:
			allIndex = getAllIndexOf(v,list);
			for index in allIndex:
				if(index not in result):
					result.append(index)
					break
		else:
			result.append(vIndex)

	return result

def getEstimatedRating(movieId, neighbours, userMovieArray):
	sum = 0
	count =0 
	for n in neighbours:
		if float(userMovieArray[n][movieId]) != 0:
			count +=1
		sum += float(userMovieArray[n][movieId])
	if count==0:
		return 0
	return sum / float(count)


def getMeasureForK(k,similarityMatrix,userMovieArray):
	testingfile = open(TESTING_FILE, 'r')
	differnceMatrix = []
	kNeighbours = [ [] for x in range(len(similarityMatrix)) ]
	for i in range(1, len(similarityMatrix)):
		kNeighbours[i] = getKClosestNeighbours(k, similarityMatrix[i])

	for line in testingfile:
		lineSplit = line.split(DELIMITER)
		userId= int(lineSplit[0])
		movieId = int(lineSplit[1])
		actualRating = int(lineSplit[2])
		estimatedRating = getEstimatedRating(movieId,kNeighbours[userId], userMovieArray)
		if(estimatedRating!=0):
			diff = abs(estimatedRating - actualRating)
			differnceMatrix.append(diff)
	measure = sum(differnceMatrix) / float(len(differnceMatrix))
	return measure

def findOptimalK(similarityMatrix, userMovieArray):
	for k in range(3,100): 
		index = k*10
		print 'k is '+str(index)+' and measure is '+str(getMeasureForK(index, similarityMatrix,userMovieArray))


def main():
	divideDataSet()

	movieCount = getMovieCount()+1
	userCount = getUserCount()+1
	userMovieArray = createUserMovieArray(movieCount,userCount)

	# similarityMatrix = createSimilarityMatix(userMovieArray,movieCount,userCount)
	similarityMatrix = getSimilarityMatrix(userCount)
	
	similarityMatrix = copySymmetricMatrix(similarityMatrix)
	

	print '*********** optimalK is '+ str(findOptimalK(similarityMatrix, userMovieArray))

main()