import re

from collections import defaultdict

re_comment1 = re.compile(r"(\/\*[\s\S]*\*\/)")
re_comment2 = re.compile(r"(^\/\/.+$)")

def parse_data(data):
    data = _remove_comments(data)
    data = _remove_empty_lines(data)
    data = _transpose(_parse_objective_function(data[0]), _parse_constraints(data[1:]))


def _remove_comments(data):
    comments = [re_comment1.findall(line) for line in data]
    comments += [re_comment2.findall(line) for line in data]

    for comment in comments:
        if comment:
            for line in comment:
                data.remove(line)
    return data

def _remove_empty_lines(data):
    return [line for line in data if line]



def _parse_objective_function(objective_function):
    objective_function = objective_function[4:]
    objective_function = [line.strip().replace(';', '') for line in objective_function.split('+') if line.strip()]
    objective_function = [pair.split('*') for pair in objective_function]
    
    pairs = defaultdict(int)

    for pair in objective_function:
        pairs[pair[1]] = int(pair[0])

    return pairs

def _parse_constraints(constraints):
    list_of_pairs = []
    for constrain in constraints:
        constrain, val = constrain.split('>=')
        constrain = [line.strip() for line in constrain.split('+') if line.strip()]
        constrain = [pair.split('*') for pair in constrain]

        pairs = defaultdict(int)

        for pair in constrain:
            pairs[pair[1]] = int(pair[0])

        pairs['val'] = int(val.replace(';', ''))

        list_of_pairs.append(pairs)
    
    return list_of_pairs


def _transpose(objective_function, constraints):
    matrix = []

    for constraint in constraints:
        matrix.append(list(constraint.values()))
    matrix.append(list(objective_function.values()) + ['z'])

    print(matrix)

    matrix = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

    print(matrix)