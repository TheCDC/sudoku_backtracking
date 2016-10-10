
# sudoku_solving Library Demo #
As always, import the library.


```python
from sudoku_solving import *
```

# Usage #
Boards can be created form strings or lists. The size of the board is assumed to be 9x9, unless specified otherwise.


```python
board_str = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
board = board_from_string(board_str)
print(board)
```

    
    -------------
    |003|020|600|
    |900|305|001|
    |001|806|400|
    -------------
    |008|102|900|
    |700|000|008|
    |006|708|200|
    -------------
    |002|609|500|
    |800|203|009|
    |005|010|300|
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
    |003|020|600|
    |900|305|001|
    |001|806|400|
    -------------
    |008|102|900|
    |700|000|008|
    |006|708|200|
    -------------
    |002|609|500|
    |800|203|009|
    |005|010|300|
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
    |10|30|
    |04|02|
    -------
    |20|40|
    |03|01|
    -------


# Solution Checking #
Boards may also be checked for legalityanf finality with the `check` and `check_partial` methods.


```python
print("4x4 maybe still solvable?",b.check_partial(),"4x4 already solved?",b.check(),sep='\n')
```

    4x4 maybe still solvable?
    True
    4x4 already solved?
    False



```python
print("9x9 maybe still solvable?",board.check_partial(),"9x9 already solved?",board.check(),sep='\n')
```

    9x9 maybe still solvable?
    True
    9x9 already solved?
    False


# Board Transformation #
Some boards are more difficult to solve and some are less. Some of those boards are the same. The `optimize` and `optimized` methods transform a board to optimize it or return the optimized version, respectively.

Those methods first fill in any freebies (cells with only one candidate) then sort the rows by their information density towards the left.


```python
print("Old",b,"New",b.optimized(),sep='\n')
```

    Old
    
    -------
    |10|30|
    |04|02|
    -------
    |20|40|
    |03|01|
    -------
    New
    
    -------
    |12|34|
    |34|12|
    -------
    |21|43|
    |43|21|
    -------



```python
print("Old",board,"New",board.optimized(),sep='\n')
```

    Old
    
    -------------
    |003|020|600|
    |900|305|001|
    |001|806|400|
    -------------
    |008|102|900|
    |700|000|008|
    |006|708|200|
    -------------
    |002|609|500|
    |800|203|009|
    |005|010|300|
    -------------
    New
    
    -------------
    |804|253|709|
    |695|417|302|
    |002|689|514|
    -------------
    |907|345|821|
    |001|876|400|
    |003|921|600|
    -------------
    |709|504|108|
    |008|102|900|
    |006|708|200|
    -------------


# Untransforming Boards #
The user may want to see the untransformed (or de-optimized) version of a board in order to compare to some other output. The `unoptimize` and `unoptimized` methods perform this operation or perform it on and return a copy, respectively.


```python
print("Old",board,"New",board.optimized().unoptimized(),sep='\n')
```

    Old
    
    -------------
    |003|020|600|
    |900|305|001|
    |001|806|400|
    -------------
    |008|102|900|
    |700|000|008|
    |006|708|200|
    -------------
    |002|609|500|
    |800|203|009|
    |005|010|300|
    -------------
    New
    
    -------------
    |003|921|600|
    |907|345|821|
    |001|876|400|
    -------------
    |008|102|900|
    |709|504|108|
    |006|708|200|
    -------------
    |002|689|514|
    |804|253|709|
    |695|417|302|
    -------------


# Solving with One Function #
The function `solve_list` is provided to facilitate multi-processed backtracking for solving a board.


```python
#recall that board was constructed from board_list
out = solve_list(board_list,size=9,num_processes=4)
print("Unsolved",board,"Solved", out,sep='\n')
```

    Unsolved
    
    -------------
    |003|020|600|
    |900|305|001|
    |001|806|400|
    -------------
    |008|102|900|
    |700|000|008|
    |006|708|200|
    -------------
    |002|609|500|
    |800|203|009|
    |005|010|300|
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



```python

```
