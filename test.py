#!/usr/bin/env python3
import sudoku


def main():
    # l = [1, 2, 3, 4, 5, 6, 7, 8]
    l = [int(i) for i in list(
        """800000000003600000070090200050007000000045700000100030001000068008500010090000400""")]
    print(l)
    b = sudoku.SudokuBoard(l, 9)
    print(b)
    b.populate()
    print(b)

if __name__ == '__main__':
    main()
