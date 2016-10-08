Solving sudoku puzzles with backtracking.

# Setup #
Meh.

# Run it #
`./sudoku.py` on *nix or `python sudoku.py` on Windows. Doing this will have it run whatever test board I currently have it set to solve. Eventually there will be a proper interface/API.

# Lessons Learned #
Backtracking is pretty cool by itself, but it alone doesn't prune the possibility tree quite enough.
I learned that you have to manipulate your data so that information is concentrated at the root of the tree as much as possible.

I did this by "optimizing" the Sudoku boards by weighting each row in a row of quadrants by the measure of how well filled in cells were concentrated towards the beginning of that row. The measure is a formula is a came up with where a bigger number is better. The rows are then sorted in descending order. The original order the rows is also tracked.

Sorting the rows like this increases the allows more possibilities to be eliminated faster.

# Acknowledgements #
A big thank you to Aaron Renfroe for figuring out the information density bit.