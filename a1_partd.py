# copy over your a1_partd.py file here
#    Main Author(s): Paras Singh
#    Main Reviewer(s): Khwahish Vaid

from a1_partc import Queue


def get_neighbors(data, r, c):
    # right, up, left, down
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    neighbors = []
    # check if the neighbors are within the grid
    for dx, dy in directions:
        nx, ny = r + dx, c + dy
        if 0 <= nx < len(data) and 0 <= ny < len(data[0]):
            neighbors.append((nx, ny))
    return neighbors

def count_neighbors(data, r, c):
    # return the number of neighbors
    return len(get_neighbors(data, r, c))

def get_overflow_list(grid):
    overflow_list = []
    for row_index, row in enumerate(grid):
        for column_index, column in enumerate(row):
            number_of_neighbors = count_neighbors(grid, row_index, column_index)
            if abs(column) >= number_of_neighbors:
                overflow_list.append((row_index, column_index))
    return overflow_list or None


def same_signs(data):
    non_zero_cells = [x for row in data for x in row if x != 0]
    if not non_zero_cells:
        return True
    assume_sign = (non_zero_cells[0] > 0) - (non_zero_cells[0] < 0)
    return all((x > 0) - (x < 0) == assume_sign for x in non_zero_cells)

def overflow(grid, a_queue):
    overflow_list = get_overflow_list(grid)
    if not overflow_list or same_signs(grid):
        return 0

    new_grid = [row[:] for row in grid]
    for r, c in overflow_list:
        new_grid[r][c] = 0

    for r, c in overflow_list:
        neighbors = get_neighbors(grid, r, c)
        for x, y in neighbors:
            new_grid[x][y] += 1 if new_grid[x][y] > 0 else -1

        for x, y in neighbors:
            # if the sign of the neighbor is different from the sign of the overflow cell
            
            if (new_grid[x][y] > 0) - (new_grid[x][y] < 0) != (grid[r][c] > 0) - (grid[r][c] < 0):
                # flip the sign of the neighbor
                
                new_grid[x][y] *= -1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = new_grid[i][j]

    a_queue.enqueue([row[:] for row in grid])

    return overflow(grid, a_queue) + 1
