#!/usr/bin/env python3
from backtracking_iter import backtrack
import backtracking_iter
from beeprint import pp
import time
"""Sudoku stuff will be working with a serialized version of a board.
The whole board will be a 1-dimensional list of digits.
Any functions involving a board should be aware of this."""

# def print(*args,**kwargs):
#     pass


class SudokuBoard():

    def __init__(self, serialized, size):
        self.size = size
        self.root = int(size**(1 / 2))
        self.square = size * size
        if len(serialized) > size * size:
            raise ValueError("Board too big.")
        elif size < 1:
            raise ValueError("Requested size too small ({})".format(size))
        elif size**(1 / 2) % 1 != 0:
            raise ValueError("Size must be a square number!")
        self.serialized = pad_serialized_board(serialized, size)
        self.rows = []
        self.rows = sublists(self.serialized, size)
        self.original = serialized[:]
        # print(self.rows)
        # print("Constructed this board: ")
        # pp(self.rows)
        # print("From this list:", serialized)
        self.all_digits = set(range(1, size + 1))

    def check(self):
        return self.check_partial() and len(self.original) == self.square

    def quadrant(self, n):
        sq = []
        root = self.root
        row_offset = self.root*(n // self.root)
        rows = self.rows[row_offset: row_offset + self.root]
        for row in rows:
            col_offset = root * (n % self.root)
            sq.extend(row[col_offset: col_offset + self.root])
        return sq

    def row(self, y) -> list:
        return self.rows[y]

    def col(self, x) -> list:
        ns = []
        for i in range(self.size):
            ns.append(self.rows[i][x])
        return ns

    def check_partial(self):
        for rows in [self.rows, list(zip(*self.rows))]:
            for row in rows:
                # print("checking row:", row)
                if invalid_set(row):
                    # print("invalid row", row)
                    return False
            # need to check each square
            # there are size squares, call this n
            # for nth square
            # square size = size**(1/2)
            # square horiz offset = n% (root size)
            # vert offset = n/(root size)
            # print(root)

        for n in range(self.size):
            # print("Checking nth square in board:",n,sq,end=" ")
            quad = self.quadrant(n)
            if invalid_set(quad):
                # print("bad")
                # print("invalid quadrant", n, quad)
                return False
            else:
                pass
                # print("good")

        return True

    def candidates(self, x, y):
        ns = []
        # horizontal line
        ns.extend(self.row(y))
        # vertical line
        ns.extend(self.col(x))
        xmin = self.root * (x // self.root)
        xmax = xmin + self.root
        ymin = self.root * (y // self.root)
        ymax = ymin + self.root
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                try:
                    # print("y, x, root",y,x,self.root)
                    ns.append(self.rows[y][x])
                except Exception as e:
                    # print(self)
                    raise e

        cans = list(self.all_digits - set(ns) - set([0]))
        # print(set(ns) - set([0]))
        # print("Candidates for",x,y,cans)
        return cans

    def __repr__(self):
        return "SudokuBoard({}, {})".format(self.serialized, self.size)

    def __str__(self):
        sroot = int(self.size**(1 / 2))
        rowsep = "\n" + "-" * (self.size + 4)
        return rowsep + "\n" + '\n'.join("|" + ''.join(str(i) + "|" * ((index + 1) % sroot == 0) for index, i in enumerate(row)) + (rowsep) * ((irow + 1) % sroot == 0) for irow, row in enumerate(self.rows))


def lin_to_xy(n, size):
    return (n % size, n // size)


def sublists(l, partition_size):
    return [l[i:i + partition_size] for i in range(0, len(l), partition_size)]


def pad_serialized_board(head, size):
    return head + [0 for i in range((size * size) - len(head))]


def invalid_set(x) -> bool:
    nozeroes = len([i for i in x if i != 0])
    try:
        uniques = len(set(x) - set([0]))
    except Exception as e:
        # print("Error checking if invalid:", x)
        raise e
    return uniques < nozeroes


def sudoku_next_choice_wrapper(serialized_board, size):
    """Return a list of possible next choices given a serialized board."""
    extended = pad_serialized_board(serialized_board, size)
    # print("Info about choosing next move:",
    #       serialized_board,
    #       len(serialized_board),
    #       (size * size) - len(serialized_board))

    def wrapped(head) -> list:

        # print("Choosing next from", head)
        final = None
        if len(head) >= len(extended):
            # print("Reached target length. No more guesses.")
            final = []
        else:
            selected = extended[len(head)]
            if selected == 0:
                # print("Empty space. Choosing candidates.")
                b = SudokuBoard(head, size)
                # if len(head) >= 54 == 0:
                #     print(b)
                final = b.candidates(*lin_to_xy(len(head), size))
                del b
            else:
                # print("Occupied space. Choosing its value.")
                final = [selected]
                del selected
        # print("selected for next:", final)
        return final

    return wrapped


def sudoku_test_func(head, size) -> bool:
    result = SudokuBoard(head, size).check_partial()
    # print("Checking if", head, "is valid,", result)
    return result


def sudoku_partial_wrapper(size):
    def wrapped(head):
        return sudoku_test_func(head, size)
    return wrapped


def sudoku_final_wrapper(size):
    def wrapped(head):
        # print(head)
        # return len(head) == size * size
        return SudokuBoard(head, size).check()
    return wrapped


def main():
    print("Sudoku")
    bsize = 9
    bguess = [[]]
    print("Test case:")
    start = [int(i) for i in list(
        """003020600900305001001806400008102900700000008006708200002609500800203009005010300""")]
    # print(start)
    tb = SudokuBoard(start, 9)
    print(tb)
    print(tb.quadrant(0))
    assert tb.check_partial(), "Test input failure"
    assert tb.quadrant(0) == [int(i) for i in list("003900001")]
    assert tb.quadrant(4) == [int(i) for i in list("102000708")]
    assert tb.quadrant(5) == [int(i) for i in list("900008200")]
    assert tb.row(0) == [int(i) for i in list("003020600")]
    assert tb.row(8) == [int(i) for i in list("005010300")]

    br = backtracking_iter.Backtracker(
        next_choice_func=sudoku_next_choice_wrapper(start, bsize),
        candidate_matcher=sudoku_final_wrapper(bsize),
        partial_checker=sudoku_partial_wrapper(bsize),
        greedy=True,
        starting_guesses=[[]])
    br.go(numthreads=2)

    prev = 0
    cur = 0
    while br.intermediate_queue.qsize() > 0:
        cur = br.intermediate_queue.qsize()
        try:
            print("inter:",cur,"delta", cur-prev,"sols:", br.solutions_queue.qsize())
            # input()
            prev = cur
            time.sleep(1)
        except KeyboardInterrupt:
            quit()
    results = []
    for i in range(br.solutions_queue.qsize()):
        results.append(SudokuBoard(br.solutions_queue.get(), bsize))
    for i in results:
        print(i)

    # old function-only method without threading
    # results = backtrack(
    #     next_choice_func=sudoku_next_choice_wrapper(
    #         start, bsize),
    #     candidate_matcher=sudoku_final_wrapper(bsize),
    #     partial_checker=sudoku_partial_wrapper(bsize),
    #     greedy=True,
    #     starting_guesses=[[]])
    # print(results)
    # rr = []
    # for i in results:
    #     rr.append(SudokuBoard(i, bsize))
    # for i in rr:
    #     print(i, i.check())

if __name__ == '__main__':
    main()
