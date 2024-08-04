from pathfinding_challenge.algorithms.a_star import AStarStrategy
from pathfinding_challenge.algorithms.context import Context
from pathfinding_challenge.algorithms.dijkstra import DijkstraStrategy
from pathfinding_challenge.entities.valley import Valley
from pathfinding_challenge.utils import (
    compute_path_cost,
    create_grid,
    get_random_edge_position,
    print_grid,
)


class PFC:
    @staticmethod
    def run():
        print('\n=========  Pathfinding Challenge Application  =========\n')
        M = 100
        N = 100
        grid = create_grid(M, N)

        print_grid(grid)

        start_position = get_random_edge_position(M, N)
        end_position = get_random_edge_position(M, N)

        while start_position == end_position:
            end_position = get_random_edge_position(M, N)

        start = Valley(position=start_position)
        end = Valley(position=end_position)

        print('\n=========  START  =========\n', start.position)
        print('\n=========  END    =========\n', end.position)

        context = Context()
        context.grid = grid
        context.start = start
        context.end = end

        context.strategy = AStarStrategy()
        path = context.run()
        path_cost1 = compute_path_cost(path)
        print(
            '\n=========  A* Solution  =========\n',
            path,
            '\n',
            'Total cost: ',
            path_cost1,
        )

        context.strategy = DijkstraStrategy()
        path2 = context.run()
        path_cost2 = compute_path_cost(path2)
        print(
            "\n=========  Djikstra's Solution  =========\n",
            path2,
            '\n',
            'Total cost: ',
            path_cost2,
        )
