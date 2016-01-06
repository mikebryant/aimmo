from itertools import product, chain

from simulation.location import Location

ORIGIN = Location(0, 0)


def _get_x_values_inbounds(grid):
    point_sample = [grid.min_x, grid.min_x + 1, grid.max_x - 1]
    return set(x for x in point_sample if grid.min_x <= x < grid.max_x)


def _get_y_values_inbounds(grid):
    point_sample = [grid.min_y, grid.min_y + 1, grid.max_y - 1]
    return set(y for y in point_sample if grid.min_y <= y < grid.max_y)


def _get_x_values_outbounds(grid):
    return [grid.min_x - 1, grid.max_x]


def _get_y_values_outbounds(grid):
    return [grid.min_y - 1, grid.max_y]


class TestGrid(object):
    """
    This is an interface test. All implementations of Grid should pass these tests.
    Implementation tests should extend this class and unittest.TestCase
    """

    def setUp(self):
        # self.grid = Grid(1, 1)
        raise NotImplementedError()

    def test_contains_cell(self):

        if self.grid.contains_cell(ORIGIN):
            cell = self.grid.get_cell(ORIGIN)
            self.assertIsNotNone(cell)
            self.assertEqual(cell.location, ORIGIN)
        else:
            with self.assertRaises(AssertionError):
                self.grid.get_cell(ORIGIN)

    def test_width_and_height(self):
        self.assertGreaterEqual(self.grid.width, 0)
        self.assertGreaterEqual(self.grid.height, 0)

    def test_min_and_max(self):
        # max_x and max_y are not included in the range
        self.assertEqual(self.grid.width, self.grid.max_x - self.grid.min_x)
        self.assertEqual(self.grid.height, self.grid.max_y - self.grid.min_y)

    def test_inbound_cells(self):
        for x, y in product(_get_x_values_inbounds(self.grid), _get_y_values_inbounds(self.grid)):
            location = Location(x, y)
            self.assertTrue(self.grid.contains_cell(location), 'grid should contain ' + str(location))

            cell = self.grid.get_cell(location)
            self.assertIsNotNone(cell)
            self.assertEqual(cell.location, location)

    def test_outbound_cells(self):
        both_outbounds = product(_get_x_values_outbounds(self.grid), _get_y_values_outbounds(self.grid))
        x_outbounds = product(_get_x_values_outbounds(self.grid), _get_y_values_inbounds(self.grid))
        y_outbounds = product(_get_x_values_inbounds(self.grid), _get_y_values_outbounds(self.grid))

        for x, y in chain(both_outbounds, x_outbounds, y_outbounds):
            location = Location(x, y)
            self.assertFalse(self.grid.contains_cell(location))
            with self.assertRaises(AssertionError):
                self.grid.get_cell(location)

