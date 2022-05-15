# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    #stack, visited : lists for DFS algorithm    
    stack = []
    visited = []
    #res : list for result 
    res = []
    stack.append((problem.getStartState(), []))
    #until stack is empty >> every node visited or no goal state
    while stack:
        pos, actionList = stack.pop()
        visited.append(pos)
        #if Goal State is found get the path into res and escape loop
        if problem.isGoalState(pos): 
            res = actionList
            break;
        #get adjacent nodes and add to stack with updated path
        for succProp in problem.getSuccessors(pos):
            if succProp[0] in visited : continue
            stack.append((succProp[0], actionList + [succProp[1]]))
            
    #if no goal state >> empty list, if found solution for problem
    return  res
    

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #queue for BFS 
    queue = []
    #queueCopy for preventing from adding same states in a queue
    queueCopy = []
    visited = []
    res = []
    queue.append((problem.getStartState(), []))
    queueCopy.append(problem.getStartState())
    while queue:
        #queue and queueCopy pushes and pops same entry
        pos, actionList = queue.pop(0)
        queueCopy.pop(0)
        visited.append(pos)
        if problem.isGoalState(pos): 
            res = actionList
            break;
        #get adjacent nodes
        #DO NOT push visited or nodes already in queue
        for succProp in problem.getSuccessors(pos):
            if succProp[0] in visited or succProp[0] in queueCopy: continue
            queue.append((succProp[0], actionList + [succProp[1]]))
            queueCopy.append(succProp[0])
            
        
    return  res

    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #we use priority queue to get minimum cost item at hand
    from util import PriorityQueue
    priQueue = PriorityQueue()
    visited=[]
    #we make dicitionary for keeping distance cost for states
    distance =dict()
    res = []
    PriorityQueue.push(priQueue, [problem.getStartState(), [], 0], 0)
    while priQueue:
        #priority is the distance of state > 
        #lowest priority comes out first == lowest cost state comes out first
        now, resList, dist = PriorityQueue.pop(priQueue)
        #if visited continue pop again 
        if now in visited : continue
        distance[now] = dist
        visited.append(now)
        #if found goal state >> break loop and return result
        if problem.isGoalState(now): 
            res = resList
            break
        succList = problem.getSuccessors(now)
        for item in succList:
            if item[0] not in visited:
                cost = distance[now]+item[2]
                #pushing in priority queue with priority as cost, so that minimum cost item is at hand
                PriorityQueue.push(priQueue, [item[0], resList+[item[1]], cost], cost)
    return res
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #it runs very similar to uniform cost search
    #but it takes priority as (distance + heuristic value)
    from util import PriorityQueue
    priQueue = PriorityQueue()
    visited=[]
    distance =dict()
    res = []
    PriorityQueue.push(priQueue, [problem.getStartState(), [], 0], 0)
    while priQueue:
        now, resList, dist = PriorityQueue.pop(priQueue)
        if now in visited : continue
        distance[now] = dist
        visited.append(now)
        if problem.isGoalState(now): 
            res = resList
            break
        succList = problem.getSuccessors(now)
        for item in succList:
            if item[0] not in visited:
                cost = distance[now]+item[2]
                #aVal for priority computation sum of distance and heuristic value
                aVal = distance[now]+item[2]+heuristic(item[0], problem)
                PriorityQueue.push(priQueue, [item[0], resList+[item[1]], cost], aVal)
    return res
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
