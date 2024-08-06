import unittest
from ChartSmith import ChartSmith

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.viz = ChartSmith()

    def test_line_plot(self):
        try:
            self.viz.line_plot([1, 2, 3], [4, 5, 6], title='Test', xlabel='X', ylabel='Y')
        except Exception as e:
            self.fail(f"line_plot raised an exception {e}")

    def test_bar_plot(self):
        try:
            self.viz.bar_plot(['A', 'B', 'C'], [1, 2, 3], title='Test', xlabel='X', ylabel='Y')
        except Exception as e:
            self.fail(f"bar_plot raised an exception {e}")

    def test_scatter_plot(self):
        try:
            self.viz.scatter_plot([1, 2, 3], [4, 5, 6], title='Test Scatter', xlabel='X', ylabel='Y')
        except Exception as e:
            self.fail(f"scatter_plot raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
