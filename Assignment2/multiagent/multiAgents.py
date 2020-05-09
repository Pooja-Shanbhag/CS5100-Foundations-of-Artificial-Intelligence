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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newCapsule = successorGameState.getCapsules()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currentScore = successorGameState.getScore()

        "*** YOUR CODE HERE ***"
        list_of_ghost_distances = []
        for ghostState in newGhostStates:
            list_of_ghost_distances.append(util.manhattanDistance(newPos, ghostState.getPosition()))
        if len(list_of_ghost_distances) == 0:
            minGhostDistance = 1
        elif len(list_of_ghost_distances) == 1:
            minGhostDistance = list_of_ghost_distances[0]
        else:
            minGhostDistance = min(list_of_ghost_distances)

        list_of_food_distances = []
        if len(newFood.asList()) == currentGameState.getNumFood():
            minFoodDistance = 999999
            for food_coordinate in newFood.asList():
                list_of_food_distances.append(util.manhattanDistance(newPos, food_coordinate))
            minFoodDistance = min(list_of_food_distances)
        else:
            minFoodDistance = 0

        list_of_capsule_distances = []
        for capsule in newCapsule:
            list_of_capsule_distances.append(util.manhattanDistance(newPos, capsule))
        if len(list_of_capsule_distances) == 0:
            minCapsuleDistance = 1
        elif len(list_of_capsule_distances) == 1:
            minCapsuleDistance = list_of_capsule_distances[0]
        else:
            minCapsuleDistance = min(list_of_capsule_distances)

        gamma = -0.04
        if minCapsuleDistance >= 5:
            if minGhostDistance > minFoodDistance:
                evaluationFunc = currentScore + gamma * (
                        minFoodDistance + minCapsuleDistance * gamma + minGhostDistance * gamma * gamma)
            else:
                if minGhostDistance == 1:
                    evaluationFunc = -4
                else:
                    evaluationFunc = currentScore + gamma * (
                            minFoodDistance + gamma * minGhostDistance + gamma * gamma *
                            minCapsuleDistance)

        elif newScaredTimes == 0:
            evaluationFunc = currentScore + gamma * (
                    minFoodDistance + gamma * minCapsuleDistance)
        else:
            evaluationFunc = currentScore + gamma * (minFoodDistance + gamma * minCapsuleDistance + gamma * gamma *
                                                     minGhostDistance)
        return evaluationFunc


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"
        val, action = self.minMax(self.depth, gameState, "", True, 0)
        return action

        util.raiseNotDefined()

    def minMax(self, depth, gameState, action, isMaxPlayer, agentIndex):
        maxAction = ""
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), action
        if isMaxPlayer:
            value = -9999999
            for action in gameState.getLegalActions(agentIndex):
                successorState = gameState.generateSuccessor(agentIndex, action)
                if not agentIndex == gameState.getNumAgents() - 1:
                    (currentEval, _) = self.minMax(depth, successorState, maxAction, False, agentIndex + 1)
                if currentEval > value:
                    value = currentEval
                    maxAction = action
            return value, maxAction
        else:
            value = 9999999
            for action in gameState.getLegalActions(agentIndex):
                successorState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    (currentEval, currAction) = self.minMax(depth - 1, successorState, action, True, 0)
                else:
                    (currentEval, currAction) = self.minMax(depth, successorState, action, False, agentIndex + 1)
                value = min(value, currentEval)
            return value, currAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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
        value, action = self.expectimax(self.depth, gameState, "", True, 0)
        return action
        util.raiseNotDefined()

    def expectimax(self, depth, gameState, action, isMaxPlayer, agentIndex):
        maxAction = ""
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), action
        if isMaxPlayer:
            value = -9999999
            for action in gameState.getLegalActions(agentIndex):
                successorState = gameState.generateSuccessor(agentIndex, action)
                if not agentIndex == gameState.getNumAgents() - 1:
                    (currentEval, _) = self.expectimax(depth, successorState, maxAction, False, agentIndex + 1)
                if currentEval > value:
                    value = currentEval
                    maxAction = action
            return value, maxAction
        else:
            value = 0
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                successorState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    (currentEval, currAction) = self.expectimax(depth - 1, successorState, action, True, 0)
                else:
                    (currentEval, currAction) = self.expectimax(depth, successorState, action, False, agentIndex + 1)
                value += currentEval
            newValue = value * 1.0 / len(actions)
            return newValue, currAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>


      Get minimum distance to food, ghost, walls, capsules. Prioritizing each value based on certain factors explained below.
    """
    "*** YOUR CODE HERE ***"

    capsulePosition = currentGameState.getCapsules()
    currentScore = currentGameState.getScore()
    ghostPositions = currentGameState.getGhostPositions()
    foodList = currentGameState.getFood().asList()
    allWalls = currentGameState.getWalls()
    pacmanPos = currentGameState.getPacmanPosition()

    list_of_food_distances = []
    for food_coordinate in foodList:
        list_of_food_distances.append(util.manhattanDistance(pacmanPos, food_coordinate))
    if len(list_of_food_distances) == 0:
        minFoodDistance = 1
    elif len(list_of_food_distances) == 1:
        minFoodDistance = list_of_food_distances[0]
    else:
        minFoodDistance = min(list_of_food_distances)

    list_of_capsule_distances = []
    for capsule in capsulePosition:
        list_of_capsule_distances.append(util.manhattanDistance(pacmanPos, capsule))
    if len(list_of_capsule_distances) == 0:
        minCapsuleDistance = 1
    elif len(list_of_capsule_distances) == 1:
        minCapsuleDistance = list_of_capsule_distances[0]
    else:
        minCapsuleDistance = min(list_of_capsule_distances)

    # list_ghost_scared_ghosts = []
    list_of_ghost_distances = []
    for ghost in ghostPositions:
        # if ghost.scaredTimer:
        #     list_ghost_scared_ghosts.append(util.manhattanDistance(pacmanPos, ghost))
        # else:
        list_of_ghost_distances.append(util.manhattanDistance(pacmanPos, ghost))
    if len(list_of_ghost_distances) == 0:
        minGhostDistance = 1
    elif len(list_of_ghost_distances) == 1:
        minGhostDistance = list_of_ghost_distances[0]
    else:
        minGhostDistance = min(list_of_ghost_distances)

    # if len(list_ghost_scared_ghosts) == 0:
    #     minGhostScaredDistance = 1
    # elif len(list_ghost_scared_ghosts) == 1:
    #     minGhostScaredDistance = list_ghost_scared_ghosts[0]
    # else:
    #     minGhostScaredDistance = min(list_ghost_scared_ghosts)

    # maxGhostScared = max(list_ghost_scared_timer)

    list_of_walls = []
    for walls in allWalls:
        list_of_walls.append(util.manhattanDistance(pacmanPos, walls))
    if len(list_of_walls) == 0:
        minWallDistance = 1
    elif len(list_of_walls) == 1:
        minWallDistance = list_of_walls[0]
    else:
        minWallDistance = min(list_of_walls)

    gamma = -0.04

    # When capsule is as near as 5 distance, giving more weightage to it.
    if minCapsuleDistance >= 5:
        # When food distance is greater than ghost distance, more weightage for food
        if minGhostDistance > minFoodDistance:
            evaluationFunc = currentScore + gamma * (minFoodDistance + minCapsuleDistance * gamma + minWallDistance *
                                                     gamma * gamma + minGhostDistance * gamma * gamma * gamma)
        else:
            # If ghost is 1 position away, set least possible value.
            if minGhostDistance == 1:
                evaluationFunc = -4
            else:
                # Give more weightage to food, than ghost
                evaluationFunc = currentScore + gamma * (minFoodDistance + gamma * minGhostDistance + gamma * gamma *
                                                         minCapsuleDistance + gamma * gamma * gamma * minWallDistance)

    # elif not minGhostScaredDistance == 0:
    #     evaluationFunc = currentScore + gamma * (
    #             minFoodDistance + gamma * minWallDistance + gamma * gamma * minCapsuleDistance)
    else:
        evaluationFunc = currentScore + gamma * (minFoodDistance + gamma * minCapsuleDistance + gamma * gamma *
                                                 minGhostDistance + gamma * gamma * gamma * minWallDistance)

    return evaluationFunc

    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
