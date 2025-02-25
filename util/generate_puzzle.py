#!/usr/bin/env python
import os
import random
import subprocess
import sys


EXEC_DIR=os.path.expanduser('~/bin')
GEN_CMD=os.path.join(EXEC_DIR, 'sudoku-gen')
SOLVE_CMD=os.path.join(EXEC_DIR, 'sudoku-solve')


def generate():
    proc = subprocess.run([GEN_CMD], capture_output=True, timeout=10)
    raw = proc.stdout
    puzzle = raw.decode('utf-8')

    proc = subprocess.run([SOLVE_CMD], input=raw, capture_output=True)
    solution = proc.stdout.decode('utf-8')

    puzzle = [x.split() for x in puzzle.split('\n')]
    solution = [x.split() for x in solution.split('\n')]

    result = []
    masked = set()
    for i, line in enumerate(solution):
        for j, cell in enumerate(line):
            result.append(cell)
            if puzzle[i][j] == cell:
                result.append('*')
            else:
                masked.add(len(result))
                result.append(' ')

    hints = 4
    # The puzzle has a minimal mask, so unmask 4 additional cells
    for choice in random.sample(list(masked), hints):
        result[choice] = '*'

    print(''.join(result))


if __name__ == '__main__':
    n = int(sys.argv[1])
    while n > 0:
        try:
            generate()
            n -= 1
        except subprocess.TimeoutExpired:
            pass
