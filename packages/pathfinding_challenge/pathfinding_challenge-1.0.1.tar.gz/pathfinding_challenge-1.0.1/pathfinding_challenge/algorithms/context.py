from dataclasses import dataclass, field
from typing import List

from pathfinding_challenge.algorithms.dijkstra import DijkstraStrategy
from pathfinding_challenge.algorithms.path_finding import PathfindingStrategy
from pathfinding_challenge.entities.down_hill import DownHill
from pathfinding_challenge.entities.node import Node
from pathfinding_challenge.entities.plateau import Plateau
from pathfinding_challenge.entities.up_hill import UpHill
from pathfinding_challenge.entities.valley import Valley


@dataclass(slots=True)
class Context:
    """
    Context class for managing the pathfinding strategy and grid of nodes.

    Attributes:
        _strategy (PathfindingStrategy): The pathfinding strategy to use.
        _grid (List[List[Node]]): The grid of nodes representing the map.
        _start (Node): The starting node for pathfinding.
        _end (Node): The ending node for pathfinding.

    Methods:
        grid: Property to get or set the grid of nodes.
        start: Property to get or set the starting node.
        end: Property to get or set the ending node.
        strategy: Property to get or set the pathfinding strategy.
        run: Executes the pathfinding strategy on the current grid, start,
        and end nodes.
        _validate_grid: Validates the grid for disallowed node configurations.
        _validate_adjacent_nodes: Checks and raises an error for forbidden
        adjacent node configurations.
    """

    _strategy: PathfindingStrategy = field(default_factory=DijkstraStrategy)
    _grid: List[List[Node]] = field(
        default_factory=lambda: [
            [Valley() for _ in range(3)] for _ in range(3)
        ]
    )
    _start: Node = field(default_factory=Valley)
    _end: Node = field(default_factory=Valley)

    @property
    def grid(self):
        """
        Property to get or set the grid of nodes.

        Returns:
            List[List[Node]]: The current grid of nodes.

        Raises:
            TypeError: If the new grid is not a list or a list of lists.
            ValueError: If the grid contains forbidden adjacent node
            configurations.
        """
        return self._grid

    @grid.setter
    def grid(self, new_grid: List[List[Node]]):
        if not isinstance(new_grid, list):
            raise TypeError('Grid must be a list')
        if not all(isinstance(row, list) for row in new_grid):
            raise TypeError('Grid must be a list of lists')
        self._grid = new_grid

    @property
    def start(self):
        """
        Property to get or set the starting node.

        Returns:
            Node: The current starting node.
        """
        return self._start

    @start.setter
    def start(self, new_start: Node):
        self._start = new_start

    @property
    def end(self):
        """
        Property to get or set the ending node.

        Returns:
            Node: The current ending node.
        """
        return self._end

    @end.setter
    def end(self, new_end: Node):
        self._end = new_end

    @property
    def strategy(self):
        """
        Property to get or set the pathfinding strategy.

        Returns:
            PathfindingStrategy: The current pathfinding strategy.

        Raises:
            TypeError: If the new strategy is not an instance of
            PathfindingStrategy.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, new_strategy: PathfindingStrategy):
        if not isinstance(new_strategy, PathfindingStrategy):
            raise TypeError(
                'Strategy must be an instance of PathfindingStrategy'
            )
        self._strategy = new_strategy

    def run(self):
        """
        Executes the pathfinding strategy on the current grid, start,
        and end nodes.

        Returns:
            List[Node]: The list of nodes representing the path from
            start to end.

        Raises:
            NotImplementedError: If the strategy does not implement the
            find_path method.
        """
        if not hasattr(self._strategy, 'find_path'):
            raise NotImplementedError(
                'Strategy must implement the find_path method'
            )
        return self._strategy.find_path(self.grid, self.start, self.end)

    def _validate_grid(self, grid: List[List[Node]]):
        """
        Validates the grid for disallowed node configurations.

        Args:
            grid (List[List[Node]]): The grid to validate.

        Raises:
            ValueError: If the grid contains forbidden adjacent
            node configurations.
        """
        for i, row in enumerate(grid):
            for j, node in enumerate(row):
                # Check horizontally
                if j < len(row) - 1:
                    right_node = row[j + 1]
                    self._validate_adjacent_nodes(node, right_node)
                # Check vertically
                if i < len(grid) - 1:
                    bottom_node = grid[i + 1][j]
                    self._validate_adjacent_nodes(node, bottom_node)

    @staticmethod
    def _validate_adjacent_nodes(node1: Node, node2: Node):
        """
        Checks and raises an error for forbidden adjacent
        node configurations.

        Args:
            node1 (Node): The first node to check.
            node2 (Node): The second node to check.

        Raises:
            ValueError: If the nodes are in a forbidden configuration.
        """
        if isinstance(node1, UpHill) and isinstance(node2, Valley):
            raise ValueError('UpHill cannot be adjacent to Valley')
        if isinstance(node1, DownHill) and isinstance(node2, Plateau):
            raise ValueError('DownHill cannot be adjacent to Plateau')
