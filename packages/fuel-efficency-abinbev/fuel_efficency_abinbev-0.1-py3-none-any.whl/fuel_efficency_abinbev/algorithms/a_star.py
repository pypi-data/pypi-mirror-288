import heapq
import math
from typing import List, Dict

from fuel_efficency_abinbev.algorithms.path_finding import PathfindingStrategy
from fuel_efficency_abinbev.entities.node import Node
from fuel_efficency_abinbev.entities.position import Position


class AStarStrategy(PathfindingStrategy):

    @staticmethod
    def dijkstra_algorithm(grid: List[List[Node]], source: Node):
        """
        Executes Dijkstra's algorithm to find the shortest paths from a given source node.
        It initializes the source distance to zero and all others to infinity. Uses a priority
        queue to explore the nearest unvisited node first, updating the path and total cost for
        each node it explores.

        Args:
            grid (List[List[Node]]): The grid representing the graph.
            source (Node): The starting node.

        Returns:
            Dict[Node, List]: Dictionary mapping each node to its minimum cost and path from the source.
        """
        cost_dict: Dict[Node, List] = {node: [math.inf, []] for row in grid for node in row}
        cost_dict[source] = [0, []]
        S = set()
        q = [(0, source)]
        heapq.heapify(q)

        while q:
            _, u = heapq.heappop(q)
            if u not in S:
                S.add(u)
                list_neighbors = __class__.get_neighbors(grid, u)
                for neighbor in list_neighbors:
                    if neighbor in S: continue
                    distance = __class__.calculate_distance(u, neighbor) + cost_dict[u][0]
                    if cost_dict[neighbor][0] > neighbor.weight + distance:
                        cost_dict[neighbor][0] = neighbor.weight + distance
                        path = cost_dict[u][1] + [u]
                        cost_dict[neighbor][1] = path
                        heapq.heappush(q, (cost_dict[neighbor][0], neighbor))
        return cost_dict

    @staticmethod
    def find_path(grid: List[List[Node]], start: Node, end: Node):
        """
        Finds and returns the shortest path from start to end node excluding the start node.
        Utilizes the result from Dijkstra's algorithm.

        Args:
            grid (List[List[Node]]): The grid representing the graph.
            start (Node): The starting node.
            end (Node): The destination node.

        Returns:
            List[Node]: The list of nodes forming the shortest path from start to end, excluding the start node.
        """
        if not (isinstance(start, Node) and isinstance(end, Node)):
            raise NotImplementedError('Nodes must be type Node.')
        all_possible_paths = __class__.dijkstra_algorithm(grid, start)
        path = all_possible_paths.get(end, [])[1]
        if path:  # Ensure path exists before modifying
            path.append(end)
        return path[1:]  # Exclude the source node

    @staticmethod
    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        """
        Finds and returns the neighboring nodes of a given node, considering cardinal directions.

        Args:
            grid (List[List[Node]]): The grid representing the graph.
            node (Node): The node to find neighbors for.

        Returns:
            List[Node]: A list of nodes adjacent to the given node.
        """
        if not isinstance(node, Node):
            raise NotImplementedError('Nodes must be type Node.')
        grid_width = len(grid[0])
        grid_height = len(grid)
        neighbors = []
        directions = [Position(-1, 0), Position(0, -1), Position(0, 1), Position(1, 0)]

        for direction in directions:
            nx, ny = node.position.x + direction.x, node.position.y + direction.y
            if 0 <= nx < grid_height and 0 <= ny < grid_width:
                neighbors.append(grid[nx][ny])

        return neighbors

    @staticmethod
    def calculate_distance(node1: Node, node2: Node) -> float:
        """
        Calculates and returns the Euclidean distance between two nodes.

        Args:
            node1 (Node): First node.
            node2 (Node): Second node.

        Returns:
            float: The Euclidean distance between the two nodes.
        """
        if not isinstance(node1, Node) or not isinstance(node2, Node):
            raise NotImplementedError('Nodes must be type Node.')
        return math.sqrt((node1.position.x - node2.position.x) ** 2 + (node1.position.y - node2.position.y) ** 2)
