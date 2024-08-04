import heapq
import math
from typing import Dict, List, Tuple

from pathfinding_challenge.algorithms.path_finding import PathfindingStrategy
from pathfinding_challenge.entities.node import Node
from pathfinding_challenge.entities.position import Position


class DijkstraStrategy(PathfindingStrategy):
    cardinal_directions = [
        Position(-1, -1),
        Position(-1, 0),
        Position(-1, 1),
        Position(0, -1),
        Position(0, 1),
        Position(1, -1),
        Position(1, 0),
        Position(1, 1),
    ]

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
        for direction in DijkstraStrategy.cardinal_directions:
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
        Dijkstra's algorithm.

        Args:
            grid (List[List[Node]]): The grid containing all nodes.
            start (Node): The starting node.
            end (Node): The destination node.

        Returns:
            List[Node]: The list of nodes representing the shortest path.
                        If no path is found, returns an empty list.
        """
        priority_queue: List[Tuple[float, Node]] = [(0, start)]
        distances: Dict[Node, float] = {start: 0}
        previous_nodes: Dict[Node, Node] = {}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                path = []
                while current_node in previous_nodes:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                path.reverse()
                return path

            for neighbor in DijkstraStrategy.get_neighbors(grid, current_node):
                distance = (
                    current_distance
                    + DijkstraStrategy.calculate_distance(
                        current_node, neighbor
                    )
                )
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    priority_queue.append((distance, neighbor))
                    previous_nodes[neighbor] = current_node

        return []
