from simulation import world_map
from simulation.location import Location


class HugeGrid(object):
    def __init__(self):
        self.min_x, self.max_x = self.min_y, self.max_y = -999999, 999999
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

    def get_cell(self, location):
        assert self.contains_cell(location)
        return world_map.Cell(location)

    def contains_cell(self, location):
        return (self.min_x <= location.x < self.max_x) and (self.min_y <= location.y < self.max_y)


class EmptyGrid(world_map.WorldMap):
    def __init__(self):
        self.min_x = self.max_x = self.min_y = self.max_y = 0
        self.width = self.height = 0

    def get_cell(self, location):
        raise AssertionError

    def contains_cell(self, location):
        return False


class ScoreOnOddXGrid(HugeGrid):
    def get_cell(self, location):
        assert self.contains_cell(location)
        if location.x % 2 == 0:
            return world_map.Cell(location)
        else:
            return world_map.Cell(location, habitable=True, generates_score=True)
