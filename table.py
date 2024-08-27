#--------\---------\---------\---------\---------\---------\---------\---------\
import numpy as np
import sys

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
