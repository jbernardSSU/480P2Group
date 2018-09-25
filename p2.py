# CS480
# Assignment: Project 2
# Authors: Justin Bernard

import sys
import timeit
import copy
from collections import deque
# program can be invoked with 1, 2, or 3 to activate certain
# statements for testing (i.e. "python3 p2.py 1")
if (len(sys.argv) > 1):
    testingFunctions = True if sys.argv[1] == '1' else False
    testingValues = True if sys.argv[1] == '2' else False
    testingQueueContents = True if sys.argv[1] == '3' else False
else:
    testingFunctions = False
    testingValues = False
    testingQueueContents = False
    
def main():
    print ("Enter permutation to be sorted:")
    values = [int(x) for x in input().split()]
    sortedValues = values.copy()
    if (testingValues):
        print ("Values Array: ", values)
        print ("sortedValues (before sort): ", sortedValues)
    sortedValues.sort()
    if (testingValues):
        print ("sortedValues (after sort): ", sortedValues)

    startTime = timeit.default_timer() # start timer
    # call bfs, which will return the number of nodesVisited and queue size
    nodesVisited, qSize = (bfs (values, sortedValues))
    endTime = timeit.default_timer() # end timer
    time = endTime - startTime # calculate total time
    # print final stats
    printStats (nodesVisited, qSize, time)

def bfs (currentList, goalList):
    q = deque() # establish a queue
    q.append(currentList) # add our root node to it
    #nodesVisited will increment every time we pop a node from the queue
    nodesVisited = 0
    
    # parentID, parents and kids all work together to track which nodes are parents
    # to each successive set of children we expand, in order to print the solution path.
    # Each time we pop a node from the queue to expand, we say that that node is now
    # a parent, and add it to the parents dictionary with a key value of parentID.
    # At the same time, each child that is spawned from this parent will be added to
    # the kids array, along with the value of parentID in the indice just before it.
    # When we've found our solution node, parentID will have been incremented to some
    # given value, so we use that as our key within parents to find that first parent.
    # Once found, we take that node value and do a search through the kids array because
    # it will be present there too from when it was first expanded as a child.  Once found,
    # we'll look at the index location just before it, because that's where its parentID
    # value will be, then, we use that value as a key to find its parent within parents,
    # and the process repeats until we hit a -1 as a key, which means we've hit the root node.
    parentID = -1
    parents = {}
    kids = []

    # begin process of building the queue with permutations
    while (len(q) != 0):
        if (testingQueueContents):
            print ("Current Queue: ", q)
        child = q.popleft()
        # check right away if the root is the goal
        if (child == goalList):
            print (">> INPUT ALREADY SORTED <<")
            return (nodesVisited, len(q))
        parents[parentID] = child # add to parents dict with the parentID
        print ("State being expanded: ", child)
        # childAdded is used to confirm whether a parent had any valid children to be added to the queue.
        # If it does, childAdded is incremented and allows parentID to be incremented farther below.
        # Below, there are checks to make sure no duplicates enter the queue, and because of this, there
        # are cases where a given parent node we're expanding has no valid children to be added.  If that's
        # the case, then childAdded will remain 0, and parentID won't be incremented.  Basically, what happens
        # is that a parent with no valid children, without this check, will be added to parents dict and
        # cause a gap in the parentIDs within kids array.  This prevents that.
        childAdded = 0
        # So, we have our parent and begin expanding its children.  The children function will take the parent
        # node and find all of its children through reversals.
        for n in children(child):
            # Here, we check each child to see if they're the goal node before they even enter the queue
            if (n == goalList):
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
                # Once we're done printing the path to the solution node, return to main and print the final stats
                return (nodesVisited, len(q))
            # Here is our check to see if a given child is already in the queue.  If it's not, then add it to the
            # queue, as well as kids array with the relevant parentID.  Also increment childAdded so we know it's
            # okay to incremement parentID as well.
            if (notInQueue(q, n)):
                nodesVisited += 1
                q.append(n)
                kids += [parentID]
                kids += [n]
                childAdded += 1
        if (childAdded != 0): # if child was added
            parentID += 1
            childAdded = 0
        else: # If a parent had no valid children to be added, then delete it from the parents dict
            del parents[parentID]
        if (testingValues):
            print ("PARENTS: ", parents)
            print ("KIDS: ", kids)
        if (testingFunctions):
            print (" >> bfs - FINISHED APPENDING")

def children (currentChild):
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

def printStats (numVisited, qSize, runTime):
    print ("__Final Stats__")
    print ("Nodes visited: ", numVisited)
    print ("Queue size: ", qSize)
    print ("Runtime: ", runTime, " seconds")

main()
