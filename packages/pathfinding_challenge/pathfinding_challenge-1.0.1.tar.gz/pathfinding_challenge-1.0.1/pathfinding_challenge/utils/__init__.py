import math
import random
from typing import List

from pathfinding_challenge.entities.down_hill import DownHill
from pathfinding_challenge.entities.plateau import Plateau
from pathfinding_challenge.entities.position import Position
from pathfinding_challenge.entities.up_hill import UpHill
from pathfinding_challenge.entities.valley import Valley


def generate_terrain(prev_terrain=None):
    """Generate a random terrain type based on continuity rules."""
    terrain_types = [Valley, UpHill, DownHill, Plateau]

    if prev_terrain == UpHill:
        # If the previous terrain is UpHill,
        # the next terrain cannot be Valley
        terrain_types.remove(Valley)
    elif prev_terrain == DownHill:
        # If the previous terrain is DownHill,
        # the next terrain cannot be Plateau
        terrain_types.remove(Plateau)

    return random.choice(terrain_types)


def get_random_edge_position(N: int, M: int) -> Position:
    """Select a random position from the edge of the grid."""
    edge_positions = (
        [(x, 0) for x in range(N)]
        + [(x, M - 1) for x in range(N)]
        + [(0, y) for y in range(1, M - 1)]
        + [(N - 1, y) for y in range(1, M - 1)]
    )
    x, y = random.choice(edge_positions)
    return Position(x, y)


def create_grid(N: int, M: int) -> List[List[object]]:
    """
    Create an NxM grid with random terrain types, adhering to continuity
    rules.

    Args:
        N (int): Number of rows in the grid.
        M (int): Number of columns in the grid.

    Returns:
        List[List[object]]: An NxM grid populated with terrain objects.
    """
    grid = []
    prev_terrain = None

    for x in range(N):
        row = []
        for y in range(M):
            terrain_type = generate_terrain(prev_terrain)
            prev_terrain = terrain_type
            row.append(terrain_type(position=Position(x, y)))
        grid.append(row)

    return grid


def print_grid(grid: List[List[object]]):
    """Print the grid with visual representation."""
    symbols = {Valley: 'V', UpHill: 'U', DownHill: 'D', Plateau: 'P'}

    for row in grid:
        print(' '.join(symbols[type(cell)] for cell in row))


def compute_path_cost(path):
    for i, node in enumerate(path[:-1]):
        node1 = node
        node2 = path[i + 1]
        path_cost = (
            math.sqrt(
                (node2.position.x - node1.position.x) ** 2
                + (node2.position.y - node1.position.y) ** 2
            )
            + node2.weight
        )
    if path_cost:
        return path_cost
    else:
        return 0
