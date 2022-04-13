import chess
import evalfuction as ef
import search as s
from collections import defaultdict
import csv



class Engine:
    def __init__(self, depth):
        self.ef = ef.EvalFunc()
        self.ns = s.NegaSearch(depth, self.ef)
    
    def setEvaluationParameters(self, value):
        self.ef = ef.EvalFunc(value)

    def printeval(self, fen: str):
        board = chess.Board(fen)
        
        print(board)
        self.ns.search(board)
        print(board.san(self.ns.bestMove))
        board.push(self.ns.bestMove)
        print("\n")
        print(board)
    
    def findmoves(self, fens):
        out = []
        for i in range(len(fens)):
            out.append(self.bestmove(fens[i]))

            #print(f'fen evaluated: {i}/{len(fens)}')

        return out
    
    def bestmove(self, fen):
        board = chess.Board(fen)
        self.ns.search(board)
        return board.san(self.ns.bestMove)

if __name__ == '__main__':
    e = Engine(6)

    e.printeval('2r4r/1bn1qpk1/p3p2p/1p1pP2R/3N1QP1/8/PPP3BP/3R2K1 w - - 1 28')