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
