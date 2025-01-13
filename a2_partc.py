# Import required modules for game implementation
from a1_partc import Queue
from a1_partd import get_neighbors, count_neighbors, get_overflow_list, same_signs, overflow
from a2_partb import copy_board, sign, flatten_board, winning_sign, evaluate_intermediate_board, evaluate_winning_board, evaluate_board


class GameTree:
    """
    A class representing the game tree for AI decision making.
    Implements minimax algorithm with alpha-beta pruning for optimal move selection.
    """
    
    class Node:
        """
        A node in the game tree representing a game state.
        Each node contains the board state, current depth, player turn, and children nodes.
        """
        
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
            # Create a deep copy of the board to prevent state mutation
            self.board = copy_board(board)
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            # List to store all possible next moves as child nodes
            self.children = []
            # Score for this board position (calculated by minimax)
            self.score = None
            # The move that led to this board state
            self.move = None

        def is_terminal(self):
            """
            Check if the node is a terminal node (no further moves possible).
            A node is terminal if either all pieces are the same sign or max depth is reached.

            :return: True if terminal, False otherwise
            :rtype: bool
            """
            return same_signs(self.board) or self.depth == self.tree_height

        def expand(self):
            """
            Expand the node by generating all possible child nodes.
            Creates a new node for each valid move from the current position.
            """
            for move in self.get_possible_moves():
                # Create new board state for each possible move
                new_board = self.make_move(move)
                # Create a new child node with the updated board state and switch the player
                child_node = GameTree.Node(new_board, self.depth + 1, -self.player, self.tree_height)
                child_node.move = move
                self.children.append(child_node)

        def get_possible_moves(self):
            """
            Get all possible valid moves from the current board state.
            Checks each cell on the board for valid moves.

            :return: A list of valid moves (tuples of row and column indices)
            :rtype: list of tuple of int
            """
            moves = []
            # Iterate through each cell on the board
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if self.is_valid_move(r, c):
                        moves.append((r, c))
            return moves

        def is_valid_move(self, r, c):
            """
            Check if a move is valid at the given row and column.
            A move is valid if the cell is empty or contains the player's piece.

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
            Creates a new board state with the move applied.

            :param move: The move to make (row, column)
            :type move: tuple of int
            :return: The new board state after the move
            :rtype: list of list of int
            """
            r, c = move
            # Create a deep copy of the board to prevent state mutation
            new_board = copy_board(self.board)
            # Place the player's piece on the board
            new_board[r][c] += self.player
            # Handle any overflow situations that result from the move
            overflow(new_board, Queue())
            return new_board

    def __init__(self, board, player, tree_height=4):
        """
        Initialize the game tree with the current game state.

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
        # Create the root node representing the current game state
        self.root = GameTree.Node(self.board, 0, self.player, self.tree_height)

    def build_tree(self, node):
        """
        Build the game tree from the root or a specified node.
        Recursively generates all possible game states up to the specified tree height.

        :param node: The node to start building from
        :type node: GameTree.Node
        """
        if not node.is_terminal():
            # Generate all possible moves from the current node
            node.expand()
            for child in node.children:
                # Recursively build the tree for each child node
                self.build_tree(child)

    def minimax(self, node, alpha=float('-inf'), beta=float('inf')):
        """
        Perform the minimax algorithm with alpha-beta pruning to find the optimal move.
        Maximizes score for the AI player and minimizes for the opponent.

        :param node: The node to perform minimax on
        :type node: GameTree.Node
        :param alpha: The best score that the maximizer can guarantee
        :type alpha: float
        :param beta: The best score that the minimizer can guarantee
        :type beta: float
        :return: The minimax score of the node
        :rtype: int
        """
        if node.is_terminal():
            # Calculate the score for terminal nodes
            node.score = evaluate_board(node.board, self.player)
            return node.score

        if node.player == self.player:
            # Maximizing player's turn
            best_score = float('-inf')
            for child in node.children:
                best_score = max(best_score, self.minimax(child, alpha, beta))
                alpha = max(alpha, best_score)

                # Alpha-beta pruning: if this path is worse than the best path
                # already found by the minimizer, skip exploring it further
                if best_score >= beta:
                    break

            node.score = best_score
        else:
            # Minimizing player's turn
            best_score = float('inf')
            for child in node.children:
                best_score = min(best_score, self.minimax(child, alpha, beta))
                beta = min(beta, best_score)

                # Alpha-beta pruning: if this path is worse than the best path
                # already found by the maximizer, skip exploring it further
                if best_score <= alpha:
                    break

            node.score = best_score

        return node.score

    def get_move(self):
        """
        Get the best move for the current player based on minimax evaluation.
        Builds the game tree and applies minimax to find optimal move.

        :return: The best move (row, column) or None if no move is found
        :rtype: tuple of int or None
        """
        # Build the complete game tree from current position
        self.build_tree(self.root)
        best_score = self.minimax(self.root)

        # Find the child node that gave the best score
        for child in self.root.children:
            if child.score == best_score:
                return child.move

        # Return None if no valid moves are found
        return None

    def clear_tree(self):
        """
        Clear the game tree to free up memory.
        Sets the root node to None.
        """
        self.root = None


class Game:
    """
    Main game class that manages the game state and player interactions.
    Handles both human and AI player moves.
    """
    
    def __init__(self, board, human_player, ai_player, tree_height=4):
        """
        Initialize the game with the starting position and player assignments.

        :param board: The game board
        :type board: list of list of int
        :param human_player: The human player (1 or -1)
        :type human_player: int
        :param ai_player: The AI player (1 or -1)
        :type ai_player: int
        :param tree_height: The maximum depth of the game tree, defaults to 4
        :type tree_height: int, optional
        """
        self.board = board
        self.human_player = human_player
        self.ai_player = ai_player
        self.current_player = human_player
        self.tree_height = tree_height
        # Store move history for undo functionality
        self.move_history = []
        # Initialize the game tree for AI decision making
        self.game_tree = GameTree(board, ai_player, tree_height)

    def make_move(self, move):
        """
        Make a move on the board and handle the game state changes.
        Updates the board, handles overflow, and switches players.

        :param move: The move to make (row, column)
        :type move: tuple of int
        :return: True if the move was successful, False otherwise
        :rtype: bool
        """
        if self.current_player != self.human_player:
            raise PermissionError("It is not the human player's turn.")

        r, c = move
        if not self.is_valid_move(r, c):
            return False
        
        

        # Store the current state for potential undo
        self.move_history.append((copy_board(self.board), self.current_player))
        # Make the move and handle any overflow
        self.board[r][c] += self.current_player
        overflow(self.board, Queue())
        # Switch to AI player's turn
        self.current_player = self.ai_player
        return True

    def undo_move(self):
        """
        Undo the last move if the current player is human and game isn't over.
        Restores the previous board state and player turn.
        """
        if self.current_player == self.ai_player:
            raise PermissionError("Only human players can undo moves.")

        if self.is_game_over():
            raise RuntimeError("Cannot undo move, the game is already over.")

        if not self.move_history:
            raise RuntimeError("No move to undo.")

        # Restore the previous game state
        last_board, last_player = self.move_history.pop()
        self.board = last_board
        self.current_player = last_player
        # Re-evaluate the game state after undoing
        self.evaluate_board(self.board, self.current_player)

    def is_valid_move(self, r, c):
        """
        Check if a move is valid at the given position.
        A move is valid if the cell is empty or contains the player's piece.

        :param r: The row index
        :type r: int
        :param c: The column index
        :type c: int
        :return: True if the move is valid, False otherwise
        :rtype: bool
        """
        return self.board[r][c] == 0 or (self.board[r][c] * self.player > 0)

    def is_game_over(self):
        """
        Check if the game is over.
        Game is over if all pieces are same sign or no moves are left.

        :return: True if the game is over, False otherwise
        :rtype: bool
        """
        return same_signs(self.board) or not self.move_history

    def evaluate_board(self, board, player):
        """
        Evaluate the current board position for the given player.
        Uses the imported evaluate_board function to calculate score.

        :param board: The game board
        :type board: list of list of int
        :param player: The current player (1 for positive, -1 for negative)
        :type player: int
        :return: The evaluation score of the board
        :rtype: int
        """
        return evaluate_board(board, player)

    def ai_move(self):
        """
        Execute the AI player's move using the game tree.
        Gets the best move from the game tree and applies it.
        """
        if self.current_player != self.ai_player:
            raise PermissionError("It is not the AI's turn.")

        # Get the best move from the game tree
        move = self.game_tree.get_move()
        if move:
            # Apply the move and switch to human player's turn
            self.make_move(move)
            self.current_player = self.human_player
