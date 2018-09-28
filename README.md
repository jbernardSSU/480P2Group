# CS480 Project 2
# Justin Bernard, Brandon Adamson-Rakidzich, Justin Moore

To run with testing statements:
python3 p2.py [option 1, 2 or 3 to print various testing statements]

To run without:
python3 p2.py

- User will be asked to enter a permutation, which can be done on a
  single line as follows:

  5 3 1 4 2

  (i.e. your chosen numbers, with spaces in between)

  Our program will then proceed to run IDS and BFS algorithms on that
  permutation, printing the path to the goal node, along with the #
  of nodes visited, and the max queue size.

- Program has been tested with permutations of up to 8 numbers, such as:

  7 3 1 4 6 2 5 (which took ~7 seconds for BFS, ~2 seconds for DFS)
  8 4 2 5 3 7 1 6 (~3.5 minutes for BFS, ~9 seconds for DFS)

  These inputs were chosen because every value is in an incorrect position
  within the permutation, and also, no value has a correct neighbor either,
  making it a difficult input to sort by reversal.

  Attempting to test an input of 9 numbers may take up to an hour or more
  based on our earlier results, or, run out of space.