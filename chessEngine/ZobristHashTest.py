import unittest
import chess
from search import ZobristHash


class ZobristHashTest(unittest.TestCase):
    def setUp(self):
        self.z = ZobristHash()
        self.i = self.z.getInitalZobristKey()

    # tests a position with castling rights vs 
    # same position without castling rights
    def testCastlingPositions(self):
        orgpos = chess.Board('rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w KQkq - 0 4')
        whiteNoCastle = chess.Board('rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w kq - 4 6')        
        blackNoCastle = chess.Board('rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w KQ - 4 6')
        whiteNoKing = chess.Board('rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w Qkq - 4 6')
        whiteNoQueen = chess.Board('rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w Kkq - 4 6') 
        blackNoKing = chess.Board('rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w KQk - 4 6')
        blackNoQueen = chess.Board('rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w KQq - 4 6')

        h1 = self.z.hashOfPosition(orgpos)
        h2 = self.z.hashOfPosition(whiteNoCastle)
        h3 = self.z.hashOfPosition(blackNoCastle)
        h4 = self.z.hashOfPosition(whiteNoKing)
        h5 = self.z.hashOfPosition(whiteNoQueen)
        h6 = self.z.hashOfPosition(blackNoKing)
        h7 = self.z.hashOfPosition(blackNoQueen)

        l = [h1, h2, h3, h4, h5, h6, h7]
        self.assertEqual(len(l), len(set(l))) 

    def testEnPassant(self):
        orgpos = chess.Board('rnbqk1nr/1p1pbpp1/8/p1pPp2p/P3P2P/8/1PP2PP1/RNBQKBNR w KQq c6 0 8')
        withoutEnPassant = chess.Board('rnbqk1nr/1p1pbpp1/8/p1pPp2p/P3P2P/8/1PP2PP1/RNBQKBNR w KQq - 4 10')

        h1 = self.z.hashOfPosition(orgpos)
        h2 = self.z.hashOfPosition(withoutEnPassant)

        self.assertNotEqual(h1, h2)


if __name__ == '__main__':
    unittest.main()
