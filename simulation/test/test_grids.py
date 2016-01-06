import unittest

from simulation.test.grids import HugeGrid, EmptyGrid, ScoreOnOddXGrid
from simulation.test.test_world_map import TestGrid
from simulation.world_map import WorldMap, Grid


class TestInfiniteGrid(unittest.TestCase, TestGrid):
    def setUp(self):
        self.grid = HugeGrid()


class TestEmptyGrid(unittest.TestCase, TestGrid):
    def setUp(self):
        self.grid = EmptyGrid()


class TestScoreOnOddXGrid(unittest.TestCase, TestGrid):
    def setUp(self):
        self.grid = ScoreOnOddXGrid()


class TestGridImpl(unittest.TestCase, TestGrid):
    def setUp(self):
        self.grid = Grid(5, 9)