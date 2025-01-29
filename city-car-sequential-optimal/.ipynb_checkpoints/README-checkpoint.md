# City Car (Sequential, Optimal)

## Domain Description

This model aims to simulate the impact of road building/demolition on traffic flows.
A city is represented as an acyclic graph, in which each node is a junction and edges are “potential” roads.
Some cars start from different positions and have to reach their final destination as soon as possible.
The agent has a finite number of roads available, which can be built for connecting two junctions and allowing a car to move between them.
Roads can also be removed and placed somewhere else, if needed.
In order to place roads or to move cars, the destination junction must be clear, i. e., no cars should be in there.

## Authors

Mauro Vallati