# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''


def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    pruned = []

    # Get the relevant constraints to check
    if newVar is None:
        constraints_to_check = csp.get_all_cons()
    else:
        constraints_to_check = csp.get_cons_with_var(newVar)

    # Iterate through each constraint
    for constraint in constraints_to_check:
        # Only consider constraints with exactly one unassigned variable
        if constraint.get_n_unasgn() == 1:
            unasgn_var = constraint.get_unasgn_vars()[0]

            # Iterate through the current domain of the unassigned variable
            for value in unasgn_var.cur_domain():
                # Check if this value has a valid support
                if not constraint.has_support(unasgn_var, value):
                    # If not, prune the value and add to pruned list
                    unasgn_var.prune_value(value)
                    pruned.append((unasgn_var, value))

            # If the variable's domain is empty, return failure
            if unasgn_var.cur_domain_size() == 0:
                return False, pruned

    # Return success and the list of pruned values
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    pruned = []
    gac_queue = []

    # Initialize the GAC queue with the appropriate constraints
    if newVar is None:
        gac_queue = csp.get_all_cons()
    else:
        gac_queue = csp.get_cons_with_var(newVar)

    # While there are constraints to process in the GAC queue
    while gac_queue:
        # Dequeue the next constraint
        constraint = gac_queue.pop(0)

        # Iterate through all variables in the scope of the constraint
        for var in constraint.get_scope():
            # Iterate through each value in the current domain of the variable
            for value in var.cur_domain():
                # Check if there is support for this (var, value) pair
                if not constraint.has_support(var, value):
                    # If no support, prune the value and add to pruned list
                    var.prune_value(value)
                    pruned.append((var, value))

                    # If the variable's domain is empty, return failure
                    if var.cur_domain_size() == 0:
                        return False, pruned

                    # Add all constraints involving the variable back to the GAC queue
                    for related_constraint in csp.get_cons_with_var(var):
                        if related_constraint not in gac_queue:
                            gac_queue.append(related_constraint)

    # Return success and the list of pruned values
    return True, pruned

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # Get all unassigned variables
    unassigned_vars = csp.get_all_unasgn_vars()

    # Select the variable with the smallest domain size, and use 'min' with a custom key to avoid unnecessary loops
    mrv_var = min(unassigned_vars, key=lambda var: var.cur_domain_size(), default=None)

    return mrv_var