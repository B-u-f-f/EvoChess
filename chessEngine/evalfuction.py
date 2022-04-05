import chess
import unittest

import typing as t


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

    def _centerpawnCount(self, board: chess.Board, color: chess.Color) -> int:
        e4: chess.Piece = board.piece_at(chess.E4)
        e5: chess.Piece = board.piece_at(chess.E5)
        d4: chess.Piece = board.piece_at(chess.D4)
        d5: chess.Piece = board.piece_at(chess.D5)

        
        count: int = 0
        if e4 != None:
            count += e4.color == color

        if d4 != None:
            count += d4.color == color

        if e5 != None:
            count += e5.color == color

        if d5 != None:
            count += d5.color == color
        
        return count

    def _kingPawnShield(self, board: chess.Board, color: chess.Color) -> int:
        kposition : chess.Square = board.king(color)

        file : int = chess.square_file(kposition)
        rank : int = chess.square_rank(kposition)
            
        count : int = 0

        validRange = range(0, 8)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]: 
                if((file + i) in validRange and (rank + j) in validRange):
                    pos = chess.square(file + i, rank + j)
                    piece = board.piece_at(pos)   
                    
                    if(piece != None and piece.piece_type == chess.PAWN):
                        count += 1

                
        return count


    def _kingAttacked(self, board: chess.Board, color: chess.Color) -> t.List[int]: 
        kposition : chess.Square = board.king(color)
        file : int = chess.square_file(kposition)
        rank : int = chess.square_rank(kposition)
 
        eneColor : chess.Color = not chess.Color

        enePieces : t.List[int] = []

        validRange = range(0, 8)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]: 
                if((file + i) in validRange and (rank + j) in validRange):
                    pos = chess.square(file + i, rank + j)
                    piece = board.piece_at(pos)   
                    
                    if(piece != None and piece.color == eneColor):

                        enePieces.append(piece.piece_type)

        return enePieces 


    def _kingDefended(self, board: chess.Board, color: chess.Color) -> t.List[int]: 
        kposition : chess.Square = board.king(color)
        file : int = chess.square_file(kposition)
        rank : int = chess.square_rank(kposition)
 
        pieces : t.List[int] = []

        validRange = range(0, 8)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]: 
                if((file + i) in validRange and (rank + j) in validRange):
                    pos = chess.square(file + i, rank + j)
                    piece = board.piece_at(pos)   
                    
                    if(piece != None and piece.color == color and piece.piece_type != chess.KING):
                        pieces.append(piece.piece_type)

        return pieces 
    
    def _kingCastled(self, board: chess.Board, color: chess.Color) -> bool:
        pass

    def _bishopMob(self, board: chess.Board, color: chess.Color) -> t.List[int]:

        pieceDict = board.piece_map()

        # finding the bishop squares
        bSquares: t.Dict[chess.Square, int] = {} 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.BISHOP and p.color == color):
                bSquares[s] = 0
        

        for m in board.legal_moves:
            if(m.from_square in bSquares):
                bSquares[m.from_square] += 1 

        return bSquares.values()
    
    def _bishopOnLarge(self, board: chess.Board, color: chess.Color) -> t.List[bool]:
        whiteDiagSquares: t.List[chess.Move] = [
                chess.H1, chess.G2, chess.F3, chess.E4,
                chess.D5, chess.C6, chess.B7, chess.A8]
        
        blackDiagSquares: t.List[chess.Move] = [
                chess.A1, chess.B2, chess.C3, chess.D4,
                chess.E5, chess.F6, chess.G7, chess.H8
                ]

        
        whiteDiag = False
        blackDiag = False

        for s in whiteDiagSquares:
            piece: chess.Piece = board.piece_at(s)

            if(piece != None and piece.piece_type == chess.BISHOP and piece.color == color):
                whiteDiag = True

                break

        for s in blackDiagSquares:
            piece: chess.Piece = board.piece_at(s)

            if(piece != None and piece.piece_type == chess.BISHOP and piece.color == color):
                blackDiag = True

                break

        return [whiteDiag, blackDiag] 

    def _bishopPair(self, board: chess.Board, color: chess.Color) -> bool:
        pieceDict = board.piece_map()
        
        count = 0
        for s, p in pieceDict.items():
            if(p.piece_type == chess.BISHOP and p.color == color):
                count += 1
        
        return count == 2

    def _knightMob(self, board: chess.Board, color: chess.Color) -> t.List[int]:
        pieceDict = board.piece_map()

        # finding the bishop squares
        kSquares: t.Dict[chess.Square, int] = {} 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares[s] = 0
        

        for m in board.legal_moves:
            if(m.from_square in kSquares):
                kSquares[m.from_square] += 1 

        return kSquares.values()
    
    # number of supported knights
    def _knightSupport(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        validRange = range(8)
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            rank += -1 if color else +1

            for f in [file-1, file+1]:
                if(rank in validRange and f in validRange):
                    piece : chess.Piece = board.piece_at(chess.square(f, rank))

                    if(piece != None and piece.piece_type == chess.PAWN and piece.color == color):
                        count += 1
                        break

        return count 

    def _knightPeriphery0(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            #print(file, rank)
            if(file in [0, 7] or rank in [0, 7]):
                count += 1
        
        return count 


    def _knightPeriphery1(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            #print(file, rank)
            positions = list(zip([1] * 6, range(1, 7)))\
            + list(zip([6] * 6, range(1, 7)))\
            + list(zip(range(1, 7), [1] * 6))\
            + list(zip(range(1, 7), [6] * 6))


            if((file, rank) in positions):
                count += 1
        
        return count 

    def _knightPeriphery2(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            positions = list(zip([2] * 6, range(2, 6)))\
            + list(zip([5] * 6, range(2, 6)))\
            + list(zip(range(2, 6), [2] * 6))\
            + list(zip(range(2, 6), [5] * 6))


            if((file, rank) in positions):
                count += 1
        
        return count 

    def _knightPeriphery3(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        kSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.KNIGHT and p.color == color):
                kSquares.append(s)
        
        count = 0
        for s in kSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)
            
            if((file, rank) in [(3, 4), (4, 3), (3, 3), (4, 4)]):
                count += 1

        return count 

    def _isoPawn(self, board: chess.Board, color: chess.Color) -> int:
        pieceDict = board.piece_map()
        pSquares: t.List[chess.Square] = [] 
        for s, p in pieceDict.items():
            if(p.piece_type == chess.PAWN and p.color == color):
                pSquares.append(s)
        
        count = 0
        for s in pSquares:
            file : int = chess.square_file(s)
            rank : int = chess.square_rank(s)

            validRange = range(0, 8)
            flag = True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]: 
                    if(i == j == 0): 
                        continue

                    if((file + i) in validRange and (rank + j) in validRange):
                        p = board.piece_at(chess.square(file + i, rank + j))

                        if(p != None and p.piece_type == chess.PAWN and p.color == color):
                            flag = False
                
                if(not flag):
                    break

            if(flag):
                count += 1

        return count

    def _doubledPawn(self, board: chess.Board, color: chess.Color) -> int:
        pass

   


        
class EvalFuncTest(unittest.TestCase):

    def setUp(self):
        self.ef = EvalFunc()

    def testCenterPawnCount(self):
        b = chess.Board('4k3/8/8/3P4/4P3/8/8/4K3 w - - 0 1')

        bCount = self.ef._centerpawnCount(b, chess.BLACK)
        wCount = self.ef._centerpawnCount(b, chess.WHITE)

        self.assertEqual(bCount, 0)
        self.assertEqual(wCount, 2)

        b = chess.Board('4k3/8/8/3pP3/4P3/8/8/4K3 w - - 0 1')

        bCount = self.ef._centerpawnCount(b, chess.BLACK)
        wCount = self.ef._centerpawnCount(b, chess.WHITE)

        self.assertEqual(bCount, 1)
        self.assertEqual(wCount, 2)
    
    def testKingPawnShield(self):
        b = chess.Board("8/8/8/8/8/8/1P6/K7 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 1)

        b = chess.Board("8/8/8/4P3/2PK4/4P3/8/8 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 3)

        b = chess.Board("3K4/3P4/8/8/2P5/4P3/8/8 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 1)

        b = chess.Board("8/8/6P1/7K/2P4P/8/8/8 w - - 0 1")
        wCount = self.ef._kingPawnShield(b, chess.WHITE)

        self.assertEqual(wCount, 2)

    def testKingDefended(self):
        b = chess.Board('8/8/8/3bP3/2PK4/3RP3/8/8 w - - 0 1')

        pieces = self.ef._kingDefended(b, chess.WHITE)
        self.assertEqual([chess.PAWN, chess.ROOK, chess.PAWN, chess.PAWN], pieces)

    def testKingAttacked(self):
        b = chess.Board('8/8/8/3bP3/2PK4/3RP3/8/8 w - - 0 1')

        pieces = self.ef._kingAttacked(b, chess.WHITE)
        self.assertEqual([chess.BISHOP], pieces)

    def testBishopMob(self):
        b = chess.Board('3k4/8/8/4PB2/2PK4/3RP3/1B6/8 w - - 0 1')

        mob = self.ef._bishopMob(b, chess.WHITE)
        self.assertEqual(set(mob), set([4, 8]))

    def testBishopOnLarge(self):
        b = chess.Board('3k4/8/8/4P3/2PKB3/1B1RP3/8/8 w - - 0 1')
        res = self.ef._bishopOnLarge(b, chess.WHITE)
        self.assertEqual(res, [True, False])

        b = chess.Board('3k4/8/3B4/4P3/2PK4/3RP3/1B6/8 w - - 0 1')
        res = self.ef._bishopOnLarge(b, chess.WHITE)
        self.assertEqual(res, [False, True])

    
    def testBishopPair(self):
        b = chess.Board('3k4/8/8/4P3/2PKB3/1B1RP3/8/8 w - - 0 1')
        res = self.ef._bishopPair(b, chess.WHITE)
        self.assertEqual(res, True)

        b = chess.Board('3k4/8/8/4P3/2PKB3/1R1RP3/8/8 w - - 0 1')
        res = self.ef._bishopPair(b, chess.WHITE)
        self.assertEqual(res, False)

    def testKnightMob(self):
        b = chess.Board('3k4/8/8/4PN2/2PK4/3RP3/1N6/8 w - - 0 1')


        mob = self.ef._knightMob(b, chess.WHITE)
        self.assertEqual(set(mob), set([2, 6]))

    def testKnightSupport(self):
        b = chess.Board('3k4/8/8/5N2/8/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/8/5N2/6P1/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 1)

        b = chess.Board('3k4/8/8/5N2/6P1/8/1N6/P2K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/6P1/5N2/8/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.WHITE)
        self.assertEqual(mob, 0)


        b = chess.Board('3k4/4n3/6P1/2n2N2/8/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/6P1/2n2N1p/6n1/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 1)

        b = chess.Board('3k4/8/1p4P1/2n2N1p/6n1/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/4n3/4p1P1/2n2N2/2p5/P7/1N6/3K4 w - - 0 1')
        mob = self.ef._knightSupport(b, chess.BLACK)
        self.assertEqual(mob, 0)

    def testKnightPeriphery0(self):
        b = chess.Board('3k4/8/8/8/N6N/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/5N2/6P1/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k1N2/8/8/8/6P1/8/8/1N1K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('2nk4/8/8/8/2N2N2/7n/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery0(b, chess.WHITE)
        self.assertEqual(mob, 0)

    def testKnightPeriphery1(self):
        b = chess.Board('3k4/8/8/8/6N1/8/1N6/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/5N2/6P1/2N5/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/4N3/8/8/6P1/8/2N5/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/2n5/8/8/2N2N2/8/6n1/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery1(b, chess.WHITE)
        self.assertEqual(mob, 0)


    def testKnightPeriphery2(self):
        b = chess.Board('3k4/8/8/8/2N2N2/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/3N4/4N1P1/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/4N3/8/6P1/3N4/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/2n5/8/3NN3/5n2/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery2(b, chess.WHITE)
        self.assertEqual(mob, 0)

    def testKnightPeriphery3(self):
        b = chess.Board('3k4/8/8/3N4/4N3/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/2N5/8/8/6P1/8/5N2/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        self.assertEqual(mob, 0)

        b = chess.Board('3k4/8/8/4N3/3N2P1/8/8/3K4 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        self.assertEqual(mob, 2)

        b = chess.Board('3k4/8/8/3n4/4n3/1N6/8/3KN3 w - - 0 1')
        mob = self.ef._knightPeriphery3(b, chess.WHITE)
        self.assertEqual(mob, 0)

    def testIsoPawn(self):
        b = chess.Board('3k4/8/8/8/3P2P1/1P2P3/8/3K4 w - - 0 1')
        mob = self.ef._isoPawn(b, chess.WHITE)
        # print(mob)
        self.assertEqual(mob, 2)



if __name__ == '__main__':
    unittest.main()

