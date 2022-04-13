import chess
import evalfuction as ef
import utility as u

import random as r
import typing as t
from dataclasses import dataclass
import enum

class ZobristHash:

    def __init__(self) -> None:
        self.pieceSquareHash = {}
        self.blackTurnHash = None
        self.castlingRightsHash = {} 
        self.passantFileHash = {}

        self.randomNumbersUsed = []

        self._genRandomArray()

    def _genRandomArray(self) -> None:
        
        # (square, color, piece)
        for s in chess.SQUARES:
            for c in [chess.WHITE, chess.BLACK]:
                for p in chess.PIECE_TYPES:
                    self.pieceSquareHash[(s, c, p)] = self._getRandom()

        self.blackTurnHash = self._getRandom()

        # (white kingside, white queenside, black kingside, black queenside)
        for i in range(0, 16):
            self.castlingRightsHash[i] = self._getRandom()

        for f in range(0, 8):
            self.passantFileHash[f] = self._getRandom()

    def getInitalZobristKey(self) -> int:
        key = 0
        
        # white pawns
        key ^= self.pieceSquareHash[(chess.A2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.B2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.C2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.D2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.E2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.F2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.G2, chess.WHITE, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.H2, chess.WHITE, chess.PAWN)]

        # white pieces
        key ^= self.pieceSquareHash[(chess.A1, chess.WHITE, chess.ROOK)]
        key ^= self.pieceSquareHash[(chess.B1, chess.WHITE, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.C1, chess.WHITE, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.D1, chess.WHITE, chess.QUEEN)]
        key ^= self.pieceSquareHash[(chess.E1, chess.WHITE, chess.KING)]
        key ^= self.pieceSquareHash[(chess.F1, chess.WHITE, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.G1, chess.WHITE, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.H1, chess.WHITE, chess.ROOK)]


        # black pawns
        key ^= self.pieceSquareHash[(chess.A7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.B7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.C7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.D7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.E7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.F7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.G7, chess.BLACK, chess.PAWN)]
        key ^= self.pieceSquareHash[(chess.H7, chess.BLACK, chess.PAWN)]

        # black pieces
        key ^= self.pieceSquareHash[(chess.A8, chess.BLACK, chess.ROOK)]
        key ^= self.pieceSquareHash[(chess.B8, chess.BLACK, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.C8, chess.BLACK, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.D8, chess.BLACK, chess.QUEEN)]
        key ^= self.pieceSquareHash[(chess.E8, chess.BLACK, chess.KING)]
        key ^= self.pieceSquareHash[(chess.F8, chess.BLACK, chess.BISHOP)]
        key ^= self.pieceSquareHash[(chess.G8, chess.BLACK, chess.KNIGHT)]
        key ^= self.pieceSquareHash[(chess.H8, chess.BLACK, chess.ROOK)]

        # all sides castling possible
        key ^= self.castlingRightsHash[15]

        return key

    def _getCastlingRightsAfterMoveHash(self, board: chess.Board, move: chess.Move) -> int:
        beforeMoveCastleID: int = self._getCastleID(board)
        board.push(move)
        afterMoveCastleID: int = self._getCastleID(board)
        board.pop()

        return self.castlingRightsHash[beforeMoveCastleID] ^ \
        self.castlingRightsHash[afterMoveCastleID]

    def _getPieceMoveHash(self, board: chess.Board, move: chess.Move) -> int:
        fromSquare: chess.Square = move.from_square
        toSquare: chess.Square = move.to_square

        movedPiece = board.piece_at(fromSquare)

        # None if no piece is captured
        capturedPiece = board.piece_at(toSquare) 

        if(capturedPiece == None):
            return \
               self.pieceSquareHash[(fromSquare, movedPiece.color, movedPiece.piece_type)]\
            ^  self.pieceSquareHash[(toSquare, movedPiece.color, movedPiece.piece_type)] 

        return \
           self.pieceSquareHash[(fromSquare, movedPiece.color, movedPiece.piece_type)]\
        ^  self.pieceSquareHash[(toSquare, movedPiece.color, movedPiece.piece_type)]\
        ^  self.pieceSquareHash[(toSquare, capturedPiece.color, capturedPiece.piece_type)]
 
    def _getEnPassantFileHash(self, board: chess.Board, move: chess.Move) -> int:
        beforeEnPassantFiles = self._getEnPassantFiles(board)
        board.push(move)
        afterEnPassantFiles = self._getEnPassantFiles(board)
        board.pop()

        finalHash = 0
        for f in (beforeEnPassantFiles + afterEnPassantFiles):
            finalHash ^= self.passantFileHash[f]

        return finalHash 

    def makeMove(self, board: chess.Board, move: chess.Move, key: int) -> int:
        key ^= self._getCastlingRightsAfterMoveHash(board, move) 
        ## print(f'After castling {key}')
            
        ## piece move
        key ^= self._getPieceMoveHash(board, move) 
        
        ## turn
        key ^= self.blackTurnHash 
        ## print(f'after turn {key} {self.blackTurnHash}')

        ## en passant
        key ^= self._getEnPassantFiles(board, move)

        ## print(f'after en passant {key}')
        return key

    def hashOfPosition(self, board: chess.Board) -> int:
        castlingHash: int = self.castlingRightsHash[self._getCastleID(board)] 

        pieceMap: t.Dict[chess.Square, chess.Piece] =  board.piece_map()

        piecePositionHash: int = 0
        for s, p in pieceMap.items():

            piecePositionHash ^= self.pieceSquareHash[(
                s, p.color, p.piece_type 
            )]

        enPassantHash = 0
        for f in self._getEnPassantFiles(board):
            enPassantHash ^= self.passantFileHash[f]               

        return castlingHash ^ piecePositionHash ^ enPassantHash 
    
    def _getEnPassantFiles(self, board: chess.Board) -> t.List[int]:
        legalMoves = board.legal_moves

        return [
            chess.square_file(move.to_square) 
            for move in legalMoves 
                if (board.is_en_passant(move))
            ]

    def _getCastleID(self, board: chess.Board) -> int:
        wk = int(board.has_kingside_castling_rights(chess.WHITE))
        wq = int(board.has_queenside_castling_rights(chess.WHITE))
        bk = int(board.has_kingside_castling_rights(chess.BLACK))
        bq = int(board.has_queenside_castling_rights(chess.BLACK))

        return u.listToBinary([wk, wq, bk, bq]) 

    def _getRandom(self) -> int: 
        num = r.getrandbits(64)
        while(num in self.randomNumbersUsed):
            num = r.getrandbits(64)

        self.randomNumbersUsed.append(num)
        return num 

@enum.unique
class NodeType(enum.Enum):
    CUT_NODE = enum.auto()
    ALL_NODE = enum.auto()
    PV_NODE = enum.auto()

@dataclass
class TTEntry:
    value: float 
    depth: int
    nodeType: NodeType


class TranspositionTable:
    def __init__(self) -> None:
        self.table: t.Dict[int, TTEntry] = {}

    def isInTable(self, hash:int) -> bool:
        return hash in self.table

    def add(self, hash: int, value: float, depth: int, nodeType: NodeType):
        self.table[hash] = TTEntry(value = value, depth = depth, nodeType = nodeType)

    def get(self, hash: int) -> t.Union[TTEntry, None]:
        return self.table.get(hash, None) 

class NegaSearch:
    def __init__(self, maxDepth: int, evaluation: ef.EvalFunc) -> None:
        self.maxDepth: int = maxDepth
        self.evaluation: ef.EvalFunc = evaluation


    def search(self, board: chess.Board) -> None:
        self.bestMove = None
        self.auxSearch(board, self.evaluation, self.maxDepth, float('-inf'), float('inf'))

    
    def auxSearch(self, board: chess.Board, evaluation: ef.EvalFunc, depth: int, 
            alpha: float, beta: float) -> float:
        
        if(depth == 0):
            return evaluation.testEval(board)

        if(board.legal_moves.count() == 0):
            if(board.is_checkmate()):
                return float('inf') if board.outcome().winner == board.turn else float('-inf') 
            
            return 0.0

        
        bestMove = None
        moveEval = float('-inf')
        bestEval = float('-inf')
        for move in board.legal_moves:
            if(depth == self.maxDepth):
                print(move)
            
            board.push(move)
            moveEval = -self.auxSearch(board, evaluation, depth - 1, -beta, -alpha) 
            board.pop()

            if(moveEval > bestEval):
                bestEval = moveEval
                bestMove = move

            if bestEval > beta:
                return bestEval
            
            alpha = max(alpha, bestEval)

 
        if(depth == self.maxDepth):
            self.bestMove = bestMove

        return bestEval 


if __name__ == '__main__':
    b = chess.Board()
    m = chess.Move.from_uci('e2e4')
    m2 = chess.Move.from_uci('d2d4')

    z = ZobristHash()
    i = z.getInitalZobristKey()
    print(i, m)
    print(b)
    h1 = z.getZobristHashKey(b, m, i)
    print("next")
    print(i, m2)
    print(b)
    h2 = z.getZobristHashKey(b, m2, i)


    print(i, h1, h2, h1 == h2)