import pygame
import sys
from enum import Enum, auto

# Initialize pygame
pygame.init()

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
IMAGES = {}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_SQUARE = (118, 150, 86)
LIGHT_SQUARE = (238, 238, 210)
HIGHLIGHT = (255, 255, 0, 50)  # Semi-transparent yellow
MOVE_HIGHLIGHT = (0, 0, 255, 50)  # Semi-transparent blue
CHECK_HIGHLIGHT = (255, 0, 0, 100)  # Semi-transparent red

# Piece types
class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

# Piece colors
class PieceColor(Enum):
    WHITE = auto()
    BLACK = auto()

class Piece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type
        self.color = color
        self.position = position
        self.has_moved = False
    
    def get_image_key(self):
        color_str = "w" if self.color == PieceColor.WHITE else "b"
        type_map = {
            PieceType.PAWN: "p",
            PieceType.KNIGHT: "n",
            PieceType.BISHOP: "b",
            PieceType.ROOK: "r",
            PieceType.QUEEN: "q",
            PieceType.KING: "k"
        }
        return color_str + type_map[self.piece_type]

    def get_possible_moves(self, board):
        row, col = self.position
        moves = []
        
        # Pawn movement logic
        if self.piece_type == PieceType.PAWN:
            direction = -1 if self.color == PieceColor.WHITE else 1
            
            # Move forward one square
            if 0 <= row + direction < BOARD_SIZE:
                if board[row + direction][col] is None:
                    moves.append((row + direction, col))
                    
                    # Move forward two squares from starting position
                    if ((self.color == PieceColor.WHITE and row == 6) or 
                        (self.color == PieceColor.BLACK and row == 1)):
                        if (0 <= row + 2*direction < BOARD_SIZE and 
                            board[row + 2*direction][col] is None):
                            moves.append((row + 2*direction, col))
            
            # Capture diagonally
            for dc in [-1, 1]:
                if 0 <= row + direction < BOARD_SIZE and 0 <= col + dc < BOARD_SIZE:
                    target = board[row + direction][col + dc]
                    if target and target.color != self.color:
                        moves.append((row + direction, col + dc))
        
        # Knight movement logic
        elif self.piece_type == PieceType.KNIGHT:
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                           (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] is None or board[r][c].color != self.color:
                        moves.append((r, c))
        
        # Bishop, Rook, and Queen movement logic
        elif self.piece_type in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
            directions = []
            
            # Bishop moves diagonally
            if self.piece_type in [PieceType.BISHOP, PieceType.QUEEN]:
                directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
            
            # Rook moves horizontally and vertically
            if self.piece_type in [PieceType.ROOK, PieceType.QUEEN]:
                directions.extend([(-1, 0), (0, -1), (0, 1), (1, 0)])
            
            for dr, dc in directions:
                for i in range(1, BOARD_SIZE):
                    r, c = row + i*dr, col + i*dc
                    
                    # Check if position is on the board
                    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                        break
                    
                    # Empty square - add move and continue
                    if board[r][c] is None:
                        moves.append((r, c))
                    # Piece of opposite color - add move and stop
                    elif board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    # Piece of same color - stop
                    else:
                        break
        
        # King movement logic
        elif self.piece_type == PieceType.KING:
            king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), 
                         (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in king_moves:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] is None or board[r][c].color != self.color:
                        moves.append((r, c))
            
            # Castling
            if not self.has_moved:
                # Kingside castling
                if (col + 3 < BOARD_SIZE and 
                    board[row][col + 3] is not None and
                    board[row][col + 3].piece_type == PieceType.ROOK and
                    board[row][col + 3].color == self.color and
                    not board[row][col + 3].has_moved and
                    board[row][col + 1] is None and
                    board[row][col + 2] is None):
                    moves.append((row, col + 2))  # Kingside castle
                
                # Queenside castling
                if (col - 4 >= 0 and
                    board[row][col - 4] is not None and
                    board[row][col - 4].piece_type == PieceType.ROOK and
                    board[row][col - 4].color == self.color and
                    not board[row][col - 4].has_moved and
                    board[row][col - 1] is None and
                    board[row][col - 2] is None and
                    board[row][col - 3] is None):
                    moves.append((row, col - 2))  # Queenside castle
        
        return moves

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.load_images()
        self.reset_game()

    def load_images(self):
        piece_names = ["wp", "wn", "wb", "wr", "wq", "wk", "bp", "bn", "bb", "br", "bq", "bk"]
        for name in piece_names:
            try:
                # Try to load from standard chess piece images
                img = pygame.image.load(f"chess_pieces/{name}.png")
                IMAGES[name] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            except:
                # If image loading fails, create a simple representation
                color = WHITE if name[0] == 'w' else BLACK
                IMAGES[name] = self.create_simple_piece(name[1], color)
    
    def create_simple_piece(self, piece_type, color):
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        
        # Draw a circle as the base of the piece
        pygame.draw.circle(
            surface, 
            color, 
            (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
            SQUARE_SIZE // 3
        )
        
        # Add a letter to identify the piece
        font = pygame.font.SysFont('Arial', SQUARE_SIZE // 2)
        letter = piece_type.upper()
        text = font.render(letter, True, WHITE if color == BLACK else BLACK)
        text_rect = text.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
        surface.blit(text, text_rect)
        
        return surface
    
    def reset_game(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PieceColor.WHITE
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.in_check = {PieceColor.WHITE: False, PieceColor.BLACK: False}
        self.kings = {PieceColor.WHITE: None, PieceColor.BLACK: None}
        
        # Set up pawns
        for col in range(BOARD_SIZE):
            self.board[1][col] = Piece(PieceType.PAWN, PieceColor.BLACK, (1, col))
            self.board[6][col] = Piece(PieceType.PAWN, PieceColor.WHITE, (6, col))
        
        # Set up other pieces
        piece_order = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]
        
        for col in range(BOARD_SIZE):
            # Black pieces
            self.board[0][col] = Piece(piece_order[col], PieceColor.BLACK, (0, col))
            # White pieces
            self.board[7][col] = Piece(piece_order[col], PieceColor.WHITE, (7, col))
            
            # Store kings for check detection
            if piece_order[col] == PieceType.KING:
                self.kings[PieceColor.BLACK] = self.board[0][col]
                self.kings[PieceColor.WHITE] = self.board[7][col]
    
    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw pieces
                piece = self.board[row][col]
                if piece:
                    self.screen.blit(IMAGES[piece.get_image_key()], (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Highlight selected piece
        if self.selected_piece:
            row, col = self.selected_piece.position
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill(HIGHLIGHT)
            self.screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            
            # Highlight possible moves
            for move_row, move_col in self.valid_moves:
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(MOVE_HIGHLIGHT)
                self.screen.blit(highlight, (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE))
        
        # Highlight king in check
        for color, is_in_check in self.in_check.items():
            if is_in_check and self.kings[color]:
                king = self.kings[color]
                row, col = king.position
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(CHECK_HIGHLIGHT)
                self.screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        pygame.display.flip()
    
    def is_in_check(self, color):
        king = self.kings[color]
        if not king:
            return False
        
        king_pos = king.position
        
        # Check all opponent pieces to see if they can attack the king
        opponent_color = PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    # Check if king's position is in this piece's possible moves
                    if king_pos in piece.get_possible_moves(self.board):
                        return True
        
        return False
    
    def would_be_in_check(self, piece, move):
        # Make a copy of the board
        temp_board = [row[:] for row in self.board]
        old_row, old_col = piece.position
        new_row, new_col = move
        
        # Simulate the move
        temp_board[new_row][new_col] = piece
        temp_board[old_row][old_col] = None
        
        # Check if king would be in check
        king = self.kings[piece.color]
        king_pos = (new_row, new_col) if piece == king else king.position
        
        # Check all opponent pieces to see if they can attack the king
        opponent_color = PieceColor.BLACK if piece.color == PieceColor.WHITE else PieceColor.WHITE
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = temp_board[r][c]
                if p and p.color == opponent_color:
                    moves = []
                    
                    # Calculate possible moves for the opponent piece
                    # Using a simplified version to avoid recursion
                    if p.piece_type == PieceType.PAWN:
                        dir_val = -1 if p.color == PieceColor.WHITE else 1
                        # Captures
                        for dc in [-1, 1]:
                            capture_pos = (r + dir_val, c + dc)
                            if 0 <= capture_pos[0] < BOARD_SIZE and 0 <= capture_pos[1] < BOARD_SIZE:
                                moves.append(capture_pos)
                    elif p.piece_type == PieceType.KNIGHT:
                        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                                       (1, -2), (1, 2), (2, -1), (2, 1)]
                        for dr, dc in knight_moves:
                            pos = (r + dr, c + dc)
                            if 0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE:
                                moves.append(pos)
                    elif p.piece_type in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
                        directions = []
                        if p.piece_type in [PieceType.BISHOP, PieceType.QUEEN]:
                            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
                        if p.piece_type in [PieceType.ROOK, PieceType.QUEEN]:
                            directions.extend([(-1, 0), (0, -1), (0, 1), (1, 0)])
                        
                        for dr, dc in directions:
                            for i in range(1, BOARD_SIZE):
                                pos = (r + i*dr, c + i*dc)
                                if not (0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE):
                                    break
                                moves.append(pos)
                                if temp_board[pos[0]][pos[1]] is not None:
                                    break
                    elif p.piece_type == PieceType.KING:
                        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), 
                                     (0, 1), (1, -1), (1, 0), (1, 1)]
                        for dr, dc in king_moves:
                            pos = (r + dr, c + dc)
                            if 0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE:
                                moves.append(pos)
                    
                    # Check if king's position is in this piece's possible moves
                    if king_pos in moves:
                        return True
        
        return False
    
    def filter_moves_for_check(self, piece, moves):
        """Filter moves that would put the king in check"""
        valid_moves = []
        for move in moves:
            if not self.would_be_in_check(piece, move):
                valid_moves.append(move)
        return valid_moves
    
    def is_checkmate(self, color):
        """Check if a player is in checkmate"""
        # If not in check, can't be checkmate
        if not self.in_check[color]:
            return False
        
        # Check if any piece can make a move that gets out of check
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    possible_moves = piece.get_possible_moves(self.board)
                    valid_moves = self.filter_moves_for_check(piece, possible_moves)
                    if valid_moves:
                        return False  # At least one legal move exists
        
        return True  # No legal moves and in check = checkmate
    
    def is_stalemate(self, color):
        """Check if a player is in stalemate (not in check but no legal moves)"""
        # If in check, can't be stalemate
        if self.in_check[color]:
            return False
        
        # Check if any piece can make a valid move
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    possible_moves = piece.get_possible_moves(self.board)
                    valid_moves = self.filter_moves_for_check(piece, possible_moves)
                    if valid_moves:
                        return False  # At least one legal move exists
        
        return True  # No legal moves and not in check = stalemate
    
    def handle_click(self, pos):
        if self.game_over:
            return
            
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        # Check if position is on the board
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        
        piece = self.board[row][col]
        
        # If piece selected and click is a valid move, move the piece
        if self.selected_piece and (row, col) in self.valid_moves:
            self.move_piece(self.selected_piece, (row, col))
            self.selected_piece = None
            self.valid_moves = []
            return
        
        # If selected piece and clicked on another piece of same color, change selection
        if piece and piece.color == self.current_player:
            self.selected_piece = piece
            possible_moves = piece.get_possible_moves(self.board)
            self.valid_moves = self.filter_moves_for_check(piece, possible_moves)
        else:
            self.selected_piece = None
            self.valid_moves = []
    
    def move_piece(self, piece, new_position):
        old_row, old_col = piece.position
        new_row, new_col = new_position
        
        # Handle castling
        if piece.piece_type == PieceType.KING and abs(old_col - new_col) > 1:
            # Kingside castling
            if new_col > old_col:
                rook = self.board[old_row][7]  # Rook at h-file
                self.board[old_row][5] = rook  # Move rook to f-file
                self.board[old_row][7] = None
                rook.position = (old_row, 5)
                rook.has_moved = True
            # Queenside castling
            else:
                rook = self.board[old_row][0]  # Rook at a-file
                self.board[old_row][3] = rook  # Move rook to d-file
                self.board[old_row][0] = None
                rook.position = (old_row, 3)
                rook.has_moved = True
        
        # Update the board
        self.board[new_row][new_col] = piece
        self.board[old_row][old_col] = None
        piece.position = new_position
        piece.has_moved = True
        
        # Check for pawn promotion at end of board
        if piece.piece_type == PieceType.PAWN:
            if (piece.color == PieceColor.WHITE and new_row == 0) or \
               (piece.color == PieceColor.BLACK and new_row == 7):
                self.board[new_row][new_col] = Piece(PieceType.QUEEN, piece.color, new_position)
        
        # Switch players
        self.current_player = PieceColor.BLACK if self.current_player == PieceColor.WHITE else PieceColor.WHITE
        
        # Update check status
        self.in_check[PieceColor.WHITE] = self.is_in_check(PieceColor.WHITE)
        self.in_check[PieceColor.BLACK] = self.is_in_check(PieceColor.BLACK)
        
        # Check for checkmate or stalemate
        if self.is_checkmate(self.current_player):
            self.game_over = True
            print("Checkmate!")
        elif self.is_stalemate(self.current_player):
            self.game_over = True
            print("Stalemate!")
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse click
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    # Reset the game if 'R' is pressed
                    if event.key == pygame.K_r:
                        self.reset_game()
            
            # Draw the game
            self.draw_board()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Create and run the game
if __name__ == "__main__":
    game = ChessGame()
    game.run()