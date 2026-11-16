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

    stack = util.Stack()
    visited = set()

    stack.push((problem.getStartState(), []))

    while(not stack.isEmpty()):
        state, path = stack.pop()
        if(problem.isGoalState(state)):
            return path
        visited.add(state)

        successor = problem.getSuccessors(state)

        for state,nextpath,cost in reversed(successor):
            if(state in visited):
                continue
            stack.push((state, path + [nextpath]))

    return []

def breadthFirstSearch(problem: SearchProblem):
    queue = util.Queue()
    # 由于出队的操作，访问 C 后，C 出队了。当再次遇到 C 的时候，扩展 C 的话，这时并不是最短路径
    visited = set()
    # 记录已经进入队列的数据，之所以这样做，是因为广度优先只要进入队列就已经是最短路径了
    inQueue = set()

    queue.push((problem.getStartState(), []))

    while(not queue.isEmpty()):
        state, path = queue.pop()
        if(problem.isGoalState(state)):
            return path

        visited.add(state)

        successor = problem.getSuccessors(state)
        for state,nextpath,cost in successor:
            if(state in visited or state in inQueue):
                continue
            queue.push((state, path + [nextpath]))
            inQueue.add(state)

    return []

def uniformCostSearch(problem: SearchProblem):
    queue = util.PriorityQueue()
    visited = set()

    startState = problem.getStartState()
    queue.push((startState,[], 0), 0)

    while(not queue.isEmpty()):
        current_state, current_path, current_cost = queue.pop()
        if(problem.isGoalState(current_state)):
            return current_path
        if(current_state in visited):
            continue

        visited.add(current_state)

        successors = problem.getSuccessors(current_state)
        for state, action, cost in successors:
            next_cost = cost + current_cost
            queue.push((state, current_path + [action], next_cost), next_cost)

    return []

def nullHeuristic(state, problem=None):
    s, a, c = state
    return c + problem.getCostOfActions(a)

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    # fn = g(n) + h(n)
    # g(n) 从根开始到当前节点的 cost 总和
    # h(n) 是选择某个 action 的代价估算
    # 在统一代价搜索的基础上增加了 h(n)
    h = lambda s: nullHeuristic(s, problem)
    queue = util.PriorityQueueWithFunction(h)
    visited = set()

    start_state = problem.getStartState()
    queue.push((start_state, [], 0))

    while(not queue.isEmpty()):
        current_state, current_path, current_cost = queue.pop()
        if(problem.isGoalState(current_state)):
            return current_path
        if(current_state in visited):
            continue
        visited.add(current_state)

        successors = problem.getSuccessors(current_state)

        for state, action, cost in successors:
            queue.push((state, current_path + [action], cost+current_cost))

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
