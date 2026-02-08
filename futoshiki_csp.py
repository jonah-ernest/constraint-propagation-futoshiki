# Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary
      all-different constraints for both the row and column constraints.
    
    The input board is specified as a list of n lists. Each of the n lists
    represents a row of the board. If a 0 is in the list it represents an empty
    cell. Otherwise if a number between 1--n is in the list then this
    represents a pre-set board position.

    Each list is of length 2n-1, with each space on the board being separated
    by the potential inequality constraints. '>' denotes that the previous
    space must be bigger than the next space; '<' denotes that the previous
    space must be smaller than the next; '.' denotes that there is no
    inequality constraint.

    E.g., the board

    -------
    | > |2|
    | | | |
    | | < |
    -------
    would be represented by the list of lists

    [[0,>,0,.,2],
     [0,.,0,.,0],
     [0,.,0,<,0]]

'''
import cspbase
import itertools


def futoshiki_csp_model_1(futo_grid):
    '''Model using only binary not-equal constraints and binary inequality constraints'''

    n = len(futo_grid)
    csp = cspbase.CSP("Futoshiki_Model_1")
    variables = []
    
    # Step 1: Create variables
    for i in range(n):
        row = []
        for j in range(0, 2 * n - 1, 2):
            # If the cell is 0, it is unassigned, so the domain is [1..n]
            if futo_grid[i][j] == 0:
                domain = list(range(1, n + 1))
            else:
                # Otherwise, the cell is pre-assigned with a specific value
                domain = [futo_grid[i][j]]
            
            var = cspbase.Variable(f"V{i}{j//2}", domain)
            row.append(var)
            csp.add_var(var)
        variables.append(row)

    # Step 2: Add binary constraints for rows
    for i in range(n):
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                var1 = variables[i][j1]
                var2 = variables[i][j2]
                constraint = cspbase.Constraint(f"Row{i}_NotEqual_{j1}{j2}", [var1, var2])
                
                # Create satisfying tuples for not-equal constraint
                sat_tuples = [(val1, val2) for val1 in var1.cur_domain() for val2 in var2.cur_domain() if val1 != val2]
                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)

    # Step 3: Add binary constraints for columns
    for j in range(n):
        for i1 in range(n):
            for i2 in range(i1 + 1, n):
                var1 = variables[i1][j]
                var2 = variables[i2][j]
                constraint = cspbase.Constraint(f"Col{j}_NotEqual_{i1}{i2}", [var1, var2])
                
                # Create satisfying tuples for not-equal constraint
                sat_tuples = [(val1, val2) for val1 in var1.cur_domain() for val2 in var2.cur_domain() if val1 != val2]
                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)

    # Step 4: Add inequality constraints
    for i in range(n):
        for j in range(1, 2 * n - 1, 2):
            constraint_symbol = futo_grid[i][j]
            if constraint_symbol in ['<', '>']:
                var1 = variables[i][j // 2]
                var2 = variables[i][j // 2 + 1]
                constraint = cspbase.Constraint(f"Inequality_{i}_{j // 2}_{j // 2 + 1}", [var1, var2])
                
                if constraint_symbol == '<':
                    sat_tuples = [(val1, val2) for val1 in var1.cur_domain() for val2 in var2.cur_domain() if val1 < val2]
                else:  # constraint_symbol == '>'
                    sat_tuples = [(val1, val2) for val1 in var1.cur_domain() for val2 in var2.cur_domain() if val1 > val2]

                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)

    return csp, variables


def futoshiki_csp_model_2(futo_grid):
    n = len(futo_grid)
    variables = []
    csp = cspbase.CSP("Futoshiki_Model_2")

    # Step 1: Create variables
    for i in range(n):
        row = []
        for j in range(0, 2 * n - 1, 2):
            if futo_grid[i][j] == 0:
                domain = list(range(1, n + 1))
            else:
                domain = [futo_grid[i][j]]
            
            var = cspbase.Variable(f"V{i}{j//2}", domain)
            row.append(var)
            csp.add_var(var)
        variables.append(row)

    # Step 2: Add n-ary all-different constraints for rows
    for i in range(n):
        row_vars = variables[i]
        constraint = cspbase.Constraint(f"Row_AllDiff_{i}", row_vars)
        
        # Generate all satisfying tuples where all values are different
        sat_tuples = [tup for tup in itertools.permutations(range(1, n + 1), n)]
        constraint.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(constraint)

    # Step 3: Add n-ary all-different constraints for columns
    for j in range(n):
        col_vars = [variables[i][j] for i in range(n)]
        constraint = cspbase.Constraint(f"Col_AllDiff_{j}", col_vars)
        
        # Generate all satisfying tuples where all values are different
        sat_tuples = [tup for tup in itertools.permutations(range(1, n + 1), n)]
        constraint.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(constraint)

    # Step 4: Add binary inequality constraints for rows (horizontal only)
    for i in range(n):
        for j in range(1, 2 * n - 1, 2):
            constraint_symbol = futo_grid[i][j]
            if constraint_symbol in ['<', '>']:
                var1 = variables[i][j // 2]
                var2 = variables[i][j // 2 + 1]
                constraint = cspbase.Constraint(f"Inequality_{i}_{j // 2}_{j // 2 + 1}", [var1, var2])
                
                if constraint_symbol == '<':
                    sat_tuples = [(val1, val2) for val1 in var1.cur_domain() for val2 in var2.cur_domain() if val1 < val2]
                else:  # constraint_symbol == '>'
                    sat_tuples = [(val1, val2) for val1 in var1.cur_domain() for val2 in var2.cur_domain() if val1 > val2]

                constraint.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(constraint)

    return csp, variables