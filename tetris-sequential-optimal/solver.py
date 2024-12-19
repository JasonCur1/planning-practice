from unified_planning.shortcuts import *
from unified_planning.model.problem import Problem

def create_tetris_problem():
    # Types and fluents remain the same
    position = UserType("position")
    pieces = UserType("pieces")
    one_square = UserType("one_square", father=pieces)
    two_straight = UserType("two_straight", father=pieces)
    right_l = UserType("right_l", father=pieces)

    problem = Problem("tetris")

    # Define fluents
    clear = Fluent("clear", BoolType(), position=position)
    connected = Fluent("connected", BoolType(), x=position, y=position)
    at_square = Fluent("at_square", BoolType(), element=one_square, xy=position)
    at_two = Fluent("at_two", BoolType(), element=two_straight, xy=position, xy2=position)
    at_right_l = Fluent("at_right_l", BoolType(), element=right_l, xy=position, xy2=position, xy3=position)
    
    # Add fluents to problem
    problem.add_fluent(clear, default_initial_value=False)
    problem.add_fluent(connected, default_initial_value=False)
    problem.add_fluent(at_square, default_initial_value=False)
    problem.add_fluent(at_two, default_initial_value=False)
    problem.add_fluent(at_right_l, default_initial_value=False)

    # Create objects
    positions = []
    for i in range(6):
        for j in range(4):
            pos = Object(f"f{i}-{j}f", position)
            positions.append(pos)
            problem.add_object(pos)

    squares = [Object(f"square{i}", one_square) for i in range(3)]
    straights = [Object(f"straight{i}", two_straight) for i in range(2)]
    ls = [Object(f"rightl0", right_l)]

    for obj in squares + straights + ls:
        problem.add_object(obj)

    # Define simplified actions
    # Move square
    move_square = InstantaneousAction("move_square", xy_initial=position, xy_final=position, element=one_square)
    xi, xf, e = move_square.parameters
    move_square.add_precondition(clear(xf))
    move_square.add_precondition(at_square(e, xi))
    move_square.add_precondition(connected(xi, xf))
    move_square.add_effect(clear(xi), True)
    move_square.add_effect(at_square(e, xf), True)
    move_square.add_effect(clear(xf), False)
    move_square.add_effect(at_square(e, xi), False)
    problem.add_action(move_square)

    # Move two straight (with rotation)
    move_two = InstantaneousAction("move_two", xy_initial1=position, xy_initial2=position, 
                                  xy_final=position, element=two_straight)
    xi1, xi2, xf, e = move_two.parameters
    move_two.add_precondition(clear(xf))
    move_two.add_precondition(at_two(e, xi1, xi2))
    move_two.add_precondition(connected(xi2, xf))
    move_two.add_effect(clear(xi1), True)
    move_two.add_effect(at_two(e, xi2, xf), True)
    move_two.add_effect(clear(xf), False)
    move_two.add_effect(at_two(e, xi1, xi2), False)
    problem.add_action(move_two)

    # Move L right - simplified
    move_l_right = InstantaneousAction("move_l_right", 
        xy_initial1=position, xy_initial2=position, xy_initial3=position,
        xy_final=position, xy_final2=position, element=right_l)
    xi1, xi2, xi3, xf, xf2, e = move_l_right.parameters
    move_l_right.add_precondition(clear(xf))
    move_l_right.add_precondition(clear(xf2))
    move_l_right.add_precondition(at_right_l(e, xi1, xi2, xi3))
    move_l_right.add_precondition(connected(xi1, xf))
    move_l_right.add_precondition(connected(xi3, xf2))
    move_l_right.add_effect(clear(xi2), True)
    move_l_right.add_effect(clear(xi1), True)
    move_l_right.add_effect(at_right_l(e, xf, xi3, xf2), True)
    move_l_right.add_effect(clear(xf), False)
    move_l_right.add_effect(clear(xf2), False)
    move_l_right.add_effect(at_right_l(e, xi1, xi2, xi3), False)
    problem.add_action(move_l_right)

    # Move L left - simplified
    move_l_left = InstantaneousAction("move_l_left",
        xy_initial1=position, xy_initial2=position, xy_initial3=position,
        xy_final=position, xy_final2=position, element=right_l)
    xi1, xi2, xi3, xf, xf2, e = move_l_left.parameters
    move_l_left.add_precondition(clear(xf))
    move_l_left.add_precondition(clear(xf2))
    move_l_left.add_precondition(at_right_l(e, xi1, xi2, xi3))
    move_l_left.add_precondition(connected(xi1, xf))
    move_l_left.add_precondition(connected(xi2, xf2))
    move_l_left.add_precondition(connected(xf2, xf))
    move_l_left.add_effect(clear(xi3), True)
    move_l_left.add_effect(clear(xi1), True)
    move_l_left.add_effect(at_right_l(e, xf, xf2, xi2), True)
    move_l_left.add_effect(clear(xf), False)
    move_l_left.add_effect(clear(xf2), False)
    move_l_left.add_effect(at_right_l(e, xi1, xi2, xi3), False)
    problem.add_action(move_l_left)

    # Initialize the world
    # Horizontal connections
    for i in range(6):
        for j in range(3):
            problem.set_initial_value(connected(positions[i*4 + j], positions[i*4 + j + 1]), True)
            problem.set_initial_value(connected(positions[i*4 + j + 1], positions[i*4 + j]), True)

    # Vertical connections
    for i in range(5):
        for j in range(4):
            problem.set_initial_value(connected(positions[i*4 + j], positions[(i+1)*4 + j]), True)
            problem.set_initial_value(connected(positions[(i+1)*4 + j], positions[i*4 + j]), True)

    # Set clear positions
    clear_positions = [
        "f0-3f", "f2-3f", "f3-0f", "f3-1f", "f3-2f", "f3-3f",
        "f4-0f", "f4-1f", "f4-2f", "f4-3f",
        "f5-0f", "f5-1f", "f5-2f", "f5-3f"
    ]
    for pos_name in clear_positions:
        pos = problem.object(pos_name)
        problem.set_initial_value(clear(pos), True)

    # Set initial piece positions
    problem.set_initial_value(at_right_l(ls[0], problem.object("f0-2f"), problem.object("f1-2f"), problem.object("f1-3f")), True)
    problem.set_initial_value(at_two(straights[0], problem.object("f0-0f"), problem.object("f1-0f")), True)
    problem.set_initial_value(at_two(straights[1], problem.object("f0-1f"), problem.object("f1-1f")), True)
    problem.set_initial_value(at_square(squares[0], problem.object("f2-0f")), True)
    problem.set_initial_value(at_square(squares[1], problem.object("f2-1f")), True)
    problem.set_initial_value(at_square(squares[2], problem.object("f2-2f")), True)

    # Set goal state
    for i in range(3):
        for j in range(4):
            problem.add_goal(clear(positions[i*4 + j]))

    return problem

# Suppress credits printing
# up.shortcuts.get_environment().credits_stream = None

# Create and solve problem
problem = create_tetris_problem()
with OneshotPlanner(name='pyperplan') as planner:
    result = planner.solve(problem)
    if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
        print("Pyperplan returned: %s" % result.plan)
    else:
        print("No plan found.")