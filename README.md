Solving sudoku puzzles with backtracking.

# Setup #
This project requires installation of the included `backtracking` and `sudoku_solving` modules.

To do so, simply run `./install.sh`. I have only tested this on Ubuntu Linux. It may work on OSX.

# Run it #
`python3 -m sudoku_solving` `python -m  sudoku_solving` depending on your OS and python command name. Doing this will have it run whatever test board I currently have it set to solve. Eventually there will be a proper interface/API.

# Solving Strategy #
My solving strategy is normal backtracking but with a twist. The solving starts from the top left of the board. Now of course backtracking is faster the more partial solutions you can discard earlier on so I wrote a short routine that weights a given row on the board. The weighting is based on how many freebies are on the row and how closely concentrated to the left they are. For this weight a larger number is better. Each row in each row of quadrants is then sorted in descending order by their weights. Finally, the rows of quadrants are sorted by the weights of their highest scoring rows. The original order is remembered and boards can be "de-optimized" for output purposes.

# Lessons Learned #
Backtracking is pretty cool by itself, but it alone doesn't prune the possibility tree quite enough.
I learned that you have to manipulate your data so that information is concentrated at the root of the tree as much as possible.

I did this by "optimizing" the Sudoku boards by weighting each row in a row of quadrants by the measure of how well filled in cells were concentrated towards the beginning of that row. The measure is a formula is a came up with where a bigger number is better. The rows are then sorted in descending order. The original order the rows is also tracked.

Sorting the rows like this increases the allows more possibilities to be eliminated faster.

# Acknowledgements #
A big thank you to Aaron Renfroe for figuring out the information density bit.

# Introduction #
**By Christopher Chen**

This is a demonstration of my sudoku_solving Python library. It lives at [https://github.com/TheCDC/sudoku_backtracking](https://github.com/TheCDC/sudoku_backtracking)

It has routines for:

 1. Creating Sudoku board objects
 
 2. Manipulating boards to make solving easier
 
 4. getting/setting the values of cells on boards
 
 5. Populating the freebies
 
 6. Solving boards using multiprocessed backtracking.



# Usage #
Begin by importing the library. As always, never use wildcard imports in production. They are liable to muck up your namespace and you'll tear your hair out wondering why functions and being overwritten. The wildcard is used here for brevity.



```python
from sudoku_solving import *
```

Boards can be created from strings or lists. The size of the board is assumed to be 9x9, unless specified otherwise.


```python
board_str = ("003020600"
             "900305001"
             "001806400"
             "008102900"
             "700000008"
             "006708200"
             "002609500"
             "800203009"
             "005010300")
board = board_from_string(board_str)
print(board)
```

    -------------
    |--3|-2-|6--|
    |9--|3-5|--1|
    |--1|8-6|4--|
    -------------
    |--8|1-2|9--|
    |7--|---|--8|
    |--6|7-8|2--|
    -------------
    |--2|6-9|5--|
    |8--|2-3|--9|
    |--5|-1-|3--|
    -------------



```python
board_list = [0, 0, 3, 0, 2, 0, 6, 0, 0, 
              9, 0, 0, 3, 0, 5, 0, 0, 1,
              0, 0, 1, 8, 0, 6, 4, 0, 0,
              0, 0, 8, 1, 0, 2, 9, 0, 0,
              7, 0, 0, 0, 0, 0, 0, 0, 8,
              0, 0, 6, 7, 0, 8, 2, 0, 0,
              0, 0, 2, 6, 0, 9, 5, 0, 0,
              8, 0, 0, 2, 0, 3, 0, 0, 9,
              0, 0, 5, 0, 1, 0, 3, 0, 0]
board = SudokuBoard(board_list)
print(board)
```

    -------------
    |--3|-2-|6--|
    |9--|3-5|--1|
    |--1|8-6|4--|
    -------------
    |--8|1-2|9--|
    |7--|---|--8|
    |--6|7-8|2--|
    -------------
    |--2|6-9|5--|
    |8--|2-3|--9|
    |--5|-1-|3--|
    -------------


## Board Sizes ##
Simply supply the optional size argument to the constructor to create a non-9x9 board.


```python
l = [1,0,3,0,
     0,4,0,2,
     2,0,4,0,
     0,3,0,1]
b = SudokuBoard(l,size=4)
print(b)
```

    -------
    |1-|3-|
    |-4|-2|
    -------
    |2-|4-|
    |-3|-1|
    -------


## Solution Checking ##
Boards may also be checked for legality and finality with the `check` and `check_partial` methods.


```python
print("4x4 maybe still solvable?",
      b.check_partial(),
      "4x4 already solved?",
      b.check(),sep='\n')
```

    4x4 maybe still solvable?
    True
    4x4 already solved?
    False



```python
print("9x9 maybe still solvable?",
      board.check_partial(),
      "9x9 already solved?",
      board.check(),sep='\n')
```

    9x9 maybe still solvable?
    True
    9x9 already solved?
    False


## Board Transformation ##
Some boards are more difficult to solve and some are less. Some of those boards are the same. The `optimize` and `optimized` methods transform a board to optimize it or return the optimized version, respectively.

Those methods first fill in any freebies (cells with only one candidate) then sort the rows by their information density towards the left.


```python
print("Old",b,"New",b.optimized(),sep='\n')
```

    Old
    -------
    |1-|3-|
    |-4|-2|
    -------
    |2-|4-|
    |-3|-1|
    -------
    New
    -------
    |1-|3-|
    |-4|-2|
    -------
    |2-|4-|
    |-3|-1|
    -------



```python
print("Not optimized",board,"Optimized",board.optimized(),sep='\n')
```

    Not optimized
    -------------
    |--3|-2-|6--|
    |9--|3-5|--1|
    |--1|8-6|4--|
    -------------
    |--8|1-2|9--|
    |7--|---|--8|
    |--6|7-8|2--|
    -------------
    |--2|6-9|5--|
    |8--|2-3|--9|
    |--5|-1-|3--|
    -------------
    Optimized
    -------------
    |9--|3-5|--1|
    |--1|8-6|4--|
    |--3|-2-|6--|
    -------------
    |8--|2-3|--9|
    |--2|6-9|5--|
    |--5|-1-|3--|
    -------------
    |7--|---|--8|
    |--8|1-2|9--|
    |--6|7-8|2--|
    -------------


## Untransforming Boards ##
The user may want to see the untransformed (or de-optimized) version of a board in order to compare to some other output. The `unoptimize` and `unoptimized` methods perform this operation or perform it on and return a copy, respectively.


```python
print("Not Transformed",board,"Un un transformed",board.optimized().unoptimized(),sep='\n')
```

    Not Transformed
    -------------
    |--3|-2-|6--|
    |9--|3-5|--1|
    |--1|8-6|4--|
    -------------
    |--8|1-2|9--|
    |7--|---|--8|
    |--6|7-8|2--|
    -------------
    |--2|6-9|5--|
    |8--|2-3|--9|
    |--5|-1-|3--|
    -------------
    Un un transformed
    -------------
    |--3|-2-|6--|
    |9--|3-5|--1|
    |--1|8-6|4--|
    -------------
    |--8|1-2|9--|
    |7--|---|--8|
    |--6|7-8|2--|
    -------------
    |--2|6-9|5--|
    |8--|2-3|--9|
    |--5|-1-|3--|
    -------------


## Iterative Solving ##
The `populate` method of the SudokuBoard object fills in all the freebies. It is called automatically by the `optimize` method. It is often useful to call it by itself as it returns the number of freebies it filled in.


```python
new_board = board.clone() #the clone method returns a deep copy of a board
while new_board.populate() != 0:
    pass #do nothing, populate() handles all the work
print(new_board)
```

    -------------
    |483|921|657|
    |967|345|821|
    |251|876|493|
    -------------
    |548|132|976|
    |729|564|138|
    |136|798|245|
    -------------
    |372|689|514|
    |814|253|769|
    |695|417|382|
    -------------


The `populate()` method also has an optional `max_depth` argument which specifies the maximum  number of times it the board will try to populate itself. A value of 0 means it will try until it reaches a step in which 0 freebies are filled.


```python
new_board = board.clone()
new_board.populate(max_depth=1)
print(new_board)
```

    -------------
    |--3|-2-|6--|
    |9--|3-5|--1|
    |--1|8-6|4--|
    -------------
    |--8|1-2|9--|
    |7--|--4|1-8|
    |--6|7-8|2--|
    -------------
    |--2|6-9|5-4|
    |8--|2-3|7-9|
    |--5|417|3--|
    -------------


# Advanced Usage #
This section covers usage involving backtracking and multiple processes.

## Solving with One Function ##
The function `solve_list` is provided to facilitate multi-processed backtracking for solving a board.


```python
#recall that board was constructed from board_list
out = solve_list(board_list,size=9,num_processes=4)
print("Unsolved",board,"Solved", out,sep='\n')
```

    Unsolved
    -------------
    |--3|-2-|6--|
    |9--|3-5|--1|
    |--1|8-6|4--|
    -------------
    |--8|1-2|9--|
    |7--|---|--8|
    |--6|7-8|2--|
    -------------
    |--2|6-9|5--|
    |8--|2-3|--9|
    |--5|-1-|3--|
    -------------
    Solved
    -------------
    |483|921|657|
    |967|345|821|
    |251|876|493|
    -------------
    |548|132|976|
    |729|564|138|
    |136|798|245|
    -------------
    |372|689|514|
    |814|253|769|
    |695|417|382|
    -------------


# Performance #
I am running this on my laptop with an i7 and 8GB of RAM.
The number of process is actually the number of child processes that are performing the backtracking. There are two more, one that manages access to shared objects in memory and the other is the main process.


```python
import time
for i in range(4,12+1):
    ti = time.time()
    solve_list(board_list,size=9,num_processes=i)
    print(i,"processes:","{:.4f} seconds".format(time.time() - ti))
```

    4 processes: 0.4594 seconds
    5 processes: 0.5675 seconds
    6 processes: 0.6694 seconds
    7 processes: 0.7720 seconds
    8 processes: 0.9000 seconds
    9 processes: 1.0117 seconds
    10 processes: 1.1081 seconds
    11 processes: 1.1992 seconds
    12 processes: 1.2964 seconds


## Performance Analysis ## 
 The particular board I have been demoing is relatively easy and can be solved using logic only. As such, adding more processes increases overhead for no particular benefit, as you may have noticed by the solve time increasing with the number of processes. However, there do exist boards that are difficult enough to merit multiprocessing. For example, the "hardest sudoku board ever"


```python
hardest = ("800000000"
           "003600000"
           "070090200"
           "050007000"
           "000045700"
           "000100030"
           "001000068"
           "008500010"
           "090000400")
bb = board_from_string(hardest)
print(bb)
print("Num. filled in:",len([i for i in hardest if i != '0']))
```

    -------------
    |8--|---|---|
    |--3|6--|---|
    |-7-|-9-|2--|
    -------------
    |-5-|--7|---|
    |---|-45|7--|
    |---|1--|-3-|
    -------------
    |--1|---|-68|
    |--8|5--|-1-|
    |-9-|---|4--|
    -------------
    Num. filled in: 21


This particular board is extremely difficult and requires several layers of guessing before any cells can be filled in with logic. Notice that no freebies are found:


```python
print("Num. freebies:",bb.populate())
```

    Num. freebies: 0


Beause we already have a board object we will use the solve_sudoku function instead of solve_list. The same benchmarking process as before is repeated. these numbers are completely system dependent but should demonstrate that there is an optimal number of child processes for a given task on a given system.


```python
for i in range(4,12+1):
    ti = time.time()
    solve_sudoku(bb,num_processes=i)
    tf = time.time()
    print(i,"processes:","{:.4f} seconds".format(tf - ti))
```

    4 processes: 8.4966 seconds
    5 processes: 5.4864 seconds
    6 processes: 8.6744 seconds
    7 processes: 7.3742 seconds
    8 processes: 6.9449 seconds
    9 processes: 9.9659 seconds
    10 processes: 7.8037 seconds


On average I get the best performance with 10 child processes.


```python

```
