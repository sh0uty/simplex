import argparse

from parser import *
from simplex import Simplex

parser = argparse.ArgumentParser()

parser.add_argument("file", help="Input of lp file", type=str)

args = parser.parse_args()


def main():
    try:
        with open(args.file, 'r') as f:
            data = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("File not found")
        exit(1)
    
    constrains, objFunc = parse_data(data)
    result = Simplex(objFunc, constrains).solve()

if __name__ == '__main__':
    main()