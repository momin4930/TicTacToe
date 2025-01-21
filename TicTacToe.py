import tkinter as tk
from tkinter import messagebox
import random

# Function to evaluate the board and calculate score for a given player
def evaluate(b, player, opp):
    # Check rows for victory
    for row in range(3):
        if b[row][0] == b[row][1] == b[row][2] and b[row][0] != '_':
            return 10 if b[row][0] == player else -10
    # Check columns for victory
    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col] and b[0][col] != '_':
            return 10 if b[0][col] == player else -10
    # Check diagonals for victory
    if b[0][0] == b[1][1] == b[2][2] and b[0][0] != '_':
        return 10 if b[0][0] == player else -10
    if b[0][2] == b[1][1] == b[2][0] and b[0][2] != '_':
        return 10 if b[0][2] == player else -10
    # No victory conditions met
    return 0

# Alpha-Beta pruning algorithm to calculate the optimal move
def alphaBeta(board, depth, isMax, alpha, beta, player, opp):
    score = evaluate(board, player, opp)
    # If player has won, subtract depth to prioritize faster wins
    if score == 10:
        return score - depth
    # If opponent has won, add depth to prioritize faster wins for the opponent
    if score == -10:
        return score + depth
    # If no moves left, it's a draw
    if not any('_' in row for row in board):
        return 0

    # Maximizer's move
    if isMax:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    best = max(best, alphaBeta(board, depth + 1, False, alpha, beta, player, opp))
                    board[i][j] = '_'
                    alpha = max(alpha, best)
                    if beta <= alpha:  # Prune the branches
                        break
        return best
    # Minimizer's move
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opp
                    best = min(best, alphaBeta(board, depth + 1, True, alpha, beta, player, opp))
                    board[i][j] = '_'
                    beta = min(beta, best)
                    if beta <= alpha:  # Prune the branches
                        break
        return best

# Function to find the best move for the AI
def findBestMove(board, player, opp):
    bestVal = -1000  # Initialize best value for AI
    bestMove = (-1, -1)  # Initialize best move coordinates
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = player
                moveVal = alphaBeta(board, 0, False, -float('inf'), float('inf'), player, opp)
                board[i][j] = '_'
                if moveVal > bestVal:  # Update the best move
                    bestVal = moveVal
                    bestMove = (i, j)
    return bestMove

# GUI for Tic Tac Toe game
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")  # Set window title
        self.board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]  # Initialize game board
        self.player = 'X'  # Default player symbol
        self.opp = 'O'  # Default AI symbol
        self.difficulty = "Easy"  # Default difficulty level
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Buttons for GUI grid
        self.create_widgets()

    # Create GUI components
    def create_widgets(self):
        tk.Label(self.root, text="Tic Tac Toe", font=("Helvetica", 20, "bold")).pack()

        # Reset button
        tk.Button(self.root, text="Reset", command=self.reset_game, font=("Helvetica", 12), bg="lightblue").pack(pady=10)

        # Difficulty selection buttons
        tk.Label(self.root, text="Choose Difficulty:", font=("Helvetica", 14)).pack()
        tk.Button(self.root, text="Easy", command=lambda: self.set_difficulty("Easy"), font=("Helvetica", 12), bg="lightgreen").pack(pady=5)
        tk.Button(self.root, text="Hard", command=lambda: self.set_difficulty("Hard"), font=("Helvetica", 12), bg="red", fg="white").pack(pady=5)

        # Game board grid
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.board_frame, text="", font=("Helvetica", 24), width=5, height=2,
                    command=lambda row=i, col=j: self.player_move(row, col), bg="white"
                )
                self.buttons[i][j].grid(row=i, column=j)

        self.select_symbol()

    # Allow the user to select their symbol (X or O)
    def select_symbol(self):
        symbol = messagebox.askquestion("Choose Symbol", "Do you want to play as 'X'? (Click 'No' for 'O')")
        if symbol == "no":
            self.player = 'O'
            self.opp = 'X'

    # Set game difficulty
    def set_difficulty(self, level):
        self.difficulty = level
        messagebox.showinfo("Difficulty Set", f"Difficulty set to {level}.")

    # Handle player's move
    def player_move(self, row, col):
        if self.board[row][col] == '_':  # Check if cell is empty
            self.board[row][col] = self.player
            self.buttons[row][col].config(text=self.player, state="disabled", disabledforeground="blue")
            if self.check_winner(self.player):  # Check if the player wins
                self.highlight_winner(self.player)
                messagebox.showinfo("Game Over", "You Win!")
                self.disable_board()
                return
            if not any('_' in row for row in self.board):  # Check for a draw
                messagebox.showinfo("Game Over", "It's a Draw!")
                return
            self.ai_move()  # AI's turn

    # Handle AI's move
    def ai_move(self):
        if self.difficulty == "Easy":
            # Random move for Easy difficulty
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '_']
            move = random.choice(empty_cells)
        else:
            # Use Alpha-Beta pruning for Hard difficulty
            move = findBestMove(self.board, self.opp, self.player)
        self.board[move[0]][move[1]] = self.opp
        self.buttons[move[0]][move[1]].config(text=self.opp, state="disabled", disabledforeground="red")
        if self.check_winner(self.opp):  # Check if AI wins
            self.highlight_winner(self.opp)
            messagebox.showinfo("Game Over", "AI Wins!")
            self.disable_board()

    # Check for a winner
    def check_winner(self, player):
        # Check rows, columns, and diagonals
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    # Highlight winning cells
    def highlight_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                for j in range(3):
                    self.buttons[i][j].config(bg="lightgreen")
            if all(self.board[j][i] == player for j in range(3)):
                for j in range(3):
                    self.buttons[j][i].config(bg="lightgreen")
        if all(self.board[i][i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][i].config(bg="lightgreen")
        if all(self.board[i][2 - i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][2 - i].config(bg="lightgreen")

    # Disable the board after the game ends
    def disable_board(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    # Reset the game to its initial state
    def reset_game(self):
        self.board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", bg="white")
        self.select_symbol()

# Initialize and run the game
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()