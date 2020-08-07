from operator import add
import sys
from ui import *

def get_problem(file_path):
    f = open(file_path)
    file_content = f.read().split("\n")

    """
        x: indicating rows
        y: indicating columns
    """

    row, column = map(int, file_content[0].split())
    start_state = list(map(int, file_content[1].split()))# Sx, Sy
    end_state = list(map(int, file_content[2].split()))# Gx, Gy
    matrix = [list(map(int, row.split()))
              for row in file_content[3:]]  # Get matrix maze
    f.close()

    return Problem(start_state, end_state, matrix, row, column)


class Cell:
    def __init__(self, state, parent_state, cost = 0):
        # A list:current position of the cell, where state[0]:x, state[1]:y
        self.state = state
        self.parent_state = parent_state
        self.cost = cost


class Problem:
    def __init__(self, start_state, goal_state, matrix, row, column):
        self.start_state = start_state
        self.goal_state = goal_state
        self.matrix = matrix
        self.row = row
        self.column = column

    def isGoalState(self, state):
        if state == self.goal_state:
            return True
        return False

    def getAdjacent(self, current_state):
        adjacent_cells = []
        added_cost = []
        next_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        diag_moves = (1, 1), (-1, -1), (1, -1), (-1, 1)

        # Find next cells from up, down, left, right directions
        for pos in next_moves:
            state = [current_state[0] + pos[0], current_state[1] + pos[1]]

            if (state[0] >= 0 and state[0] < self.row)and (state[1] >= 0 and state[1] < self.column):
                if self.matrix[state[0]][state[1]] == 0:
                    adjacent_cells.append(state)
                    added_cost.append(distance_euclid(current_state, state))

        # Find next cells from diagnol directions
        for pos in diag_moves:
            state = [current_state[0] + pos[0], current_state[1] + pos[1]]
            if (state[0] >= 0 and state[0] < self.row)and (state[1] >= 0 and state[1] < self.column):
                if self.matrix[state[0] - pos[0]][state[1]] == 0 or self.matrix[state[0]][state[1] - pos[1]] == 0:
                    if self.matrix[state[0]][state[1]] == 0:
                        adjacent_cells.append(state)
                        added_cost.append(
                            distance_euclid(current_state, state))
        return zip(adjacent_cells, added_cost)


def distance_euclid(current_state, next_state):
    return ((current_state[0] - next_state[0])**2 + (current_state[1] - next_state[1])**2)**0.5


def heuristic(current_state, goal_state):
    return ((current_state[0] - goal_state[0])**2 + (current_state[1] - goal_state[1])**2)**0.5


def find_lowest_f_cost(queue):
    _min = queue[0][1]
    index = 0
    for i in range(0, len(queue)):
        if queue[i][1] < _min:
            _min = queue[i][1]
            index = i

    return index


def pathTo(node):
    """ 
        Return a path in a list of (x, y)
    """
    actions = []
    actions.append(node.state)
    while node.parent_state is not None:
        actions.append(node.parent_state.state)
        node = node.parent_state

    actions.reverse()

    return actions


def a_star(problem):
    """
        Path finding with A* algorithm
        Return path if found and explored path
    """


    # List as elements, queue[0] is a Cell, q[1] is f(n) = g(n) + h(n)
    priority_queue = []
    priority_queue.append([Cell(problem.start_state, None), heuristic(
        problem.start_state, problem.goal_state)])

    explored_set = []
    while len(priority_queue) > 0:
        current_cell, f_cost = priority_queue.pop(
            find_lowest_f_cost(priority_queue))

        if current_cell.state in explored_set:
            continue

        explored_set.append(current_cell.state)
        if problem.isGoalState(current_cell.state):
            return pathTo(current_cell), explored_set

        for next, added_cost in list(problem.getAdjacent(current_cell.state)):
            priority_queue.append([Cell(next, current_cell, added_cost + current_cell.cost), 
                                   added_cost + current_cell.cost + heuristic(next, problem.goal_state)])
    return-1, explored_set


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end = " ")

        print()


def save_to_file(problem, path, output_file):

    for x in range(len(problem.matrix)):
        for y in range(len(problem.matrix[x])):
            if problem.matrix[x][y] == 1:
                problem.matrix[x][y] = 'o'
            else:
                problem.matrix[x][y] = '-'
    f = open(output_file, "w")
    if path == -1:
        f.write("-1")
        f.close()
        return

    for x, y in path:
        problem.matrix[x][y] = 'x'
    problem.matrix[path[0][0]][path[0][1]] = 'S'
    problem.matrix[path[-1][0]][path[-1][1]] = 'G'
    


    f.write(str(path) + '\n')
    for line in problem.matrix:
        f.write(" ".join(line) + "\n")
    f.close()


if __name__ == "__main__":
    """
        CMD: List 
        argv[1]: input.txt
        argv[2]: output.txt
    """

    if len(sys.argv) > 2:
        problem = get_problem(sys.argv[1])
        solution = a_star(problem)
        save_to_file(problem, solution[0], sys.argv[2])

        # UI
        main(problem, solution)
    else:
        problem = get_problem("ex.txt")
        solution = a_star(problem)
        save_to_file(problem, solution[0], "output.txt")

        # UI
        main(problem, solution)
       
        
        
 