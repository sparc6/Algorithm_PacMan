class Node:
    """A node class for A* pathfinding."""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Distance from start node
        self.h = 0  # Heuristic based estimated distance to end node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze."""

    # Create start and end nodes
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialize both open and closed lists
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until the end node is found
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0

        # Find the node with the lowest f value
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list and add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Check if we have reached the end, return the path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return the path in reverse (from start to end)

        # Generate children from adjacent squares
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Ensure within range of maze
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[0]) - 1) or node_position[1] < 0:
                continue

            # Ensure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append new node
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

    return None  # Path not found
