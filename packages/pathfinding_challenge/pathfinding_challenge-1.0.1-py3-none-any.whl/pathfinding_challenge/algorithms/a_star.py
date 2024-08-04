import heapq
import math
from typing import Dict, List, Tuple

from pathfinding_challenge.algorithms.path_finding import PathfindingStrategy
from pathfinding_challenge.entities.node import Node
from pathfinding_challenge.entities.position import Position


class AStarStrategy(PathfindingStrategy):
    allowed_directions = [
        Position(-1, 0),
        Position(0, -1),
        Position(0, 1),
        Position(1, 0),
    ]

    @staticmethod
    def heuristic(node1: Node, node2: Node) -> float:
        """
        Heuristic function estimating the cost from node1 to node2.
        Using the Manhattan distance.

        Args:
            node1 (Node): The starting node.
            node2 (Node): The target node.

        Returns:
            float: The estimated cost to reach node2 from node1.
        """
        return abs(node1.position.x - node2.position.x) + abs(
            node1.position.y - node2.position.y
        )

    @staticmethod
    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        """
        Retrieve the neighboring nodes for a given node in the grid.

        Args:
            grid (List[List[Node]]): The grid containing all nodes.
            node (Node): The current node whose neighbors are to be found.

        Returns:
            List[Node]: A list of neighboring nodes.
        """
        neighbors = []
        for direction in AStarStrategy.allowed_directions:
            new_position = node.position + direction
            if (0 <= new_position.x < len(grid)) and (
                0 <= new_position.y < len(grid[0])
            ):
                neighbor_node = grid[new_position.x][new_position.y]
                neighbors.append(neighbor_node)
        return neighbors

    @staticmethod
    def calculate_distance(node1: Node, node2: Node) -> float:
        """
        Calculate the path cost between two nodes.
        Uses Euclidean distance plus terrain fuel efficiency
        for accurate path cost.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            float: The path cost between the two nodes.
        """
        return (
            math.sqrt(
                (node2.position.x - node1.position.x) ** 2
                + (node2.position.y - node1.position.y) ** 2
            )
            + node2.weight
        )

    @staticmethod
    def find_path(
        grid: List[List[Node]], start: Node, end: Node
    ) -> List[Node]:
        """
        Find the shortest path from the start node to the end node using
        the A* algorithm.

        Args:
            grid (List[List[Node]]): The grid containing all nodes.
            start (Node): The starting node.
            end (Node): The destination node.

        Returns:
            List[Node]: The list of nodes representing the shortest path.
                        If no path is found, returns an empty list.
        """
        open_set: List[Tuple[float, Node]] = [(0, start)]
        came_from: Dict[Node, Node] = {}

        g_score: Dict[Node, float] = {start: 0}
        f_score: Dict[Node, float] = {
            start: AStarStrategy.heuristic(start, end)
        }

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in AStarStrategy.get_neighbors(grid, current):
                tentative_g_score = g_score[
                    current
                ] + AStarStrategy.calculate_distance(current, neighbor)

                if (
                    neighbor not in g_score
                    or tentative_g_score < g_score[neighbor]
                ):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = (
                        tentative_g_score
                        + AStarStrategy.heuristic(neighbor, end)
                    )
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []
