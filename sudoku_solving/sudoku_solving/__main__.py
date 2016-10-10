from sudoku_solving import *
import argparse

main()
def main():
    if sys.platform == "linux":
        os.setpgrp()
    print("Sudoku")
    print("Test case:")
    start = list(map(
        int, "000050040200800530510029678000004003072030950600200000125940087098003002060080000"))
    start = list(map(
        int, "483921657900305001001806400008102900700000008006708200002609500800203009005010300"))
    start = list(map(
        int, "000000000000000000000000000000000000000000000000000000000000000000000000000000000"))
    start = list(map(
        int, "900100400007020080060000000400500200080090010003006000100700030005008900020000006"))
    start = list(map(
        int, "003020600900305001001806400008102900700000008006708200002609500800203009005010300"))
    start = list(map(
        int, "800000000003600000070090200050007000000045700000100030001000068008500010090000400"))

    # start = []
    bsize = 9
    # print(start)
    tb = SudokuBoard(start, bsize)
    print(tb)
    assert tb.check_partial(), "Test input failure"

    try:
        numthreads = int(input("How many processes? default=4\n>>>").strip())
    except ValueError:
        numthreads = 4
    print(numthreads, "process(es)")
    ti_solve = time.time()
    br = backtracking.Backtracker(
        next_choice_func=sudoku_next_choices,
        candidate_matcher=sudoku_final_test,
        partial_checker=sudoku_partial_test,
        starting_guesses=[tb])
    br.go(numthreads=numthreads)

    while br.solutions_queue.empty():
        pass
    br.terminate()
    br.join()
    if not br.solutions_queue.empty():
        print("Solution found!")
        print("DeltaT = {:.5f}ish".format(time.time() - ti_solve), "seconds")
        results = []
        while not br.solutions_queue.empty():
            r = br.solutions_queue.get()
            r.unoptimize()
            print(r)
            results.append(r)
        results = [i for i in results if i.check()]
        with open("solutions.txt", 'w') as f:
            f.write("{} boards\n".format(len(results)) +
                    '\n'.join(str(i) for i in results))

    # discarded = []
    # while not br.discard_queue.empty():
    #     discarded.append(str(br.discard_queue.get().untransformed()))
    # with open("discarded.txt", 'w') as f:
    #     f.write("{} discarded\n".format(len(discarded)) + '\n'.join(discarded))


if __name__ == '__main__':
    main()