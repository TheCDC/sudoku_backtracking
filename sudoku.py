#!/usr/bin/env python3
from backtracking_iter import backtrack
import backtracking_iter
from beeprint import pp
import time
import functools
import random
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
        row_offset = self.root * (n // self.root)
        rows = self.rows[row_offset: row_offset + self.root]
        for row in rows:
            col_offset = self.root * (n % self.root)
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
        if len(self.original) > self.square:
            return False

        for i in range(self.size):
            if invalid_set(self.row(i)) or invalid_set(self.col(i)):
                # print("invalid row", row)
                return False

                # print("checking row:", row)
            # need to check each square
            # there are size squares, call this n
            # for nth square
            # square size = size**(1/2)
            # square horiz offset = n% (root size)
            # vert offset = n/(root size)
            # print(root)

        for n in range(self.size):
            # print("Checking nth square in board:",n,sq,end=" ")
            if invalid_set(self.quadrant(n)):
                # print("bad")
                # print("invalid quadrant", n, quad)
                return False
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

        cans = tuple(self.all_digits - set(ns) - set([0]))
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
    return tuple(head) + tuple(0 for i in range((size * size) - len(head)))


def invalid_set(x) -> bool:
    nozeroes = len([i for i in x if i != 0])
    try:
        uniques = len(set(x) - set([0]))
    except Exception as e:
        # print("Error checking if invalid:", x)
        raise e
    return uniques < nozeroes

def sudoku_next_choices(head, size):
    b = SudokuBoard(head, size)
    return list(b.candidates(*lin_to_xy(len(head), size)))

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
                # if len(head) >= 54 == 0:
                #     print(b)
                final = sudoku_next_choices(head,size)
            else:
                # print("Occupied space. Choosing its value.")
                final = [selected]
        # print("selected for next:", final)
        # random.shuffle(final)
        return tuple(final)

    return wrapped


# @functools.lru_cache(maxsize=1024)
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
    print("Test case:")
    start = [int(i) for i in list(
        """003020600900305001001806400008102900700000008006708200002609500800203009005010300""")]
    start = [int(i) for i in list(
        """000050040200800530510029678000004003072030950600200000125940087098003002060080000""")]
    # start = []
    # print(start)
    tb = SudokuBoard(start, bsize)
    print(tb)
    # print(tb.quadrant(0))
    # assert tb.check_partial(), "Test input failure"
    # assert tb.quadrant(0) == [int(i) for i in list("003900001")]
    # assert tb.quadrant(4) == [int(i) for i in list("102000708")]
    # assert tb.quadrant(5) == [int(i) for i in list("900008200")]
    # assert tb.row(0) == [int(i) for i in list("003020600")]
    # assert tb.row(8) == [int(i) for i in "005010300"]
    # print(tb.candidates(0,0))
    # input()

    try:
        numthreads = int(input("num threads?\n>>>").strip())
    except ValueError:
        numthreads = 8
    br = backtracking_iter.Backtracker(
        next_choice_func=sudoku_next_choice_wrapper(start, bsize),
        candidate_matcher=sudoku_final_wrapper(bsize),
        partial_checker=sudoku_partial_wrapper(bsize),
        greedy=False,
        starting_guesses=[[]])
    br.go(numthreads=numthreads)

    prev = 0
    cur = 0
    hist = []
    while br.intermediate_queue.qsize() > 0:
        cur = br.intermediate_queue.qsize()
        delta = cur - prev
        solsize = br.solutions_queue.qsize()
        hist.append((cur,delta,solsize))
        try:
            print("inter:", cur, "delta", delta,
                  "sols:", solsize)
            prev = cur
            # input("\n>>>")
            time.sleep(1)
        except KeyboardInterrupt:
            sols = []
            if br.solutions_queue.qsize() > 0:
                for i in range(br.solutions_queue.qsize()):
                    sols.append(br.solutions_queue.get())
                with open("solutions.txt", 'w') as f:
                    f.write('\n'.join(str(SudokuBoard(i, bsize)) for i in sols))
            for t in br.mythreads:
                t.terminate()
            print("Exited safely.")
            break
    results = []
    for i in range(br.solutions_queue.qsize()):
        results.append(SudokuBoard(br.solutions_queue.get(), bsize))
    for i in results:
        print(i)

if __name__ == '__main__':
    main()
