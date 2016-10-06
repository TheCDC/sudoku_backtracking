#!/usr/bin/env python3
"""Sudoku stuff will be working with a serialized version of a board.
The whole board will be a 1-dimensional list of digits.
Any functions involving a board should be aware of this."""
import backtracking
import time
import sys
import os
import signal

class UserRequestedQuit(Exception):
    pass

class SudokuBoard():

    """Handle a Sudoku board and various bits of information needed to solve it."""

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

    def check(self) -> bool:
        """Return whether the board is solved."""
        return len(self.original) == self.square and set(self.all_digits) - set(self.original) == set() and self.check_partial()

    def quadrant(self, n) -> list:
        """Return a list of all cells in the nth quadrant, start fomr the top left
        and going first to the right then down."""
        sq = []
        row_offset = self.root * (n // self.root)
        rows = self.rows[row_offset: row_offset + self.root]
        for row in rows:
            col_offset = self.root * (n % self.root)
            sq.extend(row[col_offset: col_offset + self.root])
        return sq

    def row(self, y) -> list:
        """Return a list of all cells in the nth row."""
        return self.rows[y]

    def col(self, x) -> list:
        """Return a lsit of all cells in the nth column."""
        ns = []
        for i in range(self.size):
            ns.append(self.rows[i][x])
        return ns

    def check_partial(self) -> bool:
        """Return whether the board does not violate any rules."""
        if len(self.original) > self.square:
            return False

        for i in range(self.size):
            if invalid_set(self.row(i)) or invalid_set(self.col(i)) or invalid_set(self.quadrant(i)):
                # print("invalid row", row)
                return False
        for i in range(self.square):
            # check for any empty cells with 0 candidates
            x, y = lin_to_xy(i, self.size)
            z = self.get(x, y)
            if len(self.candidates(x, y)) == 0 and z == 0:
                return False

        return True

    def candidates(self, x, y) -> set:
        """Get the set of possible digits that could be filled into cell at x,y"""
        cur = self.get(x, y)
        if cur != 0:
            return set([cur])
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

        cans = self.all_digits - set(ns) - set([0])
        # print(set(ns) - set([0]))
        # print("Candidates for",x,y,cans)
        return cans

    def populate(self):
        for x in range(self.size):
            for y in range(self.size):
                cur = self.get(x, y)
                if cur == 0:
                    cs = self.candidates(x, y)
                    if len(cs) == 1:
                        self.set(cs.pop(), x, y)

    def get(self, x, y) -> int:
        """Get value of cell at x,y"""
        return self.rows[y][x]

    def set(self, n, x, y):
        self.rows[y][x] = n

    def __repr__(self) -> str:
        return "SudokuBoard({}, {})".format(self.serialized, self.size)

    def __str__(self) -> str:
        sroot = int(self.size**(1 / 2))
        rowsep = "\n" + "-" * (self.size + self.size // self.root + 1)
        return rowsep + "\n" + '\n'.join("|" + ''.join(str(i) + "|" * ((index + 1) % sroot == 0) for index, i in enumerate(row)) + (rowsep) * ((irow + 1) % sroot == 0) for irow, row in enumerate(self.rows))


def lin_to_xy(n, size) -> tuple:
    return (n % size, n // size)


def sublists(l, partition_size) -> list:
    return [l[i:i + partition_size] for i in range(0, len(l), partition_size)]


def pad_serialized_board(head, size) -> tuple:
    return head + [0 for i in range((size * size) - len(head))]


def invalid_set(x) -> bool:
    nozeroes = len([i for i in x if i != 0])
    try:
        uniques = len(set(x) - set([0]))
    except Exception as e:
        print("Error checking if invalid:", x)
        raise e
    return uniques < nozeroes


def sudoku_next_choices(head, size) -> list:
    b = SudokuBoard(head, size)
    b.populate()
    return list(b.candidates(*lin_to_xy(len(head), size)))


def sudoku_next_choice_wrapper(serialized_board, size):
    """Return a list of possible next choices given a serialized board."""
    extended = pad_serialized_board(serialized_board, size)
    def wrapped(head) -> list:
        final = []
        try:
            if len(head) >= len(extended):
                final = []
            else:
                selected = extended[len(head)]
                if selected == 0:
                    final = sudoku_next_choices(head, size)

                else:
                    final = [selected]
        except Exception as e:
            print("HEAD:", head)
            raise e
        assert isinstance(final, list)

        return final

    return wrapped


# @functools.lru_cache(maxsize=1024)
def sudoku_test_func(head, size) -> bool:
    result = SudokuBoard(head, size).check_partial()
    # print("Checking if", head, "is valid,", result)
    return result


def sudoku_partial_wrapper(size):
    def wrapped(head) -> bool:
        return sudoku_test_func(head, size)
    return wrapped


def sudoku_final_wrapper(size):
    def wrapped(head) -> bool:
        # print(head)
        # return len(head) == size * size
        return SudokuBoard(head, size).check()
    return wrapped


def solve_string(s, *args, **kwargs) -> SudokuBoard:
    """Take a string serialized board return the solved board.
    Results may vary based on threading."""
    return solve_list([int(i) for i in s], *args, **kwargs)


def solve_list(l, size, num_processes, timeout=None) -> SudokuBoard:
    """Take a list serialized board and return the solved board.
    Results may vary based on threading."""
    tb = SudokuBoard(l, size)
    if not tb.check_partial():
        raise ValueError("Ilegal starting board.")
    br = backtracking.Backtracker(
        next_choice_func=sudoku_next_choice_wrapper(l, size),
        candidate_matcher=sudoku_final_wrapper(size),
        partial_checker=sudoku_partial_wrapper(size),
        starting_guesses=[[]])
    br.go(numthreads=num_processes)
    ti = time.time()
    while not br.solutions_queue.empty() and br.intermediate_queue.empty():
        if timeout:
            if time.time() - ti >= timeout:
                return None
    br.terminate()
    if not br.solutions_queue.empty():
        return SudokuBoard(br.solutions_queue.get(), size)
    else:
        return None

def quit_handler(a,b):
    print("Caught Ctrl-C")
    raise UserRequestedQuit()


def main():
    os.setpgrp()
    print("Sudoku")
    print("Test case:")
    start = [int(i) for i in list(
        """000000000000000000000000000000000000000000000000000000000000000000000000000000000""")]
    start = [int(i) for i in list(
        """003020600900305001001806400008102900700000008006708200002609500800203009005010300""")]
    start = [int(i) for i in list(
        """000050040200800530510029678000004003072030950600200000125940087098003002060080000""")]
    start = [int(i) for i in list(
        """483921657900305001001806400008102900700000008006708200002609500800203009005010300""")]
    start = [int(i) for i in list(
        """800000000003600000070090200050007000000045700000100030001000068008500010090000400""")]
    # start = []
    bsize = 9
    # print(start)
    tb = SudokuBoard(start, bsize)
    print(tb)
    assert tb.check_partial(), "Test input failure"

    try:
        numthreads = int(input("How many threads? default=4\n>>>").strip())
    except ValueError:
        numthreads = 4
    print(numthreads, "threads")
    br = backtracking.Backtracker(
        next_choice_func=sudoku_next_choice_wrapper(start, bsize),
        candidate_matcher=sudoku_final_wrapper(bsize),
        partial_checker=sudoku_partial_wrapper(bsize),
        starting_guesses=[[]])
    br.go(numthreads=numthreads)
    signal.signal(signal.SIGINT,quit_handler)

    prev = 0
    cur = 0
    c = 0
    while not br.intermediate_queue.empty() and br.solutions_queue.empty():
        # print("test")
        if not sys.platform == "darwin":
            cur = br.intermediate_queue.qsize()
            delta = cur - prev
            solsize = br.solutions_queue.qsize()
            print("inter:", cur, "delta", delta,
                  "sols:", solsize)
            prev = cur
        try:
            if c == 0:
                b = br.intermediate_queue.get()
                print(SudokuBoard(b, bsize))
                br.intermediate_queue.put(b)
            # input("\n>>>")
            c = (c + 1) % 10
            time.sleep(1)
        except UserRequestedQuit:
            print("Quitting...")
            # for t in br.mythreads:
            #     t.terminate()
            br.terminate()
            br.join()
            # time.sleep(3)
            l = []
            while not br.intermediate_queue.empty():
                l.append(''.join([str(i) for i in br.intermediate_queue.get()]))
            with open("partials.txt",'w') as f:
                f.write('\n'.join(l))
            print("Exited safely.")
            sys.exit()
    br.terminate()
    br.join()
    if not br.solutions_queue.empty():
        print("Solution found!")
        results = []
        while not br.solutions_queue.empty():
            r = SudokuBoard(br.solutions_queue.get(), bsize)
            print(r)
            results.append(r)
        results = [i for i in results if i.check()]
        with open("solutions.txt", 'w') as f:
            f.write("{} boards\n".format(len(results)) +
                    '\n'.join(str(i) for i in results))


if __name__ == '__main__':
    main()
