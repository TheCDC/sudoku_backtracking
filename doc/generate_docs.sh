#!/bin/bash
pydoc3 -w sudoku_solving
jupyter nbconvert --to markdown "Demo of sudoku_solving.ipynb" --output dist/sudoku_solving-demo.md
jupyter nbconvert --to html "Demo of sudoku_solving.ipynb" --output dist/sudoku_solving-demo.html
jupyter nbconvert --to pdf --template report "Demo of sudoku_solving.ipynb" --output dist/sudoku_solving-demo