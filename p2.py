# CS480
# Assignment: Project 2
# Authors: Justin Bernard

import sys
import timeit
import copy
from collections import deque
testingFunctions = True if sys.argv[1] == '1' else False
testingValues = True if sys.argv[1] == '2' else False
testingQueueContents = True if sys.argv[1] == '3' else False
    
def main():
    print ("Enter permutation to be sorted:")
    values = [int(x) for x in input().split()]
    numElements = len(values)
    # calculate number of substrings: (n(n+1)/2) - n
    numSubstrings = (numElements * (numElements + 1) / 2) - numElements
    if (testingValues):
        print ("Values Array: ", values)
        print ("Number of elements: ", numElements)
        print ("Number of substrings: ", int(numSubstrings))

    sortedValues = values.copy()
    if (testingValues):
        print ("sortedValues (before sort): ", sortedValues)
    sortedValues.sort()
    if (testingValues):
        print ("sortedValues (after sort): ", sortedValues)
    numBadPositions (values, sortedValues)
    startTime = timeit.default_timer()
    nodesVisited, qSize = (bfs (values, sortedValues))
    endTime = timeit.default_timer()
    time = endTime - startTime
    printStats (nodesVisited, qSize, time)


def bfs (currentList, goalList):
    q = deque()
    q.append(currentList)
    nodesVisited = 0
    parentID = -1
    parents = {}
    kids = []

    while (len(q) != 0):
        if (testingQueueContents):
            print ("Current Queue: ", q)
        child = q.popleft()
        if (child == goalList):
            print (">> INPUT ALREADY SORTED <<")
            return (nodesVisited, len(q))
        parents[parentID] = child
        print ("State: ", child)
        childAdded = 0
        for n in children(child, goalList):
            if (n == goalList): # begin process of printing the solution path
                print (">> SOLUTION FOUND <<")
                print ("State: ", n)
                print ("______PATH_______ ")
                print (n)
                parentKey = -100 # set parentKey
                parent = child # set parent to child (which is the first parent to return at this point)
                print (parents[parentID]) # print the first parent
                while (parentKey != -1):
                    for x in range(len(kids)):
                        if (parent == kids[x]):
                            print (parents[kids[x-1]]) # print the parent of the parent using the key
                            parent = parents[kids[x-1]] # set parent to the parent we found (on next iteration, we'll look for this parent in kids to find the next parent key)
                            parentKey = kids[x-1] # set parentKey to the key we found (for the while loop)
                            break # if we've found the parent, break out of for loop
                    # if parentKey = -100 at this point, then it means we've looped through the kids array and
                    # didn't find the parent in there.  The only way this happens is if the goal is reachable
                    # in one move (i.e. something like 4 3 2 1 is reversible in one move).  As we expand the
                    # children of 4 3 2 1, we check them immediately to see if they're the goal node before
                    # even adding them to the queue (or kids), so, when we check for a parent (which is the
                    # root in this case) it won't be present in the kids array (since the root is not added
                    # here - only the children of the root are), and we'll loop forever.
                    if (parentKey == -100):
                        break
                return (nodesVisited, len(q))
            if (notInQueue(q, n)):
                nodesVisited += 1
                q.append(n)
                kids += [parentID]
                kids += [n]
                childAdded += 1
        if (childAdded != 0): # if child was added
            parentID += 1
            childAdded = 0
        else:
            del parents[parentID]
        if (testingValues):
            print ("PARENTS: ", parents)
            print ("KIDS: ", kids)
        if (testingFunctions):
            print (" >> bfs - FINISHED APPENDING")

def children (currentChild, goal):
    cChild = currentChild.copy()
    setOfChildren = [] # will store the permutations we create by flipping values around
    startIdx = 0 # used to set and track the starting index to begin evaluating during each loop
    currentIdx = 0 # used to track the current index we're looking at
    spreadCount = 0 # used while evaluating whether a target qualifies to be reversed or not
                    # (i.e. increment if it does.  Once it's = to spreadLimit, we're ready for reversal)
    spreadLimit = 2 # the current size of a subarray reversal we're looking to do
                    # (this value also continues to grow, depending on the total array size)
    if (testingFunctions):
        print (" >> children - AT TOP")
    # This outer WHILE loop governs the increasing size of the subarrays we're looking to reverse
    # (i.e. we start by looking at reversing all subarrays of size 2, adding those permutations to
    # setOfChildren, then, we look at subarrays of size 3, 4, etc until we reach the array size itself)
    # We can't evaluate a subarray that's bigger than the array itself, this loop prevents that.
    # Being at the top of this loop means that we're starting over to evaluate permutations at a new subarray size
    while (spreadLimit < len(cChild)+1):
        if (testingFunctions):
            print (" >> children - WHILE 1 TOP")
        # This next WHILE loop governs the index we begin at as we start evaluating a given subarray size
        # (i.e. when looking for subarrays of size 2 in a list of size 4, the subarrays of size 2 begin
        # at indices 0, 1, and 2 - index 3 is the last element in the list, so if we tried to look for a
        # a subarray of size 2 there, we'd end up going out of range.  This loop prevents that.
        # Being at the top of this loop means that we're evaluating a new permutation for the current subarray size
        while (startIdx < len(cChild)-1):
            if (testingFunctions):
                print (" >> children - WHILE 2 TOP")
            currentIdx = startIdx  # since we're starting a new permutation, currentIdx must = the startIdx
            # This FOR loop makes sure we evaluate only the # of values we need for the subarray size
            # we're currently looking for.  For example, with a subarray size of 2, it will only iterate
            # twice, starting from the startIdx value.  As the subarray size increases, so will the
            # number of iterations in this loop.
            for x in range(spreadLimit):
                if (testingFunctions):
                    print (" >> children - FOR TOP")
                # This IF statement is checking to make sure that the current value we're looking at is NOT
                # in the correct position (as compared to what's in the goal array).  If it's in the correct
                # position, then we don't want to do any reversals that would move it to an incorrect position,
                # so, we'll ignore it.  If it isn't in the correct position however, then it's something that
                # can be included in a reversal.
                if (1):
                #if (cChild[currentIdx] != goal[currentIdx]):
                    if (testingFunctions):
                        print (" >> children - IF value = goalVal TOP")
                    # if we've found a valid value to reverse, increase spreadCount and currentIdx
                    spreadCount = spreadCount + 1
                    currentIdx = currentIdx + 1
                    # once spreadCount equals spreadLimit, we will do the reversal and add to setOfChildren
                    if (spreadCount == spreadLimit):
                        if (testingFunctions):
                            print (" >> children - IF spread = spreadLim TOP")
                        newChild = reverse(cChild, startIdx, spreadLimit)
                        setOfChildren.append(newChild)
                        startIdx = startIdx + 1 # we're done with this perm, so increment startIdx for the next one
                        spreadCount = 0 # reset spreadCount to 0 for the next permutation
            # when evaluating the last possible subarray within an array, currentIdx can go out of range and won't
            # be caught by the 2nd WHILE loop condition, so if currentIdx == the array size, break out
            if (currentIdx == len(cChild)):
                if (testingFunctions):
                    print (" >> children - IF currentIdx = len(cChild) TOP / WHILE 2 BOT")
                break
        # at this point, we're done evaluating all permutations of a given subarray size, so we incrememnt spreadLimit
        # and reset the startIdx.  If spreadLimit is > than the array size at this point, then we're completely done
        spreadLimit = spreadLimit + 1
        startIdx = 0
        if (testingFunctions):
            print (" >> children - WHILE 1 BOT, increasing spread limit")
    if (testingFunctions):
        print (" >> children - RETURNING setOfChildren")
    # at this point, we've evaluating all permutations at all subarray sizes, and return the set of permutations found
    return setOfChildren

# reverse takes in the current array, the starting index of the subarray to be reversed, and the subarray size
def reverse (currentList, start, size):
    if (testingFunctions):
        print (" >> reverse - TOP")
    childList = currentList.copy()
    startIdx = start
    result = [] # will store the new array with the reversed portion
    firstHalf = childList[0:startIdx] # this simply stores the beginning values that are not being reversed
    reversedSubarray = list(reversed(childList[startIdx:startIdx+size])) # reversing the segment of interest
    secondHalf = childList[startIdx+size:] # and this stores the values after the segment to be reversed
    if (testingValues):
        print ("First half of list: ", firstHalf)
        print ("Reversed subarray of list: ", reversedSubarray)
        print ("Second half of list: ", secondHalf)

    # take the firstHalf values, add the reversed subarray to it, and then add the secondHalf values
    result = firstHalf + reversedSubarray + secondHalf

    if (testingValues):
        print ("Result of reversed subarray: ", result)
    # return the new permutation, which will be added to a set of permutations upon returning
    if (testingFunctions):
        print (" >> reverse RETURNING")
    return result

def notInQueue(currentQueue, child):
    for x in currentQueue:
        if (child == x):
            return False
    return True

# numBadPositions does a comparison between the passed in array with the goal array to calculate the number
# of values that are not in the correct positions (may or may not be useful in determining how to proceed
# in a given algorithm - i.e. only expanding nodes from permutations with the least values in bad positions)
# This can be flawed however, if we had a permutation such as [4, 3, 2, 1], we have all 4 values in bad
# positions, and, using this technique, we'd obviously choose not to expand it and miss the fact that it
# really only requires 1 reversal to put all 4 in the correct positions - doh!
def numBadPositions (currentList, goalList):
    if (testingFunctions):
        print (" >> numBadPositions TOP")
    numWrong = 0
    for x in range(len(currentList)):
        if (testingValues):
            print ("Comparing ", currentList[x], " to ", goalList[x])
        if (currentList[x] != goalList[x]):
            numWrong = numWrong + 1
    if (testingValues):
        print ("Number of elements in wrong position: ", numWrong)

    if (testingFunctions):
        print (" >> numBadPositions RETURNING")
    return numWrong

def printStats (numVisited, qSize, runTime):
    print ("__Final Stats__")
    print ("Nodes visited: ", numVisited)
    print ("Queue size: ", qSize)
    print ("Runtime: ", runTime, " seconds")

main()
