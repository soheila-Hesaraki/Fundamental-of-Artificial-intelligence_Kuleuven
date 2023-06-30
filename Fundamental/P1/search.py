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

def depthFirstSearch(problem: SearchProblem):
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
    visited_nodes = {}  # A dictionary of nodes that have been visited so far and the direction that we used to find them
    Action_list = [] # Packman's list of actions that has taken so far to reach to the goal
    stack = util.Stack() # "stack" contains triplets of: (successor,action, stepCost)

    nodes_history = {} # contains nodes that packman has passed to reach there (nodes + node's parents)

    start_node = problem.getStartState()
    stack.push((start_node, '_', 0))
    # For the strat node packman has not moved to reach there, So, we don't have any direction. I defined it with '_'
    visited_nodes[start_node] = '_'

    if problem.isGoalState(start_node): # Is the start node a goal?
        return Action_list

    goal = False;

    while (stack.isEmpty() == False and goal == False):

        node = stack.pop() #Pop the most recently pushed item from the stack
        visited_nodes[node[0]] = node[1] #storing the node and its direction

        if problem.isGoalState(node[0]): # Is the node a goal?
            desired_node = node[0]
            goal = True
            break

        # Expanding the search space
        for child_node in problem.getSuccessors(node[0]):

            if child_node[0] not in visited_nodes.keys(): #If we have not visited the child node
                nodes_history[child_node[0]] = node[0] #storing the child node and its parent
                stack.push(child_node) #Push child node onto the stack

    # Bulding the path to the desired node by finding parent, parents of parent, ans so on
    while (desired_node in nodes_history.keys()):
        previous_desired_node = nodes_history[desired_node]
        Action_list.insert(0, visited_nodes[desired_node]) #Adding the direction that was needed to go to the desired node
        desired_node = previous_desired_node #Going to the previous node to fnd the parents of parent

    return Action_list

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited_nodes = {} #A dictionary of nodes that have been visited so far and the direction that we used to find them
    Action_list = [] # Packman's list of actions that has taken so far to reach to the goal

    queue = util.Queue() #triplets of: (successor,action, stepCost)
    nodes_history = {} # contains nodes that packman has passed to reach there (nodes + node's parents)

    start_node = problem.getStartState()
    queue.push((start_node, '_', 0))
    # For the strat node packman has not moved to reach there, So, we don't have any direction. I defined it with '_'
    visited_nodes[start_node] = '_'

    if problem.isGoalState(start_node): #Is the start node a goal?
        return Action_list

    goal = False;
    while (queue.isEmpty() == False and goal == False):

        node = queue.pop() #Pop the most recently pushed item from the stack
        visited_nodes[node[0]] = node[1] #storing the node and its direction

        if problem.isGoalState(node[0]): # Is the node a goal?
            desired_node = node[0]
            goal = True
            break

        # Expanding the search space
        for child_node in problem.getSuccessors(node[0]):
            # If we have not visited the child node
            if child_node[0] not in visited_nodes.keys() and child_node[0] not in nodes_history.keys():
                nodes_history[child_node[0]] = node[0]  #storing the child node and its parent
                queue.push(child_node) #Push child node onto the queue

    # Bulding the path to the desired node by finding parent, parents of parent, ans so on
    while (desired_node in nodes_history.keys()):
        previous_desired_node = nodes_history[desired_node]
        Action_list.insert(0, visited_nodes[desired_node]) #Adding the direction that was needed to go to the desired node
        desired_node = previous_desired_node #Going to the previous node to fnd the parents of parent

    return Action_list

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    visited_nodes = {} #A dictionary of nodes that have been visited so far and the direction that we used to find them
    Action_list = [] # Packman's list of actions that has taken so far to reach to the goal
    queue = util.PriorityQueue() #triplets of: (successor,action, stepCost)
    nodes_history = {} # contains nodes that packman has passed to reach there (nodes + node's parents)
    cost = {}  #A dictionary of nodes and the incremental cost of expanding to that node

    start_node = problem.getStartState()
    # For the strat node packman has not moved to reach there, So, we don't have any direction. I defined it with '_'
    queue.push((start_node, '_', 0), 0)

    visited_nodes[start_node] = '_'
    cost[start_node] = 0 # For the strat node packman has not moved to reach there, So, its cost is 0

    if problem.isGoalState(start_node): # Is the start node a goal?
        return Action_list

    goal = False;
    while (queue.isEmpty() == False and goal == False):

        node = queue.pop() # Pop the most recently pushed item from the stack
        visited_nodes[node[0]] = node[1]  # storing the node and its parent

        if problem.isGoalState(node[0]):  # Is the node a goal?
            desired_node = node[0]
            goal = True
            break

        # Expanding the search space
        for child_node in problem.getSuccessors(node[0]): # Expanding the search space

            if child_node[0] not in visited_nodes.keys():  # If we have not visited the child node
                priority = node[2] + child_node[2] #new cost calculation

                if child_node[0] in cost.keys(): # if the cost of this node was already calculated forexample when we
                    # expanded a different node,
                    if cost[child_node[0]] <= priority: # if new cost is more than old cost, continue
                        continue


                queue.push((child_node[0], child_node[1], priority), priority)# if new cost is less than old
                # cost, push to queue and change cost and parent
                cost[child_node[0]] = priority
                nodes_history[child_node[0]] = node[0]  # storing the node and its parent

    # Bulding the path to the desired node by finding parent, parents of parent, ans so on
    while (desired_node in nodes_history.keys()):

        previous_desired_node = nodes_history[desired_node]
        Action_list.insert(0, visited_nodes[desired_node])#Adding the direction that was needed to go to the desired node

        desired_node = previous_desired_node #Going to the previous node to fnd the parents of parent

    return Action_list


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited_nodes = {} #A dictionary of nodes that have been visited so far and the direction that we used to find them
    Action_list = [] # Packman's list of actions that has taken so far to reach to the goal
    queue = util.PriorityQueue()  #triplets of: (successor,action, stepCost)
    nodes_history = {}  # contains nodes that packman has passed to reach there (nodes + node's parents)
    cost = {}  #A dictionary of nodes and the incremental cost of expanding to that node

    start = problem.getStartState()
    queue.push((start, '_', 0), 0) # For the strat node packman has not moved to reach there, So, we don't have
    # any direction. I defined it with '_'

    visited_nodes[start] = '_'
    cost[start] = 0 # For the strat node packman has not moved to reach there, So, its cost is 0

    if problem.isGoalState(start):  # Is the start node a goal?
        return solution

    goal = False;
    while (queue.isEmpty() == False and goal == False):

        node = queue.pop()  # Pop the most recently pushed item from the stack
        visited_nodes[node[0]] = node[1] # storing the node and its parent

        if problem.isGoalState(node[0]): # Is the node a goal?
            desired_node = node[0]
            goal = True
            break

        # Expanding the search space
        for child_node in problem.getSuccessors(node[0]):

            if child_node[0] not in visited_nodes.keys(): # If we have not visited the child node
                priority = node[2] + child_node[2] + heuristic(child_node[0], problem) #new cost calculation

                if child_node[0] in cost.keys(): # if the cost of this node was already calculated forexample when we
                    # expanded a different node,
                    if cost[child_node[0]] <= priority:  #if new cost is more than old cost, continue
                        continue

                queue.push((child_node[0], child_node[1], node[2] + child_node[2]), priority) # if new cost is less than old
                # cost, push to queue and change cost and parent
                cost[child_node[0]] = priority
                nodes_history[child_node[0]] = node[0] # storing the node and its parent

    # Bulding the path to the desired node by finding parent, parents of parent, ans so on
    while (desired_node in nodes_history.keys()):

        previous_desired_node = nodes_history[desired_node]
        Action_list.insert(0, visited_nodes[desired_node]) #Adding the direction that was needed to go to the desired node
        desired_node = previous_desired_node

    return Action_list



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
