import sympy


class MatrixResolver:
    def __init__(self, mat):
        self.mat = self.construct_matrix(mat)
        self.__rows = self.mat.rows - 1
        self.__cols = self.mat.cols - 1
        self.__len = self.mat.__len__()
        self.result = []
        self.row_simplify_matrix()

    def construct_matrix(self, mat):
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if isinstance(mat[i][j], str):
                    mat[i][j] = sympy.symbols(mat[i][j])

        return sympy.Matrix(mat)

    def append_result(self, s):
        self.result.append({"s": s, "r": self.mat[:]})

    def row_swap(self, i, j):
        self.mat.row_swap(i, j)
        self.append_result("swap row: {} and {}".format(i + 1, j + 1))

    def change(self, head_row, head_col, curr_row):
        if self.mat[curr_row, head_col] != 0:
            s = "[row {0}] change to [row {0}] - ({1} / {2}) * [row {3}]".format(curr_row + 1,
                                                                                 self.mat[curr_row, head_col],
                                                                                 self.mat[head_row, head_col],
                                                                                 head_row + 1)
            self.mat.row_op(curr_row,
                            lambda v, j: v - (self.mat[curr_row, head_col] / self.mat[head_row, head_col]) * self.mat[
                                head_row, j])
            self.append_result(s)

    def change_all(self, head_row, head_col, curr_row, to_row):
        while curr_row <= to_row:
            self.change(head_row, head_col, curr_row)
            curr_row += 1

    def find_first_not_zero_local(self, head_row, head_col):
        curr_row = head_row + 1
        while curr_row <= self.__rows:
            if self.mat[curr_row, head_col] != 0:
                return curr_row
            curr_row += 1
        return -1

    def ladder(self):
        head_row = 0
        head_col = 0
        while True:
            if head_row > self.__rows or head_col > self.__cols:
                return
            if self.mat[head_row, head_col] == 0:
                not_zero_row = self.find_first_not_zero_local(head_row, head_col)
                if not_zero_row == -1:
                    head_col += 1
                else:
                    self.row_swap(head_row, not_zero_row)
                    self.change_all(head_row, head_col, not_zero_row + 1, self.__rows)
                    head_row += 1
                    head_col += 1
            else:
                self.change_all(head_row, head_col, head_row + 1, self.__rows)
                head_row += 1
                head_col += 1

    def find_main_element(self, row):
        col = 0
        while col <= self.__cols:
            if self.mat[row, col] != 0:
                return col
            col += 1
        return -1

    def _row_simplify_matrix(self):
        curr_row = self.__rows
        while curr_row >= 0:
            main_element = self.find_main_element(curr_row)
            if main_element != -1:
                self.change_all(curr_row, main_element, 0, curr_row - 1)
            curr_row -= 1

    def main2one(self):
        curr_row = 0
        while curr_row <= self.__rows:
            main_element = self.find_main_element(curr_row)
            if main_element != -1:
                main = self.mat[curr_row, main_element]
                self.mat.row_op(curr_row, lambda v, j: v / main)
            curr_row += 1

    def row_simplify_matrix(self):
        self.append_result("origin")
        self.ladder()
        self._row_simplify_matrix()
        self.main2one()
        self.append_result("main element to one")

        for k in self.result:
            for i in range(self.__len):
                k['r'][i] = '"' + str(k['r'][i]) + '"'
