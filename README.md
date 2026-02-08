# Futoshiki CSP Solver with Constraint Propagation and Heuristics

This project explores how **constraint satisfaction problems (CSPs)** can be used to model and efficiently solve structured logic puzzles. I implement core CSP search techniques and apply them to the game **Futoshiki**, comparing alternative modeling choices and propagation strategies.

Rather than treating the puzzle as a brute-force search task, the solver relies on constraint reasoning to aggressively prune the search space before and during backtracking.

## Background

### Constraint Satisfaction Problems

A constraint satisfaction problem consists of:
- a set of **variables**
- a domain of possible values for each variable
- a collection of **constraints** restricting which assignments are allowed

CSP solvers typically use **backtracking search** combined with:
- **constraint propagation** (to remove inconsistent values early)
- **variable-ordering heuristics** (to decide what to assign next)

These techniques are widely used in scheduling, planning, timetabling, and resource allocation.

### The Futoshiki Puzzle

Futoshiki is a Latin-square–style puzzle played on an (n x n) grid:
- each row and column must contain distinct numbers
- some pairs of cells include **inequality constraints** (e.g., \( X > Y \))

This structure makes it a natural benchmark for CSP modeling and propagation algorithms.

## Project Goals

The main objectives were:

- implement reusable CSP propagation mechanisms
- compare different modeling strategies for the same problem
- study how propagation strength affects search efficiency

Specifically, the project includes:

- **Forward Checking (FC)**  
- **Generalized Arc Consistency (GAC)**  
- **Minimum Remaining Values (MRV)** variable ordering  
- two alternative CSP encodings of the puzzle

## Implemented Components

### Constraint Propagation

Two propagation strategies are implemented:

- **Forward Checking:** prunes values when a constraint has exactly one unassigned variable remaining.
- **Generalized Arc Consistency:** enforces arc consistency by repeatedly removing unsupported values from variable domains.

### Variable Ordering

- **MRV (Minimum Remaining Values):** selects the next variable with the smallest remaining domain to reduce branching early.

### CSP Encodings

Two different formulations of Futoshiki are provided:

- **Binary model:** pairwise inequality constraints between cells in the same row or column.
- **All-different model:** n-ary constraints enforcing row/column uniqueness, plus inequality relations.

These allow direct comparison of how modeling choices influence propagation strength and solver behavior.

## Repository Contents

- `propagators.py` — Forward Checking, GAC propagation, and MRV heuristic
- `futoshiki_csp.py` — CSP model builders for the two puzzle encodings
- `cspbase.py` — CSP primitives and backtracking engine (support code)
- `csp_sample_run.py` — small driver / demonstration script
