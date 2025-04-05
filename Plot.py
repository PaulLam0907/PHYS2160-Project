"""
Plot.py

Plot a graph from given data with matplotlib
Support multi-plot on same graph

Written by S. P. Lam
"""

import matplotlib.pyplot as plt


class Plot:
    
    def __init__(self,
                 curve_data,
                 x_label = "x",
                 y_label = "y",
                 title = "",
                 curve_label = (),
                 x_ticks = (),
                 y_ticks = (),
                 x_ticks_label = (),
                 y_ticks_label = (),
                 grid = False):
        """
        Plot graph using given dataset
        
        Usage:
        f1 = [[1, 2, 3], [1, 2, 3]]
        f2 = [[1, 2, 3], [2, 3, 4]]
        graph = Plot([f1, f2], curve_label = ["y=x", "y=x+1"])
        graph()  # plot the graph
        
        :param curve_data: 3D array dataset containing data points for each graph e.g. [[ [graph1_x], [graph1_y] ], [ [graph2_x], [graph2_y] ]]
        :param x_label: (str) label for x-axis
        :param y_label: (str) label for y-axis
        :param title: (str) title for the plotted graph
        :param curve_label: (list) label (legend) for the curve(s)
        :param x_ticks: (list) labeling tick marks for x-axis
        :param y_ticks: (list) labeling tick marks for y-axis
        :param x_ticks_label: (list) label the numerical ticks marks on x-axis
        :param y_ticks_label: (list) label the numerical ticks marks on y-axis
        :param grid: (bool) indicate the use of grid in the graph
        """
        self.curve_data = curve_data
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.curve_label = curve_label if curve_label else ["" for i in range(len(curve_data))]
        self.x_ticks = x_ticks
        self.y_ticks = y_ticks
        self.x_ticks_label = x_ticks_label
        self.y_ticks_label = y_ticks_label
        self.grid = grid
        
        self._plot()
    
    def _plot(self):
        
        for curve, curve_label in zip(self.curve_data, self.curve_label):
            # subplot each curve one by one
            x = curve[0]
            y = curve[1]
            plt.plot(x, y, label = curve_label)
        
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.legend()
        if self.x_ticks:
            plt.xticks(self.x_ticks, labels = self.x_ticks_label)
        if self.y_ticks:
            plt.yticks(self.y_ticks, labels = self.y_ticks_label)
        if self.grid:
            plt.grid()
            
        plt.show()

