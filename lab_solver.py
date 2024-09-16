#--------\---------\---------\---------\---------\---------\---------\---------\
import matplotlib.pyplot as plt
import numpy as np

import math
import sys

from matplotlib.ticker import LinearLocator

class Table():
    """
    Represents a table of measurements we write on paper.
    Names and contents are both lists. By indexing them you can access a
    particular column. Names include heading for each column while contents
    include all data in that column converted to numpy NDArray.
    """
    def __init__(self, names, contents):
        """Initializes all attributes and sets them to uasble values."""
        self.names    = names
        self.contents = contents
        self.columns  = len(names)
        self.rows     = len(contents[0])
        self.leading_characters_max      = [0 for i in range(self.columns)]
        self.fractional_characters_max   = [0 for i in range(self.columns)]
        self.nzfractional_characters_max = [0 for i in range(self.columns)]
        if len(self.contents) != self.columns:
            print("Table is missing or having extra elements")
            exit()
        def set_max_characters(self):
            for i in range(self.columns):
                max_leading = 0; max_fractional = 0; max_nzfractional = 0;
                for j in range(len(self.contents[i])):
                    entry = str(self.contents[i][j]).split(".")
                    leading = len(entry[0])
                    max_leading = max(leading, max_leading)
                    if len(entry) > 1:
                        fract    = len(entry[1])
                        nz_fract = fract - entry[1].count("0")
                        max_fractional   = max(fract, max_fractional)
                        max_nzfractional = max(nz_fract, max_nzfractional)
                self.leading_characters_max[i]      = max_leading
                self.fractional_characters_max[i]   = max_fractional
                self.nzfractional_characters_max[i] = max_nzfractional
        set_max_characters(self)


    def print_test(self):
        """Test print of whether heading and array is included or not."""
        for i in range(self.columns):
            print(f"| {self.names[i]} ", end=" ")
        print("|")

        for i in range(3):
            for j in range(len(self.contents)):
                print(f"| {self.contents[j][i]} ", end = " ")
            print("|")

        print(self.leading_characters_max)
            

    def print(self, file=sys.stdout):
        """
        Writes a neat formatted table into file object
        and leaves it open (stdout by default)
        """
        def center(self, indx):
            """
            Figures out how many spaces are needed to allign name from left 
            and right and returns them as 2 integers
            """
            name_len = len(self.names[indx])
            max_len = (self.leading_characters_max[indx] +
                       self.fractional_characters_max[indx]) 
            if self.fractional_characters_max[indx] > 0:
                max_len += 1 # accomodate for '.'
            diff = max_len - name_len
            if diff < 0:
                l = 1 
                r = 1
                self.leading_characters_max[indx]      = name_len
                self.fractional_characters_max[indx]   = 0
                self.nzfractional_characters_max[indx] = 0
            else:
                l = int(diff/2) + 1
                r = int(diff/2) + 1
                if diff%2 != 0:
                    l += 1
            return l, r

        heading = ""
        for i in range(self.columns):
            l, r = center(self, i)
            heading += "|" +l*" " + self.names[i] + r*" "
        heading += "|\n"
        file.write(heading)

        def allign_coefficients(self, string, col_indx):
            """
            Figures out how many spaces are needed to allign cell from left 
            and right and returns them as 2 integer coefficients
            """
            cell = string.split(".")
            left_space =  self.leading_characters_max[col_indx] - len(cell[0])
            if len(cell) > 1:
                right_space = self.fractional_characters_max[col_indx] - len(cell[1])
            else:
                right_space = 0
            return left_space + 1, right_space + 1
        
        def top_border(self):
            """ returns "+-" string that can be used to separate each row."""
            line = ""
            for i in range(self.columns):
                s = self.leading_characters_max[i] + 2
                if self.fractional_characters_max[i] > 0:
                    s += self.fractional_characters_max[i] + 1
                line += "+"+"-"*s
            line+="+\n"
            return line

        separator = (top_border(self))
        file.write(separator)

        for r in range(self.rows):
            row = ""
            for c in range(self.columns):
                cell = str(self.contents[c][r])
                left_space, right_space = allign_coefficients(self, cell, c)
                row += "|" + left_space*" " + cell + right_space*" "
            row += "|\n"
            file.write(row)
            #file.write(separator)
        print("Check the file")


class GraphPaper():
    def __init__(self, xlabels="", ylabels="", title="",orientation='h'):
        WIDTH, HEIGHT = 28/2.54, 20/2.54
        DPI = 100
        if orientation == 'h':
            self.fig, self.ax = plt.subplots(figsize=(WIDTH, HEIGHT), dpi=DPI)
            x_origin, x_end = 0, 28 # number of 1cm cells horizontally
            y_origin, y_end = 0, 20 # number of 1cm cells vertically
        else:
            self.fig, self.ax = plt.subplots(figsize=(HEIGHT, WIDTH), dpi=DPI)
            x_origin, x_end = 0, 20 # number of 1cm cells horizontally
            y_origin, y_end = 0, 28 # number of 1cm cells vertically

        self.ax.set_aspect('equal')
        self.ax.set_xticks(range(x_end+1), xlabels)  # X-axis ticks every 1 cm
        self.ax.set_yticks(range(y_end+1), ylabels)  # Y-axis ticks every 1 cm
        self.ax.xaxis.set_minor_locator(LinearLocator(x_end*10))
        self.ax.yaxis.set_minor_locator(LinearLocator(y_end*10))
        #self.ax.set_xticklabels()
        self.ax.set(xlim=(x_origin, x_end), ylim=(y_origin, y_end),
               title=title)
        self.ax.set_xticklabels(xlabels)
        self.ax.set_yticklabels(ylabels)
        self.ax.grid(which="major",color='c', lw=1)
        self.ax.grid(which="minor",color='c', lw=0.25)
        # Adjust margins to specific values (left: 8.5 mm, right: 8.5 mm, top: 5 mm, bottom: 5 mm)
        plt.subplots_adjust(left=0.0286, right=0.9714, 
                            top=0.9762, bottom=0.0238)
    def frame(self, x, y):
        xstep = find_step(np.floor(x[0]), np.ceil(x[-1]))
        ystep = find_step(np.floor(y[0]), np.ceil(y[-1]), 'y')
        print("x, y steps:", xstep, ystep)
        xstart, ystart = 0, 0
        return xstart, xstep, ystart, ystep

    def plot(self, *args, **kwargs):
        plt.plot(*args, **kwargs)

    def save(self, *args, **kwargs):
        plt.savefig(*args, **kwargs)

    def show(self):
        plt.show()

    def scatter(self, x, y, **kwargs):
        xstep = find_step(np.floor(x[0]), np.ceil(x[-1]))
        ystep = find_step(np.floor(y[0]), np.ceil(y[-1]), 'y')
        print("x, y steps:", xstep, ystep)
        plt.scatter(x, y, **kwargs)


def what_is_going_on(x, y):
    print(f"X {np.min(x)} - {np.max(x)}")
    print(f"Y {np.min(y)} - {np.max(y)}")
    print("X floor", np.floor(x[0]))
    print("Y floor", np.floor(y[0]))

#def least_squares_method(x, y):
def sigma(x, n):
    """Takes in array of squares of deviations and length of x.
    Returns standard deviation.
    """
    s = math.sqrt(np.sum(x)/n*(n-1))
    return s

def standard_deviation(data, presicion=3):
    avg = np.average(data) 
    n = len(data)
    avg_dif = np.zeros(n)
    avg_dif2 = np.zeros(n)
    for i in range(n):
        avg_dif[i] = round(data[i] - avg, presicion)
        avg_dif2[i] = round(avg_dif[i]**2, presicion)
    return avg_dif, avg_dif2

def pair_point_method(x, y, headings):
    """Calculates angle using method of pairs of points
    and it's standard deviation
    """
    if len(x)%2 != 0:
        print("Number of points must be even in order to use pair")
        return 0, 0, 0

    pairs = int(len(x)/2)
    point_pairs = ["" for i in range(pairs)]
    Δx       = np.zeros(pairs)
    Δy       = np.zeros(pairs)
    angle    = np.zeros(pairs)

    for i in range(pairs):
        point_pairs[i] = f"{i+1}-{i+pairs+1}"
        Δx[i] = round(x[i+pairs] - x[i], 3)
        Δy[i] = round(y[i+pairs] - y[i], 3)
        angle[i] = round(Δy[i]/Δx[i], 3)

    k = np.average(angle) 
    avg_dif, avg_dif2 = standard_deviation(angle)

    σ = sigma(avg_dif2, pairs)
    contents = [point_pairs, Δx, Δy, angle, avg_dif, avg_dif2]
    #table = Table(headings, contents)

    return k, σ, contents


def read_data(file):
    """Stores file data in array and returns it"""
    data = []
    for line in file:
        data.append(line)
    return data

def parse_data(data):#, *arrays):
    """
    Splits array of csv linse by collumns and returns them as list of
    np.arrays of floats
    """
    line = data[0].split(',')
    columns = [[] for i in range(len(line))]
    for line in data:
        line = line.split(',')
        for i in range(len(line)):
            columns[i].append(float(line[i].strip()))
    columns = np.array(columns) 
    return columns


def find_step(a, b, ax='x'):
    cells = 0
    if ax in ['y', 'Y']:
        cells = 20
    else:
        cells = 28
    steps = [1, 2, 4, 5, 10]
    i = 0
    l = abs(b-a)
    while True:
        if l/steps[i] < cells:
            break
        else:
            l = abs(b-a)
            i += 1
    return steps[i]

#def find_edges(a, b, step, ax='x'):

