import chess

class EvalFunc:
    
    def __init__(self) -> None:
        self.pieceValues = {
                chess.PAWN: 1.0, 
                chess.BISHOP: 3.0, 
                chess.KNIGHT: 2.0, 
                chess.QUEEN: 9.0,
                chess.ROOK: 5.0,
                chess.KING: 100.0
                }

    def eval(self, board : chess.Board) -> float:
        eval_score = 0.0
        
        # a dict of pieces currently on the board
        pieces = board.piece_map()
        
        # pieces -> Dict[chess.Square, chess.Piece]
        
        color = not board.turn

        for piece in pieces.values():
            if(piece.color == color):
                eval_score += self.pieceValues[piece.piece_type]
            else:
                eval_score -= self.pieceValues[piece.piece_type]
                
        return eval_score
