from MapPlotter import MapPlotter
import os

script_path = os.path.dirname(__file__)

# Intersections are nodes and the routes between them are the actions
# using Manhattan distance (heurestic) we can determine the best path or using A*
# Internal nodes = Decision points (intersections).
# Leaf nodes = Final destinations.
# Edges = Actions like move forward, turn left, turn right. Are the paths between intersections
#        Start
#          |
#       (Node A)
#       /   |   \
#     Left  Fwd  Right
#       |      \
#    (Node B)  (Node C)
#     /    \
#   Stop  Forward

mp = MapPlotter(
    mode="SVG",
    filename=os.path.join(script_path,"map.svg"),  
)

mp.draw_nodes()
mp.save_map()



