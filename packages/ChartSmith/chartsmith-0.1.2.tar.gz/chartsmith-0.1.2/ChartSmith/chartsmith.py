import matplotlib.pyplot as plt
import seaborn as sns


class ChartSmith:
    def __init__(self, style='tableau-colorblind10'):
        """
        Initialize the Visualizer with a style.
        param style: The style to use for the plots. Default is 'tableau-colorblind10'.
        """
        available_styles = plt.style.available
        if style in available_styles:
            plt.style.use(style)
        else:
            sns.set_theme()
            print(f"'{style}' style not found, using Seaborn theme instead.")
        self.style = style

    def line_plot(self, x, y, title='', xlabel='', ylabel=''):
        """
        Create a line plot.
        param x: Data for x-axis.
        param y: Data for y-axis.
        param title: Title of the plot.
        param xlabel: Label for the x-axis.
        param ylabel: Label for the y-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='#1f77b4')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True)
        plt.show()

    def bar_plot(self, x, y, title='', xlabel='', ylabel=''):
        """
        Create a bar plot.
        param x: Data for x-axis.
        param y: Data for y-axis.
        param title: Title of the plot.
        param xlabel: Label for the x-axis.
        param ylabel: Label for the y-axis.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x=x, y=y, palette='colorblind')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True)
        plt.show()

    def scatter_plot(self, x, y, title='', xlabel='', ylabel=''):
        """
        Create a scatter plot.
        param x: Data for x-axis.
        param y: Data for y-axis.
        param title: Title of the plot.
        param xlabel: Label for the x-axis.
        param ylabel: Label for the y-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='#1f77b4', edgecolor='w', s=100)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True)
        plt.show()
