from abc import ABC, abstractmethod
from typing import List

from pathfinding_challenge.entities.node import Node


class PathfindingStrategy(ABC):
    """
    Abstract base class for pathfinding strategies.

    This class defines the interface for different pathfinding strategies.
    Each strategy must implement methods to find a path, calculate the distance
    between nodes, and retrieve neighboring nodes in the grid.

    Attributes:
        None
    """

    @abstractmethod
    def find_path(
        self, grid: List[List[Node]], start: Node, end: Node
    ) -> List[Node]:
        """
        Find a path from the start node to the end node.

        Args:
            grid (List[List[Node]]): The grid representing the terrain.
            start (Node): The starting node.
            end (Node): The ending node.

        Returns:
            List[Node]: A list of nodes representing the
            path from start to end.
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_neighbors(self, grid: List[List[Node]], node: Node) -> List[Node]:
        """
        Retrieve the neighboring nodes of a given node.

        Args:
            grid (List[List[Node]]): The grid representing the terrain.
            node (Node): The node for which neighbors are to be found.

        Returns:
            List[Node]: A list of neighboring nodes.
        """
        pass  # pragma: no cover

    @abstractmethod
    def calculate_distance(self, node1: Node, node2: Node) -> float:
        """
        Calculate the cost distance between two nodes,
        considering the Node's terrain.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            float: The distance between node1 and node2.
        """
        pass  # pragma: no cover
