#!/bin/bash
pydoc3 -w sudoku_solving
jupyter nbconvert --to markdown Demo.ipynb
jupyter nbconvert --to html Demo.ipynb