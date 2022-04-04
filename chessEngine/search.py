import chess
import evalfuction as ef


class NegaSearch:
    def __init__(self, maxDepth: int, evaluation: ef.EvalFunc) -> None:
        self.maxDepth: int = maxDepth
        self.evaluation: ef.EvalFunc = evaluation


    def search(self, board: chess.Board) -> chess.Move:
        pass

    
    @staticmethod
    def _search(board: chess.Board, evaluation: ef.EvalFunc, depth: int) -> chess.Move:
        
        depth -= 1
        
        moves = []

        for move in board.legal_moves:
            print(move)
            
            board.push(move)

            if (depth != 0):
                t = NegaSearch._search(board, evaluation, depth)
                t[1] *= -1.0

                moves.append(t)
            else:
                moves.append((move, evaluation.eval(board)))

            board.pop()
        
        return max(moves, key = lambda m, v: v)

