#!/usr/bin/env python3
import backtracking
from beeprint import pp
import time
import functools
import random
"""Sudoku stuff will be working with a serialized version of a board.
The whole board will be a 1-dimensional list of digits.
Any functions involving a board should be aware of this."""


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
        # assert type(serialized[0]) == int, "Must be list of ints."
        self.original = serialized[:]
        self.serialized = pad_serialized_board(serialized, size)
        self.rows = []
        self.rows = sublists(self.serialized, size)
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
            if invalid_set(self.row(i)) or invalid_set(self.col(i)) or invalid_set(self.quadrant(i)):
                # print("invalid row", row)
                return False
        for i in range(self.square):
            # check for any empty cells with 0 candidates
            x,y = lin_to_xy(i,self.size)
            z = self.get(x,y)
            if len(self.candidates(x,y)) == 0 and z == 0:
                return False

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
                ns.append(self.rows[y][x])

        cans = tuple(self.all_digits - set(ns) - set([0]))
        # print(set(ns) - set([0]))
        # print("Candidates for",x,y,cans)
        return cans

    def get(self, x, y):
        return self.rows[y][x]

    def __repr__(self):
        return "SudokuBoard({}, {})".format(self.serialized, self.size)

    def __str__(self):
        sroot = int(self.size**(1 / 2))
        rowsep = "\n" + "-" * (self.size + self.size // self.root + 1)
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
        print("Error checking if invalid:", x)
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
        final = []
        try:
            if len(head) >= len(extended):
                # print("Reached target length. No more guesses.")
                final = []
            else:
                selected = extended[len(head)]
                if selected == 0:
                    # print("Empty space. Choosing candidates.")
                    # if len(head) >= 54 == 0:
                    #     print(b)
                    final = sudoku_next_choices(head, size)

                else:
                    # print("Occupied space. Choosing its value.")
                    final = [selected]
        except Exception as e:
            print("HEAD:", head)
            raise e
        # print("selected for next:", final)
        # random.shuffle(final)
        # print(final)
        assert isinstance(final, list)

        return final

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
    print("Test case:")
    start = [int(i) for i in list(
        """483921657900305001001806400008102900700000008006708200002609500800203009005010300""")]
    start = [int(i) for i in list(
        """003020600900305001001806400008102900700000008006708200002609500800203009005010300""")]
    start = [int(i) for i in list(
        """000000000000000000000000000000000000000000000000000000000000000000000000000000000""")]
    start = [int(i) for i in list(
        """000050040200800530510029678000004003072030950600200000125940087098003002060080000""")]
    # start = []
    bsize = 9
    # print(start)
    tb = SudokuBoard(start, bsize)
    print(tb)
    assert tb.check_partial(), "Test input failure"
    # print(tb.quadrant(0))
    # assert tb.quadrant(0) == [int(i) for i in list("003900001")]
    # assert tb.quadrant(4) == [int(i) for i in list("102000708")]
    # assert tb.quadrant(5) == [int(i) for i in list("900008200")]
    # assert tb.row(0) == [int(i) for i in list("003020600")]
    # assert tb.row(8) == [int(i) for i in "005010300"]
    # print(tb.candidates(0,0))
    # input()

    try:
        numthreads = int(input("How many threads? default=8\n>>>").strip())
    except ValueError:
        numthreads = 8
    print(numthreads, "threads")
    br = backtracking.Backtracker(
        next_choice_func=sudoku_next_choice_wrapper(start, bsize),
        candidate_matcher=sudoku_final_wrapper(bsize),
        partial_checker=sudoku_partial_wrapper(bsize),
        starting_guesses=[[]])
    br.go(numthreads=numthreads)

    prev = 0
    cur = 0
    c = 0
    while br.intermediate_queue.qsize() > 0 and br.solutions_queue.qsize() == 0:
        # print("test")
        cur = br.intermediate_queue.qsize()
        delta = cur - prev
        solsize = br.solutions_queue.qsize()
        try:
            print("inter:", cur, "delta", delta,
                  "sols:", solsize)
            if c == 0:
                b = br.intermediate_queue.get()
                print(SudokuBoard(b, bsize))
                br.intermediate_queue.put(b)
            prev = cur
            # input("\n>>>")
            c = (c + 1) % 10
            time.sleep(1)
        except KeyboardInterrupt:
            # for t in br.mythreads:
            #     t.terminate()
            print("Exited safely.")
            break
    br.quit()
    br.join()
    if br.solutions_queue.qsize() > 0:
        print("Early solution found!")
    results = []
    for i in range(br.solutions_queue.qsize()):
        results.append(SudokuBoard(br.solutions_queue.get(), bsize))
    results = [i for i in results if i.check()]
    with open("solutions.txt", 'w') as f:
        f.write("{} boards\n".format(len(results)) +
                '\n'.join(str(i) for i in results))

if __name__ == '__main__':
    main()
