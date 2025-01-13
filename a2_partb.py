
from a1_partc import Queue
from a1_partd import get_neighbors, count_neighbors, get_overflow_list, same_signs, overflow

def copy_board(board):
    """
    Create a deep copy of the game board.

    :param board: The game board to copy
    :type board: list of list of int
    :return: A deep copy of the board
    :rtype: list of list of int
    """
    return [row.copy() for row in board]

def sign(cell):
    """
    Determine the sign of a cell's value.

    :param cell: The cell value
    :type cell: int
    :return: 1 if the cell is positive, -1 if negative, 0 if zero
    :rtype: int
    """
    return (cell > 0) - (cell < 0)

def flatten_board(board):
    """
    Flatten a 2D game board into a 1D list.

    :param board: The game board to flatten
    :type board: list of list of int
    :return: The flattened board
    :rtype: list of int
    """
    return [cell for row in board for cell in row]

def winning_sign(board):
    """
    Determine the sign of the first non-zero cell in the board.

    :param board: The game board
    :type board: list of list of int
    :return: The sign of the first non-zero cell
    :rtype: int
    :raises ValueError: If the board is empty or contains only zeroes
    """
    flat_board = flatten_board(board)
    # Since all the sings are the same, we can just check the first non-zero cell
    first_non_zero_cell = next(cell for cell in flat_board if cell != 0)
    return sign(first_non_zero_cell)

def evaluate_intermediate_board(board, player):
    """
    Evaluate the intermediate state of the board for the given player.

    :param board: The game board
    :type board: list of list of int
    :param player: The current player (1 for positive, -1 for negative)
    :type player: int
    :return: The evaluation score of the board
    :rtype: int
    """
    flat_board = flatten_board(board)
    # Count the extra slots occupied by any player, the more the better
    total_score = sum(sign(cell) for cell in flat_board)
    return total_score if sign(total_score) == player else -total_score

def evaluate_winning_board(board, player):
    """
    Evaluate the board if a player has won.

    :param board: The game board
    :type board: list of list of int
    :param player: The current player (1 for positive, -1 for negative)
    :type player: int
    :return: The evaluation score of the winning board
    :rtype: int
    """
    winning_player = winning_sign(board)
    return float('inf') if winning_player == player else float('-inf')

def evaluate_board(board, player):
    """
    Evaluate the board to determine its score.

    :param board: The game board
    :type board: list of list of int
    :param player: The current player (1 for positive, -1 for negative)
    :type player: int
    :return: The evaluation score of the board
    :rtype: int
    """
    if same_signs(board):
        return evaluate_winning_board(board, player)
    
    # No player has won yet, evaluate the intermediate state
    return evaluate_intermediate_board(board, player)

class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height):
            """
            Initialize a game tree node.

            :param board: The game board
            :type board: list of list of int
            :param depth: The depth of the node in the tree
            :type depth: int
            :param player: The current player (1 for positive, -1 for negative)
            :type player: int
            :param tree_height: The maximum depth of the tree
            :type tree_height: int
            """
            self.board = copy_board(board)
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            self.children = []
            self.score = None
            self.move = None

        def is_terminal(self):
            """
            Check if the node is a terminal node (no further moves possible).

            :return: True if terminal, False otherwise
            :rtype: bool
            """
            return same_signs(self.board) or self.depth == self.tree_height

        def expand(self):
            """
            Expand the node by generating all possible child nodes.
            """
            for move in self.get_possible_moves():
                new_board = self.make_move(move)
                # Create a new child node with the updated board state and switch the player
                child_node = GameTree.Node(new_board, self.depth + 1, -self.player, self.tree_height)
                child_node.move = move
                self.children.append(child_node)

        def get_possible_moves(self):
            """
            Get all possible valid moves from the current board state.

            :return: A list of valid moves (tuples of row and column indices)
            :rtype: list of tuple of int
            """
            moves = []
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if self.is_valid_move(r, c):
                        moves.append((r, c))
            return moves

        def is_valid_move(self, r, c):
            """
            Check if a move is valid at the given row and column.

            :param r: The row index
            :type r: int
            :param c: The column index
            :type c: int
            :return: True if the move is valid, False otherwise
            :rtype: bool
            """
            
            # A move is valid if the cell is empty or the player's piece is already there
            return self.board[r][c] == 0 or (self.board[r][c] * self.player > 0)

        def make_move(self, move):
            """
            Make a move on the board and handle overflow.

            :param move: The move to make (row, column)
            :type move: tuple of int
            :return: The new board state after the move
            :rtype: list of list of int
            """
            r, c = move
            new_board = copy_board(self.board)
            # Place the player's piece on the board
            new_board[r][c] += self.player
            overflow(new_board, Queue())
            return new_board

    def __init__(self, board, player, tree_height=4):
        """
        Initialize the game tree.

        :param board: The game board
        :type board: list of list of int
        :param player: The current player (1 for positive, -1 for negative)
        :type player: int
        :param tree_height: The maximum depth of the tree, defaults to 4
        :type tree_height: int, optional
        """
        self.player = player
        self.board = copy_board(board)
        self.tree_height = tree_height
        self.root = GameTree.Node(self.board, 0, self.player, self.tree_height)

    def build_tree(self, node):
        """
        Build the game tree from the root or a specified node.

        :param node: The node to start building from, defaults to None
        :type node: GameTree.Node, optional
        """
        if not node.is_terminal():
            # Uncover all possible moves from the current node
            node.expand()
            for child in node.children:
                # Recursively build the tree for each child node
                self.build_tree(child)

    def minimax(self, node, alpha = float('-inf'), beta = float('inf')):
        """
        Perform the minimax algorithm to find the optimal move.

        :param node: The node to perform minimax on
        :type node: GameTree.Node
        :return: The minimax score of the node
        :rtype: int
        """
        if node.is_terminal():
            node.score = evaluate_board(node.board, self.player)
            return node.score
        
        if node.player == self.player:
            # Set the initial best score to absurdly low value
            best_score = float('-inf')
            for child in node.children:
                best_score = max(best_score, self.minimax(child, alpha, beta))
                alpha = max(alpha, best_score)

                # prune the obvious bad branches
                if best_score >= beta:
                    break

            node.score = best_score
        else:
            # Set the initial best score to absurdly high value
            best_score = float('inf')
            for child in node.children:
                best_score = min(best_score, self.minimax(child, alpha, beta))
                beta = min(beta, best_score)

                # prune the obvious bad branches
                if best_score <= alpha:
                    break

            node.score = best_score
        
        return node.score

    def get_move(self):
        """
        Get the best move for the current player.

        :return: The best move (row, column) or None if no move is found
        :rtype: tuple of int or None
        """
        self.build_tree(self.root)
        best_score = self.minimax(self.root)
        
        # Find the child node that gave the best score
        for child in self.root.children:
            if child.score == best_score:
                return child.move

        # No move found
        return None

    def clear_tree(self):
        """
        Clear the game tree.
        """
        self.root = None