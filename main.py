import argparse

from parser import *


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
    
    data = parse_data(data)


if __name__ == '__main__':
    main()