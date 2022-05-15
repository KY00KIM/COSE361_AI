# multiAgents.py
# --------------
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


from ghostAgents import GhostAgent
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #successorGameState graph with food(.) ghost(G) pacman(>)
        #newPos (x, y)
        #newFood graph with T, F
        #print(newGhostStates)
        #print(newFood.asList())
        
        behaveGood = 0
        foodList = newFood.asList()
        
        
        #for closest food, closer the better
        dis = 0
        for i in range(len(foodList)):
            if i==0: dis = manhattanDistance(foodList[0], newPos)
            else:  
                dis = min(dis, manhattanDistance(foodList[i], newPos))
            #if food can be eaten, better
            if newPos == foodList[i]: 
                behaveGood += 1
        behaveGood += -(dis)
        

        
        
       #Beahvior Score for each ghosts
        for ghostState in newGhostStates:
            invincibleTime = ghostState.scaredTimer
            gPos = ghostState.getPosition()
            dis = manhattanDistance(gPos, newPos)
            #if ghosts are weak and eatable in range, closer the better
            if dis < invincibleTime:
                behaveGood += 3
            else : 
                #if ghosts are far away the better
                if dis > 3:
                    behaveGood += 2
                else : behaveGood -= 2
        
        return successorGameState.getScore() + behaveGood
        

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        result = self.helperFunc( gameState, 0, 0)
        return result[0]
        util.raiseNotDefined()
    
    #helper function returning tuple (move, evaluatedValue) in recursive way
    def helperFunc(self, gameState, depth, agentIdx):
        if agentIdx == 0 : depth += 1
        
        #recursion return point 
        if gameState.isWin() or gameState.isLose() or depth == 1+self.depth:
            return ( Directions.STOP , self.evaluationFunction(gameState))
        
        #recursive search for successors
        agentNum = gameState.getNumAgents()
        legalMoves = gameState.getLegalActions(agentIdx)
        actionScore =[]
        for legalMove in legalMoves:
            tmp = self.helperFunc( gameState.generateSuccessor(agentIdx, legalMove), depth, (agentIdx+1)%agentNum)
            actionScore.append(tmp[1])
        
        #if 0 Pacman maxScore 
        #if not 0 ghosts minScore
        bestScore =   max(actionScore) if agentIdx==0 else min(actionScore)
        bestIndices = [index for index in range(len(actionScore)) if actionScore[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        
        return (legalMoves[chosenIndex], actionScore[chosenIndex])
    
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # using alpha beta pruning, 
        #helper function returns (action, evaluated value) based on minimax agent above
        result = self.helperFunc(gameState, 0, 0, -int(1e9), int(1e9))
        
        return result[0]
        
        util.raiseNotDefined()
        
    def helperFunc(self, gameState, depth, agentIdx,  alpha, beta):
        if agentIdx == 0 : depth+= 1
        #initialization for current state eval.
        currMove = Directions.STOP
        curr = -int(1e9) if not agentIdx else int(1e9)

        #recursion return point 
        if gameState.isWin() or gameState.isLose() or depth == 1+self.depth:
            return ( Directions.STOP , self.evaluationFunction(gameState))
        
        #recursive search for successors
        agentNum = gameState.getNumAgents()
        legalMoves = gameState.getLegalActions(agentIdx)
        for legalMove in legalMoves:
            childProp = self.helperFunc( gameState.generateSuccessor(agentIdx, legalMove), depth, (agentIdx+1)%agentNum, alpha, beta)
            #if pacman (Max Agent)
            if agentIdx == 0:
                if childProp[1] > curr:
                    curr = childProp[1]
                    currMove = legalMove
                alpha = max(alpha, curr)
                #pruning point
                if curr > beta : return (legalMove, curr)
            #if ghost (Min Agent)
            else:
                if childProp[1] < curr:
                    curr = childProp[1]
                    currMove = legalMove
                beta = min(curr, beta)
                #pruning point
                if curr < alpha : return (legalMove, curr)
        
        return (currMove, curr)
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
