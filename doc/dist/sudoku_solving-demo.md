
# Introduction #
**By Christopher Chen**

This is a demonstration of my sudoku_solving Python library. It lives at [https://github.com/TheCDC/sudoku_backtracking](https://github.com/TheCDC/sudoku_backtracking)

It has routines for:

 1. Creating Sudoku board objects
 
 2. Manipulating boards to make solving easier
 
 4. getting/setting the values of cells on boards
 
 5. Populating the freebies
 
 6. Solving boards using multiprocessed backtracking.

Skip to the end for a breakdown of the solving strategy.


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
print("Not Transformed",board,"Transform and undo",board.optimized().unoptimized(),sep='\n')
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


## Iterative Solving with Logic ##
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

    4 processes: 0.0278 seconds
    5 processes: 0.0332 seconds
    6 processes: 0.0515 seconds
    7 processes: 0.0363 seconds
    8 processes: 0.0553 seconds
    9 processes: 0.0722 seconds
    10 processes: 0.0813 seconds
    11 processes: 0.0614 seconds
    12 processes: 0.0651 seconds


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
print("Num. already filled in:",len([i for i in hardest if i != '0']))
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
    Num. already filled in: 21


This particular board is extremely difficult and requires several layers of guessing before any cells can be filled in with logic. Notice that no freebies are found:


```python
print("Num. freebies:",bb.populate())
```

    Num. freebies: 0


Beause we already have a board object we will use the solve_sudoku function instead of solve_list. The same benchmarking process as before is repeated. these numbers are completely system dependent but should demonstrate that there is an optimal number of child processes for a given task on a given system.


```python
for i in range(4,16+1):
    ti = time.time()
    solve_sudoku(bb,num_processes=i)
    tf = time.time()
    print(i,"processes:","{:.4f} seconds".format(tf - ti))
```

    4 processes: 2.4859 seconds
    5 processes: 10.0220 seconds
    6 processes: 5.0304 seconds
    7 processes: 5.8383 seconds
    8 processes: 4.2815 seconds
    9 processes: 5.9268 seconds
    10 processes: 6.0324 seconds
    11 processes: 4.1717 seconds
    12 processes: 0.6664 seconds
    13 processes: 1.2861 seconds
    14 processes: 2.1656 seconds
    15 processes: 5.4176 seconds
    16 processes: 1.9314 seconds


On average I get the most consistently good performance with 10 child processes. These numbers are auto-generated based on the machine that produced the docs which may sometimes introduce some variance.

# Solving Strategy Breakdown #

The naive way to solve a sudoku board is to brute-force test all possible permutations. The number of board to test with this method is 9^(num. empty spaces). That's no fun.

Backtracking is applicable to problems for which you can produce partial solutions that fail fast and before you have even built a sequence of desired length. The `check_partial()` method allows for this.

Logic is the common human method of solving boards, that is finding all possible candidates for all cells and filling in cells who only have a single candidate and repeating.

I use both of these methods.

## Part 1 ##

Step 1 is always to exhaust freebies. Each freebie eliminates an entire branch ofthe possibility tree.

## Part 2 ##

The aforementioned techniques put together were succeessful in guaranteeing solutions, however, for the "hardest board in the world" took...well, hours before I killed the program. Easier boards such as the other ones used in this document took multiple minutes solve. This was not tractable.

Another method of board solving was introduced, this is the in the `optimize()` method.

### Pruning Trees ###

Backtracking is the practice of traversing the entire possibility tree but pruning impossible branches along the way. My board solving starts at the top left of the board and continues to the right then the next row and so on. This starting point is arbitrary, but you have to start somewhere. Imagine the first row is completely empty: "000000000". that means that the first nine levels of the possibility tree are all empty, that's 9^9(ish) partial solutions that have to be considered before you discover any shortcuts!

Now imagine that that board ended with the row "123456789". What if I told you you could flip this board on its head and that would give you an easier problem for free? Some boards are easy and some of them are hard and some of those are the same. If the board would instead start with the wholly populated row then that would eliminate...a LOT of work!

### Lifting Weights ## #

The row sorting strategy purposes to concentrate the most possible information earlier in the sequence. The row weighting function uses this line: `sum((i != 0) / (index + 1) for index, i in enumerate(r)) / len(r)`. This procedure heavily skews the weight to prefer rows that have a number in ths first column. This is intentional because of the aforementioned tree pruning. The rows are sorted in descending order by weight and their original order is remembered.

Theoretically, if you applied this function to rows of differing length, it would often prefer the shorter row.

TL;DR optimized boards are MUCH faster to solve because you get more information earlier in the backtracking process.

## Part 3 ##

Profit.


```python

```
