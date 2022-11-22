import math
import random


def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)

# This is a helping function designed to read the file and translate the text into the matrix
def fileReader(n, filename):
	if n>0: #first case
		Matrix = [[0 for x in range(n)] for y in range(n)] #creates empty matrix
		with open (filename, 'rt') as myfile: 			   #opens file
			for myline in myfile: 						   #reads line by line
														   #these two lines add the entries to the matrix
				Matrix[int(myline.split()[0])][int(myline.split()[1])] = int(myline.split()[2])
				Matrix[int(myline.split()[1])][int(myline.split()[0])] = int(myline.split()[2])
		return(Matrix)
	if n<0: 											   #second case
		nodes = [] 										   #empty list to add the coordinates
		with open (filename, 'rt') as myfile: 			   #opens file
			for myline in myfile: 						   #reads line by line
				nodes.append([int(myline.split()[0]), int(myline.split()[1])]) # adds the coordinates to the list
		Matrix = [[euclid(x, y) for x in nodes] for y in nodes] #creates the matrix calculating the distances
		return(Matrix)


class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):
    	self.dists = fileReader(n,filename)    #calls the helping function
    	self.n = len(self.dists) 			   # amount of nodes
    	self.perm = [i for i in range(self.n)] #the path currently chosen

    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
    	distance = sum([self.dists[self.perm[a]][self.perm[(a+1)%self.n]] for a in range(self.n)]) 
    	return distance

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
    	a = self.perm[i] 				      # new perm values
    	b = self.perm[(i+1)%self.n]
    	originalValue = self.tourValue()      # calculates the current tour value
    	self.perm[i] = b 					  #changes the actual perm using the new values
    	self.perm[(i+1)%self.n] = a
    	if self.tourValue() >= originalValue: #if the change isn't beneficiary
    		self.perm[i] = a 				  #changes perm back to how it was
    		self.perm[(i+1)%self.n] = b
    		return False
    	else:               				  #if the change is beneficiary
    		return True     				  #mantains perm as chancheg

    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.
    def tryReverse(self,i,j):
    	permMock = [n for n in self.perm] 								 # copie of the current perm
    	originalValue = self.tourValue() 								 # calculates the current tour value
    	self.perm = permMock[0:i]+permMock[i:j][::-1]+permMock[j:self.n] # changes the actual perm
    	if self.tourValue() >= originalValue: 							 #if the change isn't beneficiary 
    		self.perm = permMock 										 #changes perm back to how it was
    		return False
    	else:					 										 #if the change is beneficiary
    		return True 		 										 #mantains perm as chancheg


    def swapHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
    	permMock = [i for i in self.perm] # copie of the current perm
    	a = permMock[0]                   # initial node chosen as starting point
    	for i in range(1, self.n-1):      # iteration to add each subsequent node
    		permMock.remove(a)            # chosen nodes are removed from the elegible nodes
    		self.perm[i] = (min([(self.dists[a][n], n) for n in permMock]))[1] #selects most suitable node to add necht
    		a = self.perm[i]              #updates last node added
    

    #This is the algorithm I've chosen to do, it's similar to two opt.
    #But in this case, three nodes and thus two segments are swapped. 
    #It outperforms two_opt clealrly when data is bigger.

    #same as trySwap but swaping two segments
    def tripleReverse(self,k,i,j):
    	permMock = [n for n in self.perm]
    	originalValue = self.tourValue()
    	self.perm = permMock[:k]+permMock[k:i][::-1]+permMock[i:j][::-1]+permMock[j:] 
    	if self.tourValue() >= originalValue:
    		self.perm = permMock
    		return False
    	else:
    		return True

    #this is the part of the algorythm that iterates through the possible swappings
    def ThreeOptHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):      #loop that tries different swaps
            better = False
            count += 1
            for j in range(self.n-1):
                for i in range(j):
                	for k in range(i):
                		if self.tripleReverse(k,i,j): #calls the function triplereverse to check if the swap is beneficiary
                			better = True




g=Graph(-1,'cities50')
print(g.tourValue())
g.swapHeuristic(50)
g.TwoOptHeuristic(50)
g.Greedy()
g.ThreeOptHeuristic(50)
print(g.tourValue())