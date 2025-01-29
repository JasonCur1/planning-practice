from unified_planning.shortcuts import *
from unified_planning.model.problem import Problem
from unified_planning.engines import PlanGenerationResultStatus
from unified_planning.model.metrics import *

def create_city_car_problem():
    # Domain
    problem = Problem('citycar')

    # Types
    car = UserType('car')
    junction = UserType('junction')
    garage = UserType('garage')
    road = UserType('road')

    # Predicates/Fluents
    same_line = Fluent('same_line', BoolType(), xy=junction, xy2=junction) # Junctions in line (row)
    diagonal = Fluent('diagonal', BoolType(), x=junction, y=junction) # Junctions in diagonal (on the map)
    at_car_jun = Fluent('at_car_jun', BoolType(), c=car, x=junction) # A car is at the junction
    at_car_road = Fluent('at_car_road', BoolType(), c=car, x=road) # A car is in a road
    starting = Fluent('starting', BoolType(), c=car, x=garage) # A car is in its initial position
    arrived = Fluent('arrived', BoolType(), c=car, x=junction) # A car arrived at destination
    road_connect = Fluent('road_connect', BoolType(), r1=road, xy=junction, xy2=junction) # There is a road that connects 2 junctions
    clear = Fluent('clear', BoolType(), xy=junction) # The junction is clear
    in_place = Fluent('in_place', BoolType(), x=road) # The road has been put in place
    at_garage = Fluent('at_garage', BoolType(), g=garage, xy=junction) # Position of the starting garage
    #total_cost = Fluent('total-cost', IntType())

    # Add fluents with explicit default values
    problem.add_fluent(same_line, default_initial_value=False)
    problem.add_fluent(diagonal, default_initial_value=False)
    problem.add_fluent(at_car_jun, default_initial_value=False)
    problem.add_fluent(at_car_road, default_initial_value=False)
    problem.add_fluent(starting, default_initial_value=False)
    problem.add_fluent(arrived, default_initial_value=False)
    problem.add_fluent(road_connect, default_initial_value=False)
    problem.add_fluent(clear, default_initial_value=False)
    problem.add_fluent(in_place, default_initial_value=False)
    problem.add_fluent(at_garage, default_initial_value=False)
    #problem.add_fluent(total_cost, default_initial_value=Int(0))

    # Actions
    # Move car in road
    move_car_in_road = InstantaneousAction('move_car_in_road', xy_initial=junction, xy_final=junction, machine=car, r1=road)
    xyi, xyf, m, r = move_car_in_road.parameters
    move_car_in_road.add_precondition(at_car_jun(m, xyi))
    move_car_in_road.add_precondition(road_connect(r, xyi, xyf))
    move_car_in_road.add_precondition(in_place(r))
    move_car_in_road.add_effect(clear(xyi), True)
    move_car_in_road.add_effect(at_car_road(m, r), True)
    move_car_in_road.add_effect(at_car_jun(m, xyi), False)
    #move_car_in_road.add_effect(total_cost, total_cost + 1)
    problem.add_action(move_car_in_road)

    # Move car out of road
    move_car_out_road = InstantaneousAction('move_car_out_road', xy_initial=junction, xy_final=junction, machine=car, r1=road)
    xyi, xyf, m, r = move_car_out_road.parameters
    move_car_out_road.add_precondition(at_car_road(m, r))
    move_car_out_road.add_precondition(clear(xyf))
    move_car_out_road.add_precondition(road_connect(r, xyi, xyf))
    move_car_out_road.add_precondition(in_place(r))
    move_car_out_road.add_effect(at_car_jun(m, xyf), True)
    move_car_out_road.add_effect(clear(xyf), False)
    move_car_out_road.add_effect(at_car_road(m, r), False)
    #move_car_out_road.add_effect(total_cost, total_cost + 1)
    problem.add_action(move_car_out_road)

    # Car arrived
    car_arrived = InstantaneousAction('car_arrived', xy_final=junction, machine=car)
    xyf, m = car_arrived.parameters
    car_arrived.add_precondition(at_car_jun(m, xyf))
    car_arrived.add_effect(clear(xyf), True)
    car_arrived.add_effect(arrived(m, xyf), True)
    car_arrived.add_effect(at_car_jun(m, xyf), False)
    # No cost for car_arrived
    problem.add_action(car_arrived)

    # Car start
    car_start = InstantaneousAction('car_start', xy_final=junction, machine=car, g=garage)
    xyf, m, g = car_start.parameters
    car_start.add_precondition(at_garage(g, xyf))
    car_start.add_precondition(starting(m, g))
    car_start.add_precondition(clear(xyf))
    car_start.add_effect(clear(xyf), False)
    car_start.add_effect(at_car_jun(m, xyf), True)
    car_start.add_effect(starting(m, g), False)
    # No cost for car_start
    problem.add_action(car_start)

    # Build diagonal road
    build_diagonal_oneway = InstantaneousAction('build_diagonal_oneway', xy_initial=junction, xy_final=junction, r1=road)
    xyi, xyf, r = build_diagonal_oneway.parameters
    build_diagonal_oneway.add_precondition(clear(xyf))
    build_diagonal_oneway.add_precondition(Not(in_place(r)))
    build_diagonal_oneway.add_precondition(diagonal(xyi, xyf))
    build_diagonal_oneway.add_effect(road_connect(r, xyi, xyf), True)
    build_diagonal_oneway.add_effect(in_place(r), True)
    #build_diagonal_oneway.add_effect(total_cost, total_cost + 30)
    problem.add_action(build_diagonal_oneway)

    # Build straight road
    build_straight_oneway = InstantaneousAction('build_straight_oneway', xy_initial=junction, xy_final=junction, r1=road)
    xyi, xyf, r = build_straight_oneway.parameters
    build_straight_oneway.add_precondition(clear(xyf))
    build_straight_oneway.add_precondition(same_line(xyi, xyf))
    build_straight_oneway.add_precondition(Not(in_place(r)))
    build_straight_oneway.add_effect(road_connect(r, xyi, xyf), True)
    build_straight_oneway.add_effect(in_place(r), True)
    #build_straight_oneway.add_effect(total_cost, total_cost + 20)
    problem.add_action(build_straight_oneway)

    # Destroy road
    destroy_road = InstantaneousAction('destroy_road', xy_initial=junction, xy_final=junction, r1=road)
    xyi, xyf, r = destroy_road.parameters
    destroy_road.add_precondition(road_connect(r, xyi, xyf))
    destroy_road.add_precondition(in_place(r))
    destroy_road.add_effect(in_place(r), False)
    destroy_road.add_effect(road_connect(r, xyi, xyf), False)
    #destroy_road.add_effect(total_cost, total_cost + 10)
    
    # Handle cars on destroyed road
    c = Variable('c', car)
    destroy_road.add_effect(at_car_road(c, r), False, at_car_road(c, r), forall=[c])
    destroy_road.add_effect(at_car_jun(c, xyi), True, at_car_road(c, r), forall=[c])
    problem.add_action(destroy_road)

    # Add costs for each action
    costs = {
        move_car_in_road: 1,
        move_car_out_road: 1,
        car_arrived: 0,  # Add cost for all actions
        car_start: 0,
        build_diagonal_oneway: 30,
        build_straight_oneway: 20,
        destroy_road: 10
    }
    problem.add_quality_metric(MinimizeActionCosts(costs))

    
    # Instance
    # Objects
    j00 = Object('junction0-0', junction)
    j01 = Object('junction0-1', junction)
    j10 = Object('junction1-0', junction)
    j11 = Object('junction1-1', junction)
    problem.add_objects([j00, j01, j10, j11])

    car0 = Object('car0', car)
    car1 = Object('car1', car)
    problem.add_objects([car0, car1])

    garage0 = Object('garage0', garage)
    problem.add_objects([garage0])

    road0 = Object('road0', road)
    road1 = Object('road1', road)
    road2 = Object('road2', road)
    road3 = Object('road3', road)
    problem.add_objects([road0, road1, road2, road3])

    # Initial states
    # Same Line Connections
    problem.set_initial_value(same_line(j00, j01), True)
    problem.set_initial_value(same_line(j01, j00), True)
    problem.set_initial_value(same_line(j10, j11), True)
    problem.set_initial_value(same_line(j11, j10), True)
    problem.set_initial_value(same_line(j00, j10), True)
    problem.set_initial_value(same_line(j10, j00), True)
    problem.set_initial_value(same_line(j01, j11), True)
    problem.set_initial_value(same_line(j11, j01), True)

    # Diagonal Connections
    problem.set_initial_value(diagonal(j00, j11), True)
    problem.set_initial_value(diagonal(j11, j00), True)
    problem.set_initial_value(diagonal(j01, j10), True)
    problem.set_initial_value(diagonal(j10, j01), True)

    # Clearing junctions
    problem.set_initial_value(clear(j00), True)
    problem.set_initial_value(clear(j01), True)
    problem.set_initial_value(clear(j10), True)
    problem.set_initial_value(clear(j11), True)

    # Garage and Cars
    problem.set_initial_value(at_garage(garage0, j01), True) # Set location of initial garage
    problem.set_initial_value(starting(car0, garage0), True)
    problem.set_initial_value(starting(car1, garage0), True)

    # Goals
    problem.add_goal(arrived(car0, j11))
    problem.add_goal(arrived(car1, j10))

    # # Add minimize total-cost metric
    # problem.add_quality_metric(MinimizeExpression(total_cost))

    return problem



print("Available planners:", get_environment().factory.engines)

# Create and solve problem
problem = create_city_car_problem()

print("\nTrying optimal solver:")
with OneshotPlanner(name='fast-downward-opt', 
                   problem_kind=problem.kind) as optimal_planner:
    result = optimal_planner.solve(problem)
    if result.status in [PlanGenerationResultStatus.SOLVED_OPTIMALLY, PlanGenerationResultStatus.SOLVED_SATISFICING]:
        if result.plan:
            print("Optimal solution found:", result.plan)
            total_cost = sum(1 for _ in result.plan.actions)
            print("Number of actions:", total_cost)
        else:
            print("Solver returned success but no plan was found (this should not happen)")
    else:
        print("No optimal solution found")
        print("Status:", result.status)
        print("Engine name:", result.engine_name)
        if hasattr(result, 'log'):
            print("Log:", result.log)
        if hasattr(result, 'metric_value'):
            print("Metric value:", result.metric_value)

# Try regular solver for comparison
print("\nTrying regular solver:")
with OneshotPlanner(problem_kind=problem.kind) as planner:
    result = planner.solve(problem)
    if result:
        print("Solution found:", result.plan)
        if result.plan:
            total_cost = sum(1 for _ in result.plan.actions)  # Basic action count
            print("Number of actions:", total_cost)
    else:
        print("No solution found")

# with OneshotPlanner(name='fast-downward-opt', problem_kind=problem.kind, optimality_guarantee=PlanGenerationResultStatus.SOLVED_OPTIMALLY) as optimal_planner:
#     result = optimal_planner.solve(problem)
#     print("Engine returned: %s" % result.plan)



# with OneshotPlanner(problem_kind=problem.kind) as planner:
#     result = planner.solve(problem)
#     print("Engine returned: %s" % result.plan)