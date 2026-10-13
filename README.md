# Puzzle Solver

<img width="560" height="960" alt="2026-10-13 12 24 08" src="https://github.com/user-attachments/assets/ecffa270-ec1f-4faa-9260-93ccf99f0727" />

## Story

I try to apply what I learnt in CS2109S Introduction to Machine Learning in real life. I encountered a puzzle game and use python to formulate a search problem. Informally, the search problem is DFS with branching factor 8 x 8 grid and 8 puzzle pieces. 

## Thought process
Searching naively piece by piece is too slow and does too much redundant work. I try to speed up the search by using the piece that has the least number of legal moves. E.g. I sort the pieces by size (length * breadth) and use the largest piece first. 

I also used bit mask techniques (E.g. 8 x 8 grid can fit into 64-bit integer) which reduced the time taken from 1-5s to ~100ms.

Reference(s)
Donald Knuth : Dancing Links, Algorithm X
Instruction manual for the puzzle
