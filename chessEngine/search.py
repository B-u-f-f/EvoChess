import chess
import evalfuction as ef

import tqdm
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
        return NegaSearch.auxSearch(board, self.evaluation, self.maxDepth, float('-inf'), float('inf'))

    
    @staticmethod
    def auxSearch(board: chess.Board, evaluation: ef.EvalFunc, depth: int, 
            alpha: float, beta: float) -> EngineMove:
         
        bestMove = None
        
        move = None
        if(not bool(board.legal_moves)):
            if(board.is_checkmate()):
                return EngineMove(None, -10000) 
            
            elif(board.is_stalemate()):
                return EngineMove(None, 0)

        for move in board.legal_moves:
            
            board.push(move)

            if (depth != 0):
                em = NegaSearch.auxSearch(board, evaluation, depth - 1, -beta, -alpha)

                move = EngineMove(move, -1.0 * em.eval)
            else:
                move = EngineMove(move, evaluation.eval(board))
            
            board.pop()

            
            if(bestMove == None):
                bestMove = move
            elif(move.eval > bestMove.eval):
                bestMove.eval = move.eval

            print(board.turn, " ", bestMove.eval)
            if(bestMove.eval >= alpha):
                alpha = bestMove.eval

            if(alpha >= beta):
                return EngineMove(None, alpha) 


        
        return bestMove 
