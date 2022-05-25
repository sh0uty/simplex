import os
from collections import defaultdict

class Simplex:
    def __init__(self, objFunc, constraints, problem):
        self.problem = problem
        self.objFunc = objFunc
        self.originalObjFunc = objFunc.copy()
        self.constraints = constraints
        self.slack_variables = []
        self.iteration = 1
        try:
            _, self.columns = map(int, os.popen('stty size', 'r').read().split())
        except:
            self.columns = 100

        print("Starting tableau: ")
        self.print_tabelau()
        print()

    def print_tabelau(self):
        print(end="-"*self.columns + "\n")
        for constraint in self.constraints:
            print(dict(constraint))
        print(dict(self.objFunc))
        print(end="-"*self.columns + "\n")
        print()


    def solve(self):
        win_condition = False
        self._add_slack_variables()
        while not win_condition:
            print(f"Starting iteration: {self.iteration}")
            print()

            pivot_column_index, pivot_row_index = self._get_pivot_element()

            print(f"Pivot: Column - {pivot_column_index}, Row - {pivot_row_index} -> Pivot Element: {self.constraints[pivot_row_index][pivot_column_index]}")
            print()

            self._subtract_pivot_row_from_rows(pivot_column_index, pivot_row_index)
            print("New tableau:")
            self.print_tabelau()

            win = []
            for key in self.objFunc:
                if self.objFunc[key] <= 0:
                    win.append(True)
                else:
                    win.append(False)
            win_condition = all(win)
            
            print(f"Ending iteration: {self.iteration}")
            print()
            self.iteration += 1

        self.get_solution()

    """
    Adding slack variables
    """
    def _add_slack_variables(self):
        for i in range(len(self.constraints)):
            self.constraints[i][f's{i}'] = 1
            self.slack_variables.append(f's{i}')

    def _get_pivot_element(self):
        pivot_column_index = self._get_pivot_column_index()
        pivot_row_index = self._get_pivot_row_index(pivot_column_index)
        return pivot_column_index, pivot_row_index
        
    """ 
    Returning the pivot index (variable letter) by getting the 
    maximum value in the objective function
    """
    def _get_pivot_column_index(self):
        print("Getting Pivot Column")
        objFunc_exclude_val = self.objFunc.copy()

        objFunc_exclude_val['val'] = -1*float('inf')

        values = list(objFunc_exclude_val.values())
        max_val = max(values)
        print(f"Max value in objective function: {max_val}")

        pivot_column_index = list(objFunc_exclude_val.keys())[values.index(max_val)]
        print(f"Pivot Column Index: {pivot_column_index}")
        print()

        return pivot_column_index


    """
    Returning the index of the pivot row by calculating the minimum value of
    the 'val' column after dividing each value by the corresponding pivot column value
    """
    def _get_pivot_row_index(self, column_index):
        print("Getting Pivot Row")
        pivot_column_values = [constraint[column_index] for constraint in self.constraints]

        print("Calculating quotients")

        divisions = []
        for i in range(len(self.constraints)):
            if pivot_column_values[i] == 0:
                divisions.append(float('inf'))
            else:
                divison = self.constraints[i]['val'] / pivot_column_values[i]
                if divison <= 0:
                    divisions.append(float('inf'))
                else:
                    divisions.append(self.constraints[i]['val'] / pivot_column_values[i])

        print("Quotients: ", divisions)

        min_val = min(divisions)
        print(f"Min quotient: {min_val}")

        pivot_row_index = divisions.index(min_val)
        print(f"Pivot Row: {pivot_row_index}")
        print()

        return pivot_row_index

    def _subtract_pivot_row_from_rows(self, pivot_column_index, pivot_row_index):
        print("Refreshing tableau by subtracting pivot row from all other rows")
        pivot_element = self.constraints[pivot_row_index][pivot_column_index]

        if pivot_element != 1:
            print("Dividing pivot row by pivot element")
            for key in self.constraints[pivot_row_index]:
                self.constraints[pivot_row_index][key] /= pivot_element

        pivot_element = self.constraints[pivot_row_index][pivot_column_index]

        pivot_row = self.constraints[pivot_row_index]
        rows = self.constraints + [self.objFunc]

        for row in rows:
            if row == pivot_row:
                continue
            
            multiplicator = row[pivot_column_index] / pivot_element

            print(f"Subracting {multiplicator} * pivot row from row {rows.index(row)} ")

            for key in pivot_row:
                row[key] -= multiplicator * pivot_row[key]
        print()

    def get_solution(self):
        print("Found optimal solution:")

        value = self.objFunc['val'] * -1

        rows = self.constraints + [self.objFunc]

        solution = defaultdict(int)

        all_keys = set()
        for row in rows:
            all_keys.update(row.keys())

        for key in all_keys:
            if key == 'val':
                continue

            column = [row[key] for row in rows]
            
            if sum(column) == 1 and set(column) == set([1,0]):
                solution[key] = column.index(1)

        print()
        print(f'Solution: {value}')
        print()
        if self.problem == 'min':
            for slack in self.slack_variables:
                if slack in self.objFunc:
                    val = -1 * self.objFunc[slack]
                    if val == 0:
                        print(f'{slack.replace("s", "x")}: {0}')
                    else:
                        print(f'{slack.replace("s", "x")}: {val}')
                else:
                    print(f'{slack}: 0')
        else:
            for key in self.originalObjFunc:
                if key in solution:
                    print(f'{key}: {self.constraints[solution[key]]["val"]}')
                else:
                    print(f'{key}: 0')