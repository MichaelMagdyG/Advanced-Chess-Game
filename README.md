# Advanced Chess Game

This is an advanced chess game built using Python and the Tkinter library for the graphical user interface (GUI). It allows players to play chess on an interactive board, with pieces represented by Unicode chess symbols. The game supports the standard rules of chess, with special handling for player turns, piece movement, and capture.

## Features

- **Interactive GUI**: Click on the chessboard to select and move pieces.
- **Piece Movement**: Supports the movement of all chess pieces, with special handling for each piece type (Pawn, Rook, Knight, Bishop, Queen, and King).
- **Turn-based Gameplay**: The game alternates between White's turn and Black's turn.
- **Chessboard Setup**: The board is automatically set up in the initial configuration, with White and Black pieces in their starting positions.

## Screenshot

![Chess Game Screenshot](Screenshot%202024-12-03%20181326.jpg)

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## How to Run

1. Clone this repository or download the `chess_game.py` file.
2. Make sure you have Python 3.x installed on your machine.
3. Run the Python script:

   ```bash
   python chess_game.py
4. The chessboard window will open, and you can start playing.

## Code Structure
- ChessPiece class: Represents a single chess piece, storing its type, color, position, and methods for handling its movements.
- ChessBoard class: Manages the board state, including the placement of pieces, validation of moves, and turn switching.
- ChessApp class: Handles the graphical interface and user interaction, drawing the chessboard and updating the game state based on user input.

## How to Play
- To move a piece, click on the piece and then click on the destination square.
- The game alternates turns between White and Black.
- The game checks if a move is valid before allowing it, preventing invalid moves such as moving into your own pieces or moving out of bounds.

## Example
1. White's turn: Click on a white piece.
2. Select the destination square to move the piece.
3. The game will automatically switch to Black's turn, and the process repeats.