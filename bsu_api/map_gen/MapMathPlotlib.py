import matplotlib.pyplot as plt
import networkx as nx
from config import *

def map_to_network(map: list[list]):
    # Add all nodes to the graph
    network = nx.DiGraph()

    for y in range(ROWS):
        for x in range(COLS):
            cell_type = map[y][x]
            if cell_type != VOID:
                node_coords = (y,x)
                network.add_node(node_coords,cell_type=cell_type)

                neighbors = [
                    (y - 1, x),  # Up
                    (y + 1, x),  # Down
                    (y, x - 1),  # Left
                    (y, x + 1)   # Right
                ]
                for dy,dx  in neighbors:
                    if 0 <= dx < COLS and 0 <= dy < ROWS and map[dy][dx] != VOID:
                        neighbor_coords = (dy,dx)
                        network.add_edge(node_coords,neighbor_coords)
    return network


# --------------- MAIN PROGRAM --------------- #
if __name__ == "__main__":
    # Build Graph
    network = map_to_network(MAP)

    print("Number of nodes:", network.number_of_nodes())
    print("Number of edges:", network.number_of_edges())

    
    pos = {
        (r, c): (c, -r) for r, c in network.nodes()
    }

    node_clr=[
        TILE_COLORS[data_cell_type][1] for node , data_cell_type in network.nodes(data="cell_type")
    ]
    
    nx.draw(
        network, 
        pos, 
        with_labels=True, 
        node_color=node_clr, 
        cmap=plt.cm.get_cmap('viridis')
    )
    plt.title("Map as a Network")
    plt.show()