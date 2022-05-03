class Simplex:
    def __init__(self, objFunc, constraints):
        self.objFunc = objFunc
        self.constraints = constraints
        print(objFunc)
        print(constraints)

    def solve(self):
        print("Solving...")
        self._add_slack_variables()
        unknown = self._get_pivot_element()

    
    """
    Adding slack variables
    """
    def _add_slack_variables(self):
        for i in range(len(self.constraints)):
            self.constraints[i][f's{i+1}'] = 1

    def _get_pivot_element(self):
        pivot_row_index = self._get_pivot_row_index()
        print(pivot_row_index)
        pivot_column_index = self._get_pivot_column_index(pivot_row_index)
        print(pivot_column_index)
        
    """ 
    Returning the pivot index (variable letter) by getting the 
    maximum value in the objective function
    """
    def _get_pivot_row_index(self):
        index = 0
        values = list(self.objFunc.values())
        max_val = max(values)
        return list(self.objFunc.keys())[values.index(max_val)]

    """
    Returning the index of the pivot column by calculating the minimum value of
    the 'val' row after dividing each value by the corresponding pivot row value
    """
    def _get_pivot_column_index(self, row_index):
        pivot_row_values = [constraint[row_index] for constraint in self.constraints]

        divisions = []
        for i in range(len(self.constraints)):
            if pivot_row_values[i] == 0:
                divisions.append(float('inf'))
            else:
                divisions.append(self.constraints[i]['val'] / pivot_row_values[i])

        print(divisions)

        min_val = min(divisions)
        return divisions.index(min_val)