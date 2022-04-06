import chess
import evalfuction as ef
import search as s


class Engine:
    def __init__(self):
        self.ef = ef.EvalFunc()
        self.ns = s.NegaSearch(4, self.ef)


    def printeval(self, fen: str):
        board = chess.Board(fen)
        
        print(board)
        m = self.ns.search(board).move

        board.push(m)
        print("\n")
        print(board)


if __name__ == '__main__':
    e = Engine()
    e.printeval('8/4R3/1P3pk1/3N4/6K1/2p5/1r6/8 w - - 0 48');

