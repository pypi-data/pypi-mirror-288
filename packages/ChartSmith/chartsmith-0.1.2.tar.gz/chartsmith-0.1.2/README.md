# ChartSmith

ChartSmith is a Python package built on top of Matplotlib and Seaborn that creates well-formatted, well-labeled visualizations.

## Installation

```sh
pip install ChartSmith
```

## Usage

Here's how you can use the ChartSmith package:

```python
from ChartSmith import ChartSmith

# Create an instance of the ChartSmith class
viz = ChartSmith()

# Line plot
viz.line_plot(x=[1, 2, 3, 4], y=[10, 20, 25, 30], title='Line Plot', xlabel='X Axis', ylabel='Y Axis')

# Bar plot
viz.bar_plot(x=['A', 'B', 'C', 'D'], y=[10, 20, 25, 30], title='Bar Plot', xlabel='Categories', ylabel='Values')

# Scatter plot
viz.scatter_plot(x=[1, 2, 3, 4], y=[10, 20, 25, 30], title='Scatter Plot', xlabel='X Axis', ylabel='Y Axis')
```

## License
This project is licensed under the MIT License - see the LICENSE.txt file for details.
