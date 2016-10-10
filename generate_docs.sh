#!/bin/bash
cd doc/
./generate_docs.sh
cd ..
cat README_head.md > README.md
cat doc/dist/sudoku_solving-demo.md >> README.md