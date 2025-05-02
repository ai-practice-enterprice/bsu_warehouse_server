from PIL import Image , ImageDraw
from prisma.models import Zones  
import svgwrite
import svgwrite.image
import svgwrite.shapes
import networkx as nx
import base64
from .config import *
# from a AI point of view the map can be represented as a tree instead of a 2D or 3D array 
# where the each node is represented as a square and circle (a tile)
# and each edge (action) is represented as line    
class MapPlotter():
    def __init__(
        self,
        map: list[list[int]] | None = None,
        data: list[Zones] | None = None,
        tilesize=TILE_SIZE,
        mode="RGBA",
        filename="map",
        border: bool = True,
    ):
        
        try:
            if map is None and data is None:
                raise Exception("parameter map or data must be given to the MapPlotter") 
        except Exception as e:
            print(f"Exception => {e.args}")

        self.drop_zone_data = {}
        if data is not None:
            self.MAP = self.transform_data_to_map(data)
            self.data_received = True
        elif map is not None:
            self.MAP = map
            self.data_received = False

        self.add_border = border
        if border: self.border = BORDER 
        else: self.border = 0 

        try:
            with open(path_to_check_true, "rb") as f:
                self.encoded_file_check_true = base64.b64encode(f.read()).decode("utf-8")
                f.close()

            with open(path_to_check_false, "rb") as f:
                self.encoded_file_check_false = base64.b64encode(f.read()).decode("utf-8")
                f.close()
        except Exception as e:
            print(f"Could not read files {path_to_check_false} and {path_to_check_true}")

        
        # aesthetic variables
        self.TILE_SIZE = tilesize
        self.TILE_COLORS = TILE_COLORS
        self.TILE_TEXTURES = TILE_TEXTURES
        self.dot_colors = (DOT_1,DOT_2)
        self.clr_lines = LINE_COLOR

        # configuration variables
        self.filename = filename
        self.COLS = len(self.MAP[0])
        self.ROWS = len(self.MAP)
        self.WIDTH = (self.COLS + self.border) * self.TILE_SIZE
        self.HEIGHT = (self.ROWS + self.border) * self.TILE_SIZE      

        try:
            if mode == "RGBA":
                self.mode = mode
                # 1) Creating an RGBA image with transparency
                self.image = Image.new(mode="RGBA",size=(self.WIDTH,self.HEIGHT),color=(0,0,0,0))
                self.draw = ImageDraw.Draw(self.image)
            elif mode == "SVG":
                self.mode = mode
                # 2) Creating an SVG drawing
                # ID's and CLASS names are only added when switching between profiles (tiny || full)
                self.dwg = svgwrite.Drawing(self.filename, size=(self.WIDTH, self.HEIGHT),profile="tiny",class_="warehouse_svg_map")
            else: 
                raise Exception("Unknown mode")
        except Exception as e:
            print(f"Exception => {e.args}")



        # -------- for the SVG -------- #
        # / still nothing
        # -------- for the Image -------- #
        # / also nothing :(
        

    def map_to_network(self):
        # Add all nodes to the graph
        network = nx.Graph()

        for y in range(self.ROWS):
            for x in range(self.COLS):
                cell_type = self.MAP[y][x]
                node_coords = (y,x)
                # the y,x combination (in that order) is unique so it can be used as a key
                # to retrieve each node
                network.add_node(
                    node_coords, 
                    cell_type=cell_type
                )

                neighbors = [
                    (y - 1, x),  # Up
                    (y + 1, x),  # Down
                    (y, x - 1),  # Left
                    (y, x + 1)   # Right
                ]
                for dy,dx  in neighbors:
                    if 0 <= dx < self.COLS and 0 <= dy < self.ROWS and self.MAP[dy][dx] != VOID:
                        neighbor_coords = (dy,dx)
                        network.add_edge(node_coords,neighbor_coords)
        
        print("Number of nodes:", network.number_of_nodes())
        print("Number of edges:", network.number_of_edges())
    
        self.network = network

    def transform_data_to_map(self,data: list[Zones]):
        max_y = -1
        max_x = -1
        for zone in data:
            if max_y < zone.zoneY:
                max_y = zone.zoneY
            if max_x < zone.zoneX:
                max_x = zone.zoneX
            if zone.zoneTypes.zoneTypeID == ZONE_IN or zone.zoneTypes.zoneTypeID == ZONE_OUT:
                self.drop_zone_data[zone.zoneID] = zone.zoneAvailable

        map_from_db = [[None for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        for zone in data:
            if 0 <= zone.zoneY <= max_y and 0 <= zone.zoneX <= max_x:
                map_from_db[zone.zoneY][zone.zoneX] = zone.zoneType
            else:
                print(f"Warning: Zone with coordinates (x={zone.zoneX}, y={zone.zoneY}) is outside the determined bounds.")
        return map_from_db

    def draw_nodes(self,radius=5):
        zoneID = 1
        for y, row in enumerate(self.MAP):
            for x, tile in enumerate(row):
                new_x = x 
                new_y = y
                position_x = x
                position_y = y
                clr = (0,0,0,255)

                if self.add_border:
                    position_x += 1
                    position_y += 1
                    if x == 0:
                        new_x -= 1
                    if y == 0:
                        new_y -= 1
                    if y == (self.HEIGHT - 1):
                        new_y += 1
                    if x == (self.WIDTH - 1):
                        new_x += 1
                    # self.draw_add_contour(new_x,new_y)

                if (x + y) % 2 : 
                    clr = self.dot_colors[0]
                elif (x + y) % 2 == 0:
                    clr = self.dot_colors[1]


                center = (position_x * self.TILE_SIZE + self.TILE_SIZE // 2, position_y * self.TILE_SIZE + self.TILE_SIZE // 2)

                # -------- for the SVG -------- #
                if self.mode == "SVG":
                    zone_type = ZONE_TYPE_NAMES[self.MAP[y][x]]
                    color,line_clr, alpha = self.TILE_COLORS[tile]
                    class_name = "zone"

                    self.dwg.add(
                        svgwrite.shapes.Rect(
                            insert=(position_x * self.TILE_SIZE, position_y * self.TILE_SIZE), 
                            size=(self.TILE_SIZE, self.TILE_SIZE), 
                            fill=color,
                            fill_opacity=alpha,
                            stroke=line_clr,
                            stroke_dasharray="5,5",
                            stroke_width=1,
                            id = str(zoneID),
                            class_ = zone_type + " " + class_name,
                        )
                    )
                    if self.drop_zone_data.get(zoneID,-1) != -1:
                        self.add_marks(position_x * self.TILE_SIZE,position_y * self.TILE_SIZE,self.drop_zone_data[zoneID])

                    zoneID += 1


                    self.dwg.add(
                        svgwrite.shapes.Circle(
                            center=center,
                            r=radius,
                            stroke="rgb" + str((clr[0],clr[1],clr[2])),
                            stroke_width=2,
                            fill="rgb" + str((clr[0],clr[1],clr[2])),
                            fill_opacity=0.3
                        )
                    )
                # -------- for the Image -------- #
                if self.mode == "RGBA":
                    tile_texture = self.TILE_TEXTURES.get(tile,TILE_TEXTURES[0])
                    tile_texture_resized = tile_texture.resize((self.TILE_SIZE, self.TILE_SIZE))
                    self.image.paste(tile_texture_resized, (x * self.TILE_SIZE, y * self.TILE_SIZE), tile_texture_resized)

                    self.draw.ellipse(
                        [(center[0] - radius, center[1] - radius),(center[0] + radius, center[1] + radius)],
                        fill=clr,
                        width=4
                    )

    def draw_add_contour(self,x: int,y: int):
        # -------- for the SVG -------- #
        if self.mode == "SVG":
            color,line_clr, alpha = self.TILE_COLORS[ADD_ZONE]
            class_name = "zone"
            self.dwg.add(
                svgwrite.shapes.Rect(
                    insert=(x * self.TILE_SIZE, y * self.TILE_SIZE), 
                    size=(self.TILE_SIZE, self.TILE_SIZE), 
                    fill=color,
                    fill_opacity=alpha,
                    stroke=line_clr,
                    stroke_dasharray="5,5",
                    stroke_width=1,
                    class_ =  "add_zone " + class_name,
                )
            )
        # -------- for the Image -------- #
        if self.mode == "RGBA":
            tile_texture = self.TILE_TEXTURES.get(ADD_ZONE,TILE_TEXTURES[8])
            tile_texture_resized = tile_texture.resize((self.TILE_SIZE, self.TILE_SIZE))
            self.image.paste(tile_texture_resized, (x * self.TILE_SIZE, y * self.TILE_SIZE), tile_texture_resized)

    def draw_edges(self):
        for y, row in enumerate(self.MAP):
            for x, tile in enumerate(row):
                if tile == VOID:
                    continue
                position_x = x
                position_y = y
                if self.add_border:
                    position_x += 1
                    position_y += 1
                # Draw connections (horizontal & vertical lines)
                clr_stroke = (self.clr_lines[0],self.clr_lines[1],self.clr_lines[2])
                alpha = self.clr_lines[3]
                center_current_node = (position_x * self.TILE_SIZE + self.TILE_SIZE // 2, position_y * self.TILE_SIZE + self.TILE_SIZE // 2)
                center_next_node_down = (position_x * self.TILE_SIZE + self.TILE_SIZE // 2, (position_y + 1) * self.TILE_SIZE + self.TILE_SIZE // 2)
                center_next_node_right= ((position_x + 1) * self.TILE_SIZE + self.TILE_SIZE // 2, position_y * self.TILE_SIZE + self.TILE_SIZE // 2)
                
                # -------- Horizontal Lines -------- #
                if x < self.COLS - 1 and self.MAP[y][x + 1] != VOID:
                    # -------- for the SVG -------- #
                    if self.mode == "SVG":
                        self.dwg.add(
                            svgwrite.shapes.Line(
                                start=center_current_node,
                                end=center_next_node_right,
                                stroke="rgb" + str(clr_stroke),
                                stroke_opacity=0.8,
                                stroke_width=4,
                            )
                        )
                    # -------- for the Image -------- #
                    if self.mode == "RGBA":
                        self.draw.line(
                            [center_current_node, center_next_node_right],
                            fill=self.clr_lines,
                            width=4
                        )
                # -------- Vertical Lines -------- #
                if y < self.ROWS - 1 and self.MAP[y + 1][x] != VOID:
                    # -------- for the SVG -------- #
                    if self.mode == "SVG":
                        self.dwg.add(
                            svgwrite.shapes.Line(
                                start=center_current_node,
                                end=center_next_node_down,
                                stroke="rgb" + str(clr_stroke),
                                stroke_width=4,
                                stroke_opacity=0.8,
                            )
                        )
                    # -------- for the Image -------- #
                    if self.mode == "RGBA":
                        self.draw.line(
                            [center_current_node, center_next_node_down],
                            fill=self.clr_lines,
                            width=4
                        )

    def add_marks(self,position_x,position_y,zoneAvailable):
        if self.data_received:
            if zoneAvailable:
                image_uri = f"data:image/svg+xml;base64,{self.encoded_file_check_true}"
            else:
                image_uri = f"data:image/svg+xml;base64,{self.encoded_file_check_false}"

            self.dwg.add(
                svgwrite.image.Image(
                    href=image_uri,
                    insert=(position_x,position_y),
                    size=(self.TILE_SIZE // 2,self.TILE_SIZE // 2)
                )
            )


    def save_map(self):
        if self.mode == "SVG":
            # -------- for the SVG -------- #
            self.dwg.save()
        if self.mode == "RGBA":
            # -------- for the Image -------- #
            self.image.save(self.filename)

