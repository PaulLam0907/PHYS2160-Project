"""
Plot.py

Plot a graph from given data with matplotlib
Support multi-plot on same graph

Written by S. P. Lam
"""

import matplotlib.pyplot as plt


class Figure:
    
    def __init__(self, row = 1, col = 1):
        """
        Plot graph using given dataset
        Support repeat plotting for the same Figure() class
        
        Usage:
        f1 = [[1, 2, 3], [1, 2, 3]]
        f2 = [[1, 2, 3], [2, 3, 4]]
        fig = Figure(row = 1, col = 1)  # define figure with dimension for the figure window
        fig.add_graph([f1, f2], label = ["y=x", "y=x+1"])  # plot curves with label
        fig.set_x_label("x")  # x-axis label
        fig.set_y_label("y")  # y-axis label
        fig.set_axes_title("axes title")  # axes title
        fig.set_fig_title("figure title")  # figure title
        fig.grid()  # turn on grid lines
        fig.plot()  # show the plotted graph
        
        :param row: number of rows of axes in the figure
        :param col: number of columns of axes in the figure
        """
        self.figure = plt.figure()
        self.fig_dim = [row, col]
        self.axes_list = []
        self.curve_data = {1: []}
        self.curve_label = {1: []}
        self.x_label = {1: ""}
        self.y_label = {1: ""}
        self.figure_title = ["", 16]  # [title, font_size]
        self.axes_title = {1: ""}
        self.x_ticks = {1: []}
        self.x_ticks_label = {1: [[], 11]}  # [ticks_label, font_size]
        self.y_ticks = {1: []}
        self.y_ticks_label = {1: [[], 11]}  # [ticks_label, font_size]
        self.grid_on = {1: False}
        self._setup_dataset()
        
    # def set_dim(self, row, col):
    #     """
    #     Set dimension for the figure window
    #     ie. number of axes in each row and column in figure window
    #
    #     :param row: number of axes in each row
    #     :param col: number of axes in each column
    #     :return: None
    #     """
    #     self.fig_dim = [row, col]
    #     self._setup()
        
    def _setup_dataset(self):
        """
        Helper function to setup dataset structure for further manipulation
        
        :return: None
        """
        # clear all old axes
        self.axes_list.clear()
        
        # update axes and data
        row = self.fig_dim[0]
        col = self.fig_dim[1]
        
        for i in range(1, row * col + 1):
            self.curve_data.update({i: self.curve_data[i] if i in self.curve_data.keys() else []})
            self.curve_label.update({i: self.curve_label[i] if i in self.curve_label.keys() else []})
            self.x_label.update({i: self.x_label[i] if i in self.x_label.keys() else ""})
            self.y_label.update({i: self.y_label[i] if i in self.y_label.keys() else ""})
            self.axes_title.update({i: self.axes_title[i] if i in self.axes_title.keys() else ""})
            self.x_ticks.update({i: self.x_ticks[i] if i in self.x_ticks.keys() else []})
            self.x_ticks_label.update({i: self.x_ticks_label[i] if i in self.x_ticks_label.keys() else [[], 11]})
            self.y_ticks.update({i: self.y_ticks[i] if i in self.y_ticks.keys() else []})
            self.y_ticks_label.update({i: self.y_ticks_label[i] if i in self.y_ticks_label.keys() else [[], 11]})
            self.grid_on.update({i: self.grid_on[i] if i in self.grid_on.keys() else False})
            
    def _setup_figure(self):
        """
        Helper function to setup figure window and axes
        
        :return: None
        """
        row = self.fig_dim[0]
        col = self.fig_dim[1]
        
        for i in range(1, row * col + 1):
            
            if not plt.fignum_exists(1):
                # no figure window
                # create figure object
                # https://stackoverflow.com/questions/7557098/matplotlib-interactive-mode-determine-if-figure-window-is-still-displayed
                self.figure = plt.figure()
                
                # clear all old axes
                self.axes_list.clear()
                
            # create and store axes object
            self.axes_list.append(
                    self.figure.add_subplot(row, col, i)  # axes
            )
        
    def add_graph(self, data = None, x = None, y = None, label = None, index = 1):
        """
        Add graph on the given index of axes
        Legend is automatically turned on if label for each curves is given
        
        :param data: 3D list of curve data. [ [[graph1 x], [graph1 y]], [[graph2 x], [graph2 y]], ... ]
        :param x: curve data for x
        :param y: curve data for y
        :param label: legend label for the graph
        :param index: index for the graph. Count from 1.
        :return: None
        """
        if data:
            
            for i in range(len(data)):
                # store to class
                self.curve_data[index].append(data[i])
                self.curve_label[index].append( label[i] if label else None )
                
                # plot to axes in memory
                # curve = data[i]
                # _x = curve[0]
                # _y = curve[1]
                # self.axes_list[index - 1].plot(_x, _y, label = label[i] if label else None)
                
        if x and y:
            # store to class
            self.curve_data[index].append([x, y])
            self.curve_label[index].append(label)
            
            # plot to axes in memory
            # self.axes_list[index - 1].plot(x, y, label = label)
        
        # self.axes_list[index - 1].legend()
        
    def set_x_label(self, label, index = None):
        """
        Set x-axis label for given graph's index
        To set all at once, pass a list of str for all axes respectively
        By default, the same label is set for all axes if no index is specified.
        
        :param label: label for x-axis of type str, index number is required for axes indexed greater than 1.
                      Pass a list of label for axes indexed in ascending order, index number is not required.
        :param index: index of the axes
        :return: None
        """
        if isinstance(label, str):
            
            if index:
                # set for 1 axes only
                self.x_label[index] = label
            
            else:
                # set for all axes
                for i in self.x_label.keys():
                    self.x_label[i] = label
                    
            # self.axes_list[index - 1].set_xlabel(label)
            
        elif isinstance(label, list):
            # multiple graphs
            for i in range(len(label)):
                self.x_label[i + 1] = label[i]
                
                # self.axes_list[i].set_xlabel(label[i])
    
    def set_y_label(self, label, index = None):
        """
        Set y-axis label for given graph's index
        To set all at once, pass a list of str for all axes respectively
        By default, the same label is set for all axes if no index is specified.
        
        :param label: label for y-axis of type str, index number is required for axes indexed greater than 1.
                      Pass a list of label for axes indexed in ascending order, index number is not required.
        :param index: index of the axes
        :return: None
        """
        if isinstance(label, str):
            
            if index:
                # set for 1 axes only
                self.y_label[index] = label
                
            else:
                # set for all axes
                for i in self.y_label.keys():
                    self.y_label[i] = label
                    
            # self.axes_list[index - 1].set_ylabel(label)
            
        elif isinstance(label, list):
            # multiple graphs
            for i in range(len(label)):
                self.y_label[i+1] = label[i]
                
                # self.axes_list[i].set_ylabel(label[i])
        
    def set_fig_title(self, title, font_size = 16):
        """
        Set title for the figure
        
        :param title: title for the whole figure of type str
        :param font_size: font size of the figure title
        :return:
        """
        self.figure_title = [title, font_size]
    
    def set_axes_title(self, title, index = 1):
        """
        Set title for individual axes
        To set all at once, pass a list of str for all axes respectively
        
        :param title: title for individual axes of type str, index number is required for axes indexed greater than 1.
                      Pass a list of str for axes indexed in ascending order, index number is not required.
        :param index: index of the axes. Count from 1.
        :return: None
        """
        if isinstance(title, str):
            # set for 1 axes only
            self.axes_title[index] = title
            
            # self.axes_list[index - 1].set_title(title)
        
        if isinstance(title, list):
            # multiple graphs
            for i in range(len(title)):
                self.axes_title[i+1] = title[i]
                
                # self.axes_list[i].set_title(title[i])
    
    def set_x_ticks(self, ticks, label = None, index = 1, font_size = 11):
        """
        Set tick marks and tick labels for individual axes
        
        :param ticks: tick marks on x-axis
        :param label: tick labels on x-axis
        :param index: index of the axes. Count from 1.
        :param font_size: font size of the tick marks and labels
        :return: None
        """
        self.x_ticks[index] = ticks
        self.x_ticks_label[index] = [label, font_size]
        
        # self.axes_list[index - 1].set_xticks(ticks)
        # self.axes_list[index - 1].set_xticklabels(label if label else ticks, fontsize = font_size)
    
    def set_y_ticks(self, ticks, label = None, index = 1, font_size = 11):
        """
        Set tick marks and tick labels for individual axes

        :param ticks: tick marks on y-axis
        :param label: tick labels on y-axis
        :param index: index of the axes. Count from 1.
        :param font_size: font size of the tick marks and labels
        :return: None
        """
        self.y_ticks[index] = ticks
        self.y_ticks_label[index] = [label, font_size]
        
        # self.axes_list[index - 1].set_yticks(ticks)
        # self.axes_list[index - 1].set_yticklabels(label if label else ticks, fontsize = font_size)
        
    def grid(self, index = None):
        """
        Turn on major grid lines for given index of axes
        By default, grid line for all axes is turned on when if index is not given
        
        :param index: index of axes. Count from 1.
                      Pass a list of int for turning on grid lines on axes indexed in ascending order
        :return: None
        """
        # for all axes by default
        if not index:
            
            for i in range(len(self.curve_data)):
                self.grid_on[i+1] = True
                
                # self.axes_list[i].grid()
                
        # for one axes at given index
        if isinstance(index, int):
            self.grid_on[index] = True
            
            # self.axes_list[index - 1].grid()
        
        # for individual axes specified in the list
        if isinstance(index, list):
            
            for i in index:
                self.grid_on[i] = True
                
                # self.axes_list[i - 1].grid()
                
    def clear(self):
        """
        Clear all figure and data
        
        :return: None
        """
        self.fig_dim = [1, 1]
        self.axes_list.clear()
        self.curve_data = {1: []}
        self.curve_label = {1: []}
        self.x_label = {1: ""}
        self.y_label = {1: ""}
        self.figure_title = ["", 16]  # [title, font_size]
        self.axes_title = {1: ""}
        self.x_ticks = {1: []}
        self.x_ticks_label = {1: [[], 11]}  # [ticks_label, font_size]
        self.y_ticks = {1: []}
        self.y_ticks_label = {1: [[], 11]}  # [ticks_label, font_size]
        self.grid_on = {1: False}
        
    def plot(self, tight_layout = True, h_space = None, w_space = None):
        """
        Plot and show the figure
        
        :param tight_layout: let matplotlib automatically adjust graph to avoid overlapping
        :param h_space: explicitly indicate vertical spacing between subplots
        :param w_space: explicitly indicate horizontal spacing between subplots
        :return: None
        """
        # create figure and axes object
        self._setup_figure()
        
        # plot curves
        for i in range(len(self.axes_list)):
            
            # plot curves
            for curve, curve_label in zip(self.curve_data[i+1], self.curve_label[i+1]):
                self.axes_list[i].plot(curve[0], curve[1], label = curve_label)
                
                if curve_label:
                    self.axes_list[i].legend()
            
            # set axis label
            self.axes_list[i].set_xlabel(self.x_label[i+1])
            self.axes_list[i].set_ylabel(self.y_label[i+1])
            
            # set axes title
            self.axes_list[i].set_title(self.axes_title[i+1])
            
            # set ticks and tick labels
            x_ticks = self.x_ticks[i+1]
            y_ticks = self.y_ticks[i+1]
            x_ticks_label = self.x_ticks_label[i+1]
            y_ticks_label = self.y_ticks_label[i+1]
            if x_ticks:
                self.axes_list[i].set_xticks(x_ticks)
            if y_ticks:
                self.axes_list[i].set_yticks(y_ticks)
            if x_ticks_label[0]:
                self.axes_list[i].set_xticklabels(x_ticks_label[0], fontsize = x_ticks_label[1])
            if y_ticks_label[0]:
                self.axes_list[i].set_yticklabels(y_ticks_label[0], fontsize = y_ticks_label[1])
            
            # turn on major grid lines
            if self.grid_on[i+1]:
                self.axes_list[i].grid()
                
        # set figure title
        self.figure.suptitle(self.figure_title[0], fontsize = self.figure_title[1])
        
        # set tight layout
        if tight_layout:
            plt.tight_layout()
            
        # set subplots' spacing
        if h_space:
            self.figure.subplots_adjust(hspace = h_space)
            
        if w_space:
            self.figure.subplots_adjust(wspace = w_space)
            
        plt.show()
        


# fig = Figure(row = 1, col= 2)
# f = [[2, 3], [3, 4]]
# g = [[1, 2], [2, 3]]
# fig.add_graph([f, g], label = ["1", "2"])
# fig.add_graph([ [[1, 2, 3], [2, 3, 4]], [[2, 3], [3, 4]]], index = 2)
# fig.add_graph([ [[1, 2], [2, 4]] ], index = 2)
# fig.set_x_label(["hii", "byee"])
# fig.set_y_label(["hii", "byee"])
# fig.set_axes_title(["hi", "bye"])
# fig.set_fig_title("asdf")
# # fig.set_x_ticks([1, 1.5, 2, 2.5, 3])
# # fig.set_y_ticks([1, 1.5, 2, 2.5, 3], ["a", "b", "c", "d", "e"])
# # fig.set_x_ticks([1, 1.5, 2, 2.5, 3], index = 2)
# # fig.set_y_ticks([1, 1.5, 2, 2.5, 3], ["a", "b", "c", "d", "e"], 2)
# fig.grid()
# fig.plot()
# fig.clear()
# fig.plot()
