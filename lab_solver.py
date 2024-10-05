#--------\---------\---------\---------\---------\---------\---------\---------\
import matplotlib.pyplot as plt
import numpy as np

import math
import sys

from matplotlib.ticker import LinearLocator

class Table():
    """Represents a table of measurements we write on paper.
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
            """Sets limits for how many symbols can be present from either side
            of dot if it is present. In the absense of dot, only
            leading_characters_max attibute is used to center cells.
            """
            for i in range(self.columns):
                max_leading = 0; max_fractional = 0; max_nzfractional = 0;

                for j in range(len(self.contents[i])):
                    entry = str(self.contents[i][j]).split(".")
                    leading = len(entry[0])
                    max_leading = max(leading, max_leading)
                    # if leading > max_leading:
                    if len(entry) > 1:
                        fract    = len(entry[1])
                        nz_fract = fract - entry[1].count("0")
                        max_fractional   = max(fract, max_fractional)
                        max_nzfractional = max(nz_fract, max_nzfractional)

                self.leading_characters_max[i]      = max_leading
                self.fractional_characters_max[i]   = max_fractional
                self.nzfractional_characters_max[i] = max_nzfractional

        set_max_characters(self)

    def print(self, file=sys.stdout):
        """Writes a neat formatted table into file object
        and leaves it open (stdout by default)
        """
        def center(self, indx):
            """Figures out how many spaces are needed to allign name from left 
            and right and returns them as 2 integers
            """
            name_len = len(self.names[indx])
            max_len  = self.leading_characters_max[indx]
            if self.fractional_characters_max[indx] > 0:
                max_len += 1 + self.fractional_characters_max[indx] 

            diff = max_len - name_len
            if diff < 0:
                l = 1 
                r = 1
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
            """Figures out how many spaces are needed to allign number cell
            from left and right and returns them as 2 integer coefficients.
            """
            cell = string.split(".")
            left =  self.leading_characters_max[col_indx] - len(cell[0])

            if len(cell) > 1:
                right = self.fractional_characters_max[col_indx] - len(cell[1])
            else:
                right = 0

            diff = len(self.names[col_indx]) - (len(string)+left+right)
            if diff > 0:
                left  += int(diff/2)
                right += int(diff/2)
                if diff%2 != 0:
                    left += 1
            return left + 1, right + 1
        
        def top_border(self):
            """Returns "+-" string that can be used to separate each row."""
            line = ""
            for i in range(self.columns):
                s = self.leading_characters_max[i] + 2
                if self.fractional_characters_max[i] > 0:
                    s += self.fractional_characters_max[i] + 1

                name_len = len(self.names[i])
                if s <= name_len:
                    s += name_len - s + 2

                line += "+"+"-"*s
            line+="+\n"
            return line

        separator = (top_border(self))
        file.write(separator)

        for r in range(self.rows):
            row = ""
            for c in range(self.columns):
                cell = str(self.contents[c][r])
                left, right = allign_coefficients(self, cell, c)
                row += "|" + left*" " + cell + right*" "
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
            self.x_origin, self.x_end = 0, 28 # number of 1cm cells horizontally
            self.y_origin, self.y_end = 0, 20 # number of 1cm cells vertically
        else:
            self.fig, self.ax = plt.subplots(figsize=(HEIGHT, WIDTH), dpi=DPI)
            self.x_origin, self.x_end = 0, 20 # number of 1cm cells horizontally
            self.y_origin, self.y_end = 0, 28 # number of 1cm cells vertically

        self.ax.set_aspect('equal')
        self.ax.set_xticks(range(self.x_end+1), xlabels)  # X ticks every 1 cm
        self.ax.set_yticks(range(self.y_end+1), ylabels)  # Y ticks every 1 cm
        self.ax.xaxis.set_minor_locator(LinearLocator(self.x_end*10))
        self.ax.yaxis.set_minor_locator(LinearLocator(self.y_end*10))
        #self.ax.set_xticklabels()
        self.ax.set(xlim=(self.x_origin, self.x_end), 
                    ylim=(self.y_origin, self.y_end),
                    title=title)
        self.ax.set_xticklabels(xlabels)
        self.ax.set_yticklabels(ylabels)
        self.ax.grid(which="major",color='c', lw=1)
        self.ax.grid(which="minor",color='c', lw=0.25)
        # Adjust margins to specific values
        # (left: 8.5 mm, right: 8.5 mm, top: 5 mm, bottom: 5 mm)
        plt.subplots_adjust(left=0.0286, right=0.9714, 
                            top=0.9762, bottom=0.0238)

    """
    def autoplot(self, x, y):
        #Do stuff on x and y
        self.plot(x, y)

    def autoscat(self, x, y, color="black", s=10, **kwargs):
        print("automatic scatter")
        x /= xstep; x += xoff
        y /= ystep; y += yoff
        plt.scatter(x, y, color=color, s=s, **kwargs)
    """

    def plot(self, *args, **kwargs):
        plt.plot(*args, color="black", **kwargs)

    def save(self, *args, **kwargs):
        plt.savefig(*args, **kwargs)

    def show(self):
        plt.show()

    def scatter(self, x, y, color="black", s=10, **kwargs):
        if type(x) == np.ndarray:
            xstep = find_step(np.floor(x[0]), np.ceil(x[-1]))
            ystep = find_step(np.floor(y[0]), np.ceil(y[-1]), 'y')
        else:
            xstep = find_step(np.floor(x), np.ceil(x))
            ystep = find_step(np.floor(y), np.ceil(y), 'y')

        print("x, y steps:", xstep, ystep)
        plt.scatter(x, y, color=color, s=s, **kwargs)

    def test_plot(self, x, y):
        plt.scatter(x[0], y[0], color="red")
        plt.scatter(x, y, color="black", s=10)
        plt.plot(x, y, color="black")
        plt.scatter(x[-1], y[-1], color="red")

    def scale(self, x_array, y_array):
        x = np.copy(x_array)
        y = np.copy(y_array)
        x_min = np.floor(np.min(x)); x_max = np.ceil(np.max(x))
        y_min = np.floor(np.min(y)); y_max = np.ceil(np.max(y))
        xcells = self.x_end - self.x_origin
        ycells = self.y_end - self.y_origin
        print(f"x: {x_min} - {x_max}")
        print(f"y: {y_min} - {y_max}")
        return x, y


class LeastSquares(Table):
    """The same table as before but methods are tweaked to write less code in 
    scripts.
    """
    def __init__(self, col1_name, col2_name, x, y, presicion=3):
        """Creates names and contents from given arguments. Calculates contents
        averages and deviations with coefficients.
        """
        self.a_coef = 0
        self.b_coef = 0
        self.averages = []
        self.deviations = []
        
        def set_names(col1_name, col2_name):
            """
            Creates names for 2, 4 and 5th columns based on provided names.
            col2_name is actually third column.
            """
            names = ["" for i in range(6)]
            names[0] = "N"
            names[1] = col1_name
            names[3] = col2_name

            def x_squared_name(name, i):
                if ',' in name:
                    names[i] = (name.split(',')[0]+"^2," +
                            name.split(',')[1]+"^2")
                else:
                    names[i] = name+"^2"

            x_squared_name(col1_name, 2)
            x_squared_name(col2_name, 4)
            names[5] = (col1_name.split(',')[0] + "*" +
                        col2_name.split(',')[0])
            if col1_name.count(',') == col2_name.count(',') == 1:
                names[5] += (" " +col1_name.split(',')[1] + "*" +
                             col2_name.split(',')[1])
            return names

        def calc_contents(x, y):
            """Implements all logic in least squares method."""
            n = len(x)
            N = np.arange(1, n+1)
            x2 = np.round(np.copy(x)**2, presicion)
            y2 = np.round(np.copy(y)**2, presicion)
            xy = np.round(x*y, presicion)
            contents = [N, x, x2, y, y2, xy]

            def avg(data):
                return round(sum(data)/n, presicion)

            σx = avg(x2) - avg(x)**2
            σy = avg(y2) - avg(y)**2

            a = (avg(xy) - (avg(x)*avg(y))) / σx
            b = avg(y) - a*avg(x)
            self.a_coef = a; self.b_coef = b

            σa = math.sqrt((1/(n-2))*((σy/σx) - a**2))
            σb = σa*math.sqrt(avg(x2))
            self.averages = [avg(x), avg(x2), avg(y), avg(y2), avg(xy)]
            self.deviations = [σx, σy, σa, σb]
            return contents

        names = set_names(col1_name, col2_name)
        contents = calc_contents(x, y)
        super().__init__(names, contents)
        print("Created a table")

    def coefficients(self):
        """Returns a - slope and b - offset coefficients of line."""
        return self.a_coef, self.b_coef


def least_squares(x, y, names, presicion=3):
    """Uses least squares to calculat a and b coefficients of line
    Returns a, b, collumns of squares [x, x^2, y, y^2, x*y],
    list of their averages in respecting order, and list of deviations
    [x, y, a, b]. SHOUD PROBABLY RETURN THEM AS STRINGS and add 2 separate 
    presicions
    """
    n = len(x)
    N = np.arange(1, n+1)
    x2 = np.round(np.copy(x)**2, presicion)
    y2 = np.round(np.copy(y)**2, presicion)
    xy = np.round(x*y, presicion)
    contents = [N, x, x2, y, y2, xy]
    def avg(data):
        return round(sum(data)/n, presicion)
    σx = avg(x2) - avg(x)**2
    σy = avg(y2) - avg(y)**2
    #print(avg(xy), avg(x)*avg(y), σx)
    a = (avg(xy) - (avg(x)*avg(y))) / σx
    b = avg(y) - a*avg(x)
    σa = math.sqrt((1/(n-2))*((σy/σx) - a**2))
    σb = σa*math.sqrt(avg(x2))
    averages = [avg(x), avg(x2), avg(y), avg(y2), avg(xy)]
    deviations = [σx, σy, σa, σb]
    print(f"a = {a}; b = {b}")
    print(f"Avg: x={averages[0]}; x^2={averages[1]};")
    print(f"y={averages[2]}; y^2={averages[3]}; <xy>={averages[4]}")
    print(f"dev: σx={σx}, σy={σy}, σa={σa}, σb={σb}")
    table = Table(names, contents)
    return a, b, contents, averages, deviations

def sigma(x):
    """
    Takes in array of squares of deviations.
    Returns standard deviation.
    """
    n = len(x)
    s = math.sqrt(np.sum(x)/n*(n-1))
    return s

def standard_deviation(data, presicion=3):
    """Calculates standard deviation for given data and returns two numpy
    arrays. Deviation from average and deviation from average squared.
    """
    n        = len(data)
    avg      = np.average(data) 
    avg_dif  = np.zeros(n)
    avg_dif2 = np.zeros(n)

    for i in range(n):
        avg_dif[i] = round(data[i] - avg, presicion)
        avg_dif2[i] = round(avg_dif[i]**2, presicion)
    return avg_dif, avg_dif2

def pair_point(x, y, headings): #SHOULD RETURN TABLE
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

    σ = sigma(avg_dif2)
    contents = [point_pairs, Δx, Δy, angle, avg_dif, avg_dif2]
    #table = Table(headings, contents)
    return k, σ, contents


def read_data(file_name="input.csv"):
    """Stores file data in array and returns it"""
    file = open(file_name, "r")
    data = []
    for line in file:
        data.append(line)
    file.close()
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

    if len(line) == 1:
        columns = np.array(columns[0])
    else:
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
