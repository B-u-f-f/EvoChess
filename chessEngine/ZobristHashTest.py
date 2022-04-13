import unittest
from search import ZobristHash


class ZobristHashTest(unittest.TestCase):
    def setUp(self) -> None:
        self.z = ZobristHash()
        self.i = self.z.getInitalZobristKey()

    def castling(self):
        pass