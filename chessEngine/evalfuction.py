import chess

class EvalFunc:
    
    def __init__(self, color) -> None:
        self.piecevalue = {
                chess.PAWN: 1.0, 
                chess.BISHOP: 3.0, 
                chess.KNIGHT: 2.0, 
                chess.QUEEN: 9.0,
                chess.ROOK: 5.0,
                chess.KING: 100.0
                }

        self.color = color 

    def eval(self, board : chess.Board) -> float:
        pass
