import re

from collections import defaultdict

re_comment1 = re.compile(r"(\/\*[\s\S]*\*\/)")
re_comment2 = re.compile(r"(^\/\/.*$)")

def parse_data(data):
    data = _remove_comments(data)
    data = _remove_empty_lines(data)

    problem, objFunc = _parse_objective_function(data[0])
    constraints = _parse_constraints(data[1:], problem)

    if problem.lower() == 'min':
        objFunc, constraints = _transpose(objFunc, constraints)
    return constraints, objFunc, problem


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
    problem, objective_function = objective_function.split(':')
    objective_function = [line.strip().replace(';', '') for line in objective_function.split('+') if line.strip()]
    objective_function = [pair.split('*') for pair in objective_function]
    
    pairs = defaultdict(int)

    for pair in objective_function:
        pairs[pair[1]] = int(pair[0])

    return problem, pairs

def _parse_constraints(constraints, problem):
    list_of_pairs = []
    for constraint in constraints:
        if problem.lower() == 'min':
            constraint, val = constraint.split('>=')
        else:
            constraint, val = constraint.split('<=')
        constraint = [line.strip() for line in constraint.split('+') if line.strip()]
        constraint = [pair.split('*') for pair in constraint]

        pairs = defaultdict(int)

        for pair in constraint:
            pairs[pair[1]] = int(pair[0])

        pairs['val'] = int(val.replace(';', ''))

        list_of_pairs.append(pairs)
    
    return list_of_pairs


def _transpose(objFunc, constraints):
    all_variables = list(objFunc.keys()) + ['val']

    matrix = constraints.copy()
    matrix.append(objFunc)

    transposed = []
    for key in all_variables:
        transposed.append([row[key] for row in matrix])

    new_constraints_list = transposed[:-1]
    new_objFunc_list = transposed[-1]

    new_constraints = []
    new_objFunc = defaultdict(int)

    for row in new_constraints_list:
        constraint = defaultdict(int)
        for i in range(len(row) - 1):
            constraint[f'yx{i}'] = row[i]
        constraint['val'] = row[-1]
        new_constraints.append(constraint)

    for i in range(len(new_objFunc_list) - 1):
        new_objFunc[f'yx{i}'] = new_objFunc_list[i]
    new_objFunc['val'] = new_objFunc_list[-1]

    return new_objFunc, new_constraints