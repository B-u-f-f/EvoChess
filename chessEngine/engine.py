import chess
import evalfuction as ef
import search as s


class Engine:
    def __init__(self):
        self.ef = ef.EvalFunc()
        self.ns = s.NegaSearch(2, self.ef)


    def printeval(self, fen: str):
        board = chess.Board(fen)
        
        print(board)
        m = self.ns.search(board).move

        board.push(m)
        print("\n")
        print(board)


if __name__ == '__main__':
    e = Engine()
    e.printeval('3k4/8/8/8/8/8/3Pn3/3K4 w - - 0 1');

