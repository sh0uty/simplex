from collections import defaultdict

class Simplex:
    def __init__(self, objFunc, constraints, problem):
        self.problem = problem
        self.objFunc = objFunc
        self.originalObjFunc = objFunc.copy()
        self.constraints = constraints
        self.pretty_print()
        self.slack_variables = []

    def pretty_print(self):
        for constraint in self.constraints:
            print(dict(constraint))
        print("---------------------------------------------------")
        print(dict(self.objFunc))

    def solve(self):
        win_condition = False
        count = 1
        self._add_slack_variables()
        while not win_condition:
            pivot_column_index, pivot_row_index = self._get_pivot_element()

            print(f"Pivot: Column - {pivot_column_index}, Row - {pivot_row_index} -> Pivot Element: {self.constraints[pivot_row_index][pivot_column_index]}")
            print()

            self._subtract_pivot_row_from_rows(pivot_column_index, pivot_row_index)
            self.pretty_print()

            win = []
            for key in self.objFunc:
                if self.objFunc[key] <= 0:
                    win.append(True)
                else:
                    win.append(False)
            win_condition = all(win)
            count += 1

        print(count)
        self.get_solution()

    """
    Adding slack variables
    """
    def _add_slack_variables(self):
        for i in range(len(self.constraints)):
            self.constraints[i][f's{i+1}'] = 1
            self.slack_variables.append(f's{i+1}')

    def _get_pivot_element(self):
        pivot_column_index = self._get_pivot_column_index()
        pivot_row_index = self._get_pivot_row_index(pivot_column_index)
        return pivot_column_index, pivot_row_index
        
    """ 
    Returning the pivot index (variable letter) by getting the 
    maximum value in the objective function
    """
    def _get_pivot_column_index(self):
        objFunc_exclude_val = self.objFunc.copy()

        objFunc_exclude_val['val'] = -1*float('inf')

        values = list(objFunc_exclude_val.values())
        max_val = max(values)
        return list(objFunc_exclude_val.keys())[values.index(max_val)]

    """
    Returning the index of the pivot row by calculating the minimum value of
    the 'val' column after dividing each value by the corresponding pivot column value
    """
    def _get_pivot_row_index(self, column_index):
        pivot_column_values = [constraint[column_index] for constraint in self.constraints]

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

        print("Divisions: ", divisions)

        min_val = min(divisions)
        return divisions.index(min_val)

    def _subtract_pivot_row_from_rows(self, pivot_column_index, pivot_row_index):
        pivot_element = self.constraints[pivot_row_index][pivot_column_index]

        if pivot_element != 1:
            for key in self.constraints[pivot_row_index]:
                self.constraints[pivot_row_index][key] /= pivot_element

        pivot_element = self.constraints[pivot_row_index][pivot_column_index]

        pivot_row = self.constraints[pivot_row_index]
        rows = self.constraints + [self.objFunc]

        for row in rows:
            if row == pivot_row:
                continue
            
            multiplicator = row[pivot_column_index] / pivot_element

            for key in pivot_row:
                row[key] -= multiplicator * pivot_row[key]


    def get_solution(self):
        value = self.objFunc['val'] * -1

        rows = self.constraints + [self.objFunc]

        solution = defaultdict(int)

        all_keys = set()
        for row in rows:
            all_keys.update(row.keys())

        for key in all_keys:
            if key == 'val':
                continue

            column = []
            for row in rows:
                column.append(row[key])
            
            if sum(column) == 1 and set(column) == set([1,0]):
                solution[key] = column.index(1)

        print()
        print(f'Solution: {value}')
        print()
        if self.problem == 'min':
            pass
        else:
            for key in self.originalObjFunc:
                if key in solution:
                    print(f'{key}: {self.constraints[solution[key]]["val"]}')
                else:
                    print(f'{key}: 0')