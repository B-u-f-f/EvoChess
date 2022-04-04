import chess
import evalfuction as ef

from dataclasses import dataclass

@dataclass
class EngineMove:
    move: chess.Move
    eval: float 

class NegaSearch:
    def __init__(self, maxDepth: int, evaluation: ef.EvalFunc) -> None:
        self.maxDepth: int = maxDepth
        self.evaluation: ef.EvalFunc = evaluation


    def search(self, board: chess.Board) -> EngineMove:
        return NegaSearch.auxSearch(board, self.evaluation, self.maxDepth)

    
    @staticmethod
    def auxSearch(board: chess.Board, evaluation: ef.EvalFunc, depth: int) -> EngineMove:
        
        depth -= 1
        
        moves = []

        for move in board.legal_moves:
            
            board.push(move)

            if (depth != 0):
                em = NegaSearch.auxSearch(board, evaluation, depth)

                moves.append(EngineMove(move, -1.0 * em.eval))
            else:
                moves.append(EngineMove(move, evaluation.eval(board)))
            
            print(board)
            print(board.turn, " ", moves[-1].eval)

            board.pop()
        
        return max(moves, key = lambda em: em.eval)

