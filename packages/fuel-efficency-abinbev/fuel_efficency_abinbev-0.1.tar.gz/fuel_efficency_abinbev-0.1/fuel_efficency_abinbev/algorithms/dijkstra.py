import heapq
import math
from typing import List, Dict

from fuel_efficency_abinbev.algorithms.path_finding import PathfindingStrategy
from fuel_efficency_abinbev.entities.node import Node
from fuel_efficency_abinbev.entities.position import Position


class DijkstraStrategy(PathfindingStrategy):
    """
    Implements Dijkstra's algorithm for shortest path finding in graphs where all edge weights are non-negative.

    This class includes methods to calculate shortest paths from a single source node to all other nodes in the graph,
    retrieve specific paths, and get neighboring nodes in the graph based on the current node's position.
    """

    @staticmethod
    def dijkstra_algorithm(grid: List[List[Node]], source: Node):
        """
        Calculates the shortest paths from the source node to all other nodes in the grid using Dijkstra's algorithm.

        Args:
            grid (List[List[Node]]): A 2D list representing the graph.
            source (Node): The starting node for path calculations.

        Returns:
            Dict[Node, List[float, List[Node]]]: A dictionary mapping each node to its shortest path cost and the actual path as a list of nodes.

        The algorithm uses a priority queue to repeatedly select the node with the smallest path cost to explore next.
        """
        cost_dict: Dict[Node, List] = {}
        for list_nodes in grid:
            for node in list_nodes:
                cost_dict[node] = [math.inf, []]

        cost_dict[source] = [0, []]
        visited = set()
        priority_queue = [(0, source)]
        heapq.heapify(priority_queue)

        while priority_queue:
            _, current_node = heapq.heappop(priority_queue)
            if current_node not in visited:
                visited.add(current_node)
                neighbors = __class__.get_neighbors(grid, current_node)
                for neighbor in neighbors:
                    if neighbor in visited:
                        continue
                    new_cost = __class__.calculate_distance(current_node, neighbor) + cost_dict[current_node][0]
                    if cost_dict[neighbor][0] > new_cost:
                        cost_dict[neighbor][0] = new_cost
                        path = cost_dict[current_node][1] + [current_node]
                        cost_dict[neighbor][1] = path
                        heapq.heappush(priority_queue, (new_cost, neighbor))
        return cost_dict

    @staticmethod
    def find_path(grid: List[List[Node]], start: Node, end: Node):
        """
        Retrieves the shortest path from the start node to the end node using previously calculated paths.

        Args:
            grid (List[List[Node]]): A 2D list representing the graph.
            start (Node): The starting node of the path.
            end (Node): The destination node.

        Returns:
            List[Node]: A list of nodes forming the shortest path from start to end, excluding the start node.

        This function assumes that the full Dijkstra's algorithm has been run from the start node to calculate all paths.
        """
        if not (isinstance(start, Node) and isinstance(end, Node)):
            raise NotImplementedError('Nodes must be of type Node.')
        paths = __class__.dijkstra_algorithm(grid, start)
        path = paths.get(end, [])[1]
        if path:
            path.append(end)
        return path[1:]  # Exclude the source node from the result.

    @staticmethod
    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        """
        Finds and returns the neighboring nodes of a given node based on vertical, horizontal, and diagonal adjacency.

        Args:
            grid (List[List[Node]]): The grid representing the graph.
            node (Node): The node to find neighbors for.

        Returns:
            List[Node]: A list of neighboring nodes.

        Neighbors are determined by examining adjacent positions in the grid, considering the node's position.
        """
        if not isinstance(node, Node):
            raise NotImplementedError('Parameter must be of type Node.')
        grid_width = len(grid)
        grid_height = len(grid[0])
        neighbors = []
        directions = [
            Position(-1, -1), Position(-1, 0), Position(-1, 1),
            Position(0, -1), Position(0, 1),
            Position(1, -1), Position(1, 0), Position(1, 1)
        ]

        for direction in directions:
            nx, ny = node.position.x + direction.x, node.position.y + direction.y
            if 0 <= nx < grid_height and 0 <= ny < grid_width:
                neighbors.append(grid[nx][ny])

        return neighbors

    @staticmethod
    def calculate_distance(node1: Node, node2: Node) -> float:
        """
        Computes the Euclidean distance between two nodes based on their Cartesian coordinates.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            float: The Euclidean distance between the two nodes.
        """
        if not isinstance(node1, Node) or not isinstance(node2, Node):
            raise NotImplementedError('Both parameters must be of type Node.')
        return math.sqrt((node1.position.x - node2.position.x) ** 2 + (node1.position.y - node2.position.y) ** 2)
