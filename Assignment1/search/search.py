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
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push((problem.getStartState(), ()))
    explore_set = []

    while not frontier.isEmpty():
        (current_node, current_path) = frontier.pop()
        explore_set.append(current_node)
        if problem.isGoalState(current_node):
            return list(current_path)
        for (next_state, action, step_cost) in problem.getSuccessors(current_node):
            if next_state not in explore_set:
                frontier.push((next_state, (list(current_path) + [action])))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    frontier.push((problem.getStartState(), []))
    explore_set = []
    frontier_has_element = False

    while not frontier.isEmpty():
        (current_node, current_path) = frontier.pop()
        explore_set.append(current_node)
        if problem.isGoalState(current_node):
            return current_path
        for (next_state, action, step_cost) in problem.getSuccessors(current_node):
            if next_state not in explore_set:
                frontier_has_element = False
                for (state, listPath) in frontier.list:
                    if next_state == state:
                        frontier_has_element = True
                        break
                if not frontier_has_element:
                    frontier.push((next_state, current_path + [action]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    initial_state = problem.getStartState()
    initial_node = ((initial_state, []), 0)
    frontier = util.PriorityQueue()
    frontier.push(initial_node, 0)
    explore_set = []

    while not frontier.isEmpty():
        current_node, current_cost = frontier.pop()
        current_state = current_node[0]
        current_path = current_node[1]

        explore_set.append(current_state)
        if problem.isGoalState(current_state):
            return current_path
        for (next_state, action, step_cost) in problem.getSuccessors(current_state):
            frontier_has_element = False
            next_cost = current_cost + step_cost
            if next_state not in explore_set:
                list_action = current_path + [action]
                next_node = (next_state, list_action)
                for (_, _, node) in frontier.heap:
                    heap_state = node[0][0]
                    heap_cost = node[1]
                    if next_state == heap_state:
                        frontier_has_element = True
                        break
                if not frontier_has_element:
                    frontier.push((next_node, next_cost), next_cost)
                else:
                    if next_cost < heap_cost:
                        frontier.update((next_node, next_cost), next_cost)
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
    initial_state = problem.getStartState()
    initial_node = ((initial_state, []), 0)
    frontier = util.PriorityQueue()
    frontier.push(initial_node, heuristic(initial_state, problem))
    explore_set = []

    while not frontier.isEmpty():
        curr_node, curr_cost = frontier.pop()
        curr_state = curr_node[0]
        curr_path = curr_node[1]
        explore_set.append(curr_state)
        if problem.isGoalState(curr_state):
            return curr_path
        for (next_state, action, step_cost) in problem.getSuccessors(curr_state):
            next_cost = curr_cost + step_cost
            next_node = ((next_state, curr_path + [action]), next_cost)
            next_priority = next_cost + heuristic(next_state, problem)
            frontier_has_element = False
            if next_state not in explore_set:
                for (heap_priority, _, node) in frontier.heap:
                    heap_state = node[0][0]
                    if next_state == heap_state:
                        frontier_has_element = True
                        break
                if not frontier_has_element:
                    frontier.push(next_node, next_priority)
                else:
                    if next_priority < heap_priority:
                        frontier.update(next_node, next_priority)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch