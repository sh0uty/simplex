import re

from collections import defaultdict

re_comment1 = re.compile(r"(\/\*[\s\S]*\*\/)")
re_comment2 = re.compile(r"(^\/\/.*$)")

def parse_data(data):
    data = _remove_comments(data)
    data = _remove_empty_lines(data)

    objFunc = _parse_objective_function(data[0])
    constraints = _parse_constraints(data[1:])

    #data = _transpose(objFunc, constraints)
    return constraints, objFunc


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
    
    objective_function = objective_function[4:] #! Parse min and max differently
    objective_function = [line.strip().replace(';', '') for line in objective_function.split('+') if line.strip()]
    objective_function = [pair.split('*') for pair in objective_function]
    
    pairs = defaultdict(int)

    for pair in objective_function:
        pairs[pair[1]] = int(pair[0])

    return pairs

def _parse_constraints(constraints):
    list_of_pairs = []
    for constraint in constraints:
        constraint, val = constraint.split('<=')
        constraint = [line.strip() for line in constraint.split('+') if line.strip()]
        constraint = [pair.split('*') for pair in constraint]

        pairs = defaultdict(int)

        for pair in constraint:
            pairs[pair[1]] = int(pair[0])

        pairs['val'] = int(val.replace(';', ''))

        list_of_pairs.append(pairs)
    
    return list_of_pairs