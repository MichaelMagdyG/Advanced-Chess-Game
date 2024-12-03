import tkinter as tk
from tkinter import messagebox, simpledialog
import enum


class Color(enum.Enum):
    WHITE = 'white'
    BLACK = 'black'

class PieceType(enum.Enum):
    PAWN = 'pawn'
    ROOK = 'rook'
    KNIGHT = 'knight'
    BISHOP = 'bishop'
    QUEEN = 'queen'
    KING = 'king'

class ChessPiece:
    def __init__(self, piece_type, color, row, col):
        """
        Represents a chess piece with its type, color, and current position.
        """
        self.type = piece_type
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False
        self.symbol = self._get_symbol()

    def _get_symbol(self):
        """
        Returns the Unicode symbol for the piece based on its type and color.
        """
        symbols = {
            Color.WHITE: {
                PieceType.PAWN: '♙', 
                PieceType.ROOK: '♖', 
                PieceType.KNIGHT: '♘',
                PieceType.BISHOP: '♗', 
                PieceType.QUEEN: '♕', 
                PieceType.KING: '♔'
            },
            Color.BLACK: {
                PieceType.PAWN: '♟', 
                PieceType.ROOK: '♜', 
                PieceType.KNIGHT: '♞',
                PieceType.BISHOP: '♝', 
                PieceType.QUEEN: '♛', 
                PieceType.KING: '♚'
            }
        }
        return symbols[self.color][self.type]

    def get_possible_moves(self, board):
        """
        Generate possible moves for the piece. 
        To be implemented for each piece type.
        """
        raise NotImplementedError("Subclasses must implement this method")

class ChessBoard:
    def __init__(self, size=8):
        """
        Initialize the chess board with pieces in their starting positions.
        """
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self._setup_board()
        self.current_turn = Color.WHITE
        self.move_history = []

    def _setup_board(self):
        """
        Place pieces in their initial positions.
        """
        self.board[7][0] = ChessPiece(PieceType.ROOK, Color.WHITE, 7, 0)
        self.board[7][1] = ChessPiece(PieceType.KNIGHT, Color.WHITE, 7, 1)
        self.board[7][2] = ChessPiece(PieceType.BISHOP, Color.WHITE, 7, 2)
        self.board[7][3] = ChessPiece(PieceType.QUEEN, Color.WHITE, 7, 3)
        self.board[7][4] = ChessPiece(PieceType.KING, Color.WHITE, 7, 4)
        self.board[7][5] = ChessPiece(PieceType.BISHOP, Color.WHITE, 7, 5)
        self.board[7][6] = ChessPiece(PieceType.KNIGHT, Color.WHITE, 7, 6)
        self.board[7][7] = ChessPiece(PieceType.ROOK, Color.WHITE, 7, 7)
        
        for col in range(self.size):
            self.board[6][col] = ChessPiece(PieceType.PAWN, Color.WHITE, 6, col)
        
        self.board[0][0] = ChessPiece(PieceType.ROOK, Color.BLACK, 0, 0)
        self.board[0][1] = ChessPiece(PieceType.KNIGHT, Color.BLACK, 0, 1)
        self.board[0][2] = ChessPiece(PieceType.BISHOP, Color.BLACK, 0, 2)
        self.board[0][3] = ChessPiece(PieceType.QUEEN, Color.BLACK, 0, 3)
        self.board[0][4] = ChessPiece(PieceType.KING, Color.BLACK, 0, 4)
        self.board[0][5] = ChessPiece(PieceType.BISHOP, Color.BLACK, 0, 5)
        self.board[0][6] = ChessPiece(PieceType.KNIGHT, Color.BLACK, 0, 6)
        self.board[0][7] = ChessPiece(PieceType.ROOK, Color.BLACK, 0, 7)
        
        for col in range(self.size):
            self.board[1][col] = ChessPiece(PieceType.PAWN, Color.BLACK, 1, col)

    def is_valid_move(self, piece, new_row, new_col):
        """
        Check if the proposed move is valid.
        
        Args:
            piece (ChessPiece): The piece to be moved
            new_row (int): Destination row
            new_col (int): Destination column
        
        Returns:
            bool: True if the move is valid, False otherwise
        """
        if (new_row < 0 or new_row >= self.size or 
            new_col < 0 or new_col >= self.size):
            return False
        
        dest_piece = self.board[new_row][new_col]
        if dest_piece and dest_piece.color == piece.color:
            return False
        
        return True

    def move_piece(self, from_row, from_col, to_row, to_col):
        """
        Move a piece from one position to another.
        
        Args:
            from_row (int): Starting row
            from_col (int): Starting column
            to_row (int): Destination row
            to_col (int): Destination column
        
        Returns:
            bool: True if move was successful, False otherwise
        """
        piece = self.board[from_row][from_col]
        
        if not piece:
            return False
        
        if piece.color != self.current_turn:
            return False
        
        if not self.is_valid_move(piece, to_row, to_col):
            return False
        
        capture = self.board[to_row][to_col]
        move_record = {
            'piece': piece,
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'captured': capture
        }
        self.move_history.append(move_record)
        
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        piece.row = to_row
        piece.col = to_col
        piece.has_moved = True
        
        self.current_turn = (Color.BLACK if self.current_turn == Color.WHITE 
                             else Color.WHITE)
        
        return True

class ChessApp:
    def __init__(self, root):
        """
        Initialize the Chess Game GUI.
        
        Args:
            root (tk.Tk): The main window
        """
        self.root = root
        self.root.title("Advanced Chess Game")
        
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 80
        
        self.canvas = tk.Canvas(
            root, 
            width=self.BOARD_SIZE * self.SQUARE_SIZE, 
            height=self.BOARD_SIZE * self.SQUARE_SIZE
        )
        self.canvas.pack(padx=10, pady=10)
        
        self.chess_board = ChessBoard()
        self.drawn_pieces = {}
        
        self.canvas.bind('<Button-1>', self.on_square_click)
        
        self._draw_board()
        self._draw_pieces()
        
        self.selected_piece = None
        
        self.status_label = tk.Label(
            root, 
            text=f"White's Turn", 
            font=('Arial', 12)
        )
        self.status_label.pack(pady=5)

    def _draw_board(self):
        """
        Draw the chessboard squares.
        """
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = 'white' if (row + col) % 2 == 0 else 'lightgray'
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill=color, 
                    outline='black'
                )
                
                if col == 0:
                    self.canvas.create_text(
                        x1 + 10, y1 + 10, 
                        text=str(self.BOARD_SIZE - row), 
                        font=('Arial', 8)
                    )
                if row == self.BOARD_SIZE - 1:
                    self.canvas.create_text(
                        x1 + self.SQUARE_SIZE - 10, 
                        y1 + self.SQUARE_SIZE - 10, 
                        text=chr(97 + col), 
                        font=('Arial', 8)
                    )

    def _draw_pieces(self):
        """
        Draw all pieces on the board.
        """
        for piece in self.drawn_pieces.values():
            self.canvas.delete(piece)
        self.drawn_pieces.clear()
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.chess_board.board[row][col]
                if piece:
                    x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    
                    piece_text = self.canvas.create_text(
                        x, y, 
                        text=piece.symbol, 
                        font=('Arial', 36),
                        fill='black' if piece.color == Color.WHITE else 'darkgray'
                    )
                    
                    self.drawn_pieces[(row, col)] = piece_text

    def on_square_click(self, event):
        """
        Handle mouse click on the chessboard.
        
        Args:
            event: Tkinter mouse click event
        """
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        
        if (0 <= row < self.BOARD_SIZE and 
            0 <= col < self.BOARD_SIZE):
            
            clicked_piece = self.chess_board.board[row][col]
            
            if self.selected_piece:
                success = self.chess_board.move_piece(
                    self.selected_piece.row, 
                    self.selected_piece.col, 
                    row, 
                    col
                )
                
                if success:
                    self._draw_pieces()
                    
                    turn_text = ("White's Turn" if 
                                 self.chess_board.current_turn == Color.WHITE 
                                 else "Black's Turn")
                    self.status_label.config(text=turn_text)
                
                self.selected_piece = None
            
            elif clicked_piece:
                if clicked_piece.color == self.chess_board.current_turn:
                    self.selected_piece = clicked_piece

def main():
    """
    Main function to start the Chess Game.
    """
    root = tk.Tk()
    root.title("Advanced Chess Game")
    
    root.resizable(False, False)

    app = ChessApp(root)
    root.update_idletasks()
    
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()