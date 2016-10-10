#!/usr/bin/env python3
import sudoku_solving
import time
import matplotlib.pyplot as plt


def main():
    test_results = {}
    # for num_procs in [4,8,12,16,20,24,32]:
    for num_procs in range(4, 32 + 1, 2):
        test_results.update({num_procs: []})
        print("Testing", num_procs, "process(es)")
        for i in range(20):
            s = list(map(
                int, "800000000003600000070090200050007000000045700000100030001000068008500010090000400"))
            # print("Start:")
            # print(SudokuBoard(s))
            # print("Solution:")
            ti = time.time()
            sudoku_solving.solve_string(s, num_processes=num_procs)
            tf = time.time()
            print("\tDeltaT = ", tf - ti, "seconds")
            test_results[num_procs].append(tf - ti)
    for k, i in sorted(test_results.items(), key=lambda x: x[0]):
        print(k, sum(i) / len(i))
    with open("benchmarks.txt",'w') as f:
        f.write(str(test_results))
    plt.figure()
    xs, ys = list(zip(*sorted(test_results.items(), key=lambda x: x[0])))
    ys = [sum(i)/len(i) for i in ys]
    plt.plot(xs,ys) 
    plt.show()

if __name__ == '__main__':
    main()
