import os
from PIL import Image , ImageDraw 

script_path = os.path.dirname(__file__)


# MAP RELATED TILES ===================================================================================
VOID = 1
ROBOT_STATION = 2
STORAGE = 3
ZONE_IN = 4
ERROR_ZONE = 5
NORMAL = 6
ZONE_OUT = 7
ADD_ZONE = 8


ZONE_TYPES = [
    VOID            ,
    ROBOT_STATION   ,
    STORAGE         ,
    ZONE_IN         ,
    ERROR_ZONE      ,
    NORMAL          ,
    ZONE_OUT        ,
]

ZONE_TYPE_NAMES = {
    VOID            : "Void",
    ROBOT_STATION   : "RobotStation",
    STORAGE         : "Storage",
    ZONE_IN         : "DropZoneIn",
    ERROR_ZONE      : "ErrorZone",
    NORMAL          : "Normal",
    ZONE_OUT        : "DropZoneOut",
}

ZONE_TYPE_NAMES_DESC = {
    VOID            : "Void",
    ROBOT_STATION   : "Robot Station",
    STORAGE         : "Storage",
    ZONE_IN         : "Drop Zone (In)",
    ERROR_ZONE      : "Error Zone",
    NORMAL          : "Normal",
    ZONE_OUT        : "Drop Zone (Out)",
}

ZONE_TYPE_FOR_ROBOTS = [
    "RobotStation",
    "Storage",
    "DropZoneIn",
    "ErrorZone",
    "DropZoneOut",
]

ZONE_TYPE_FOR_ROBOTS_DESC = {
    ROBOT_STATION : "for charging the robots",
    STORAGE       : "for putting packages (up to 4)",
    ZONE_IN       : "zone in which courriers can deposit their packages and robots can pick up",
    ERROR_ZONE    : "zone in which robots can deposit packages that are unreadable or not present in the DB",
    ZONE_OUT      : "zone in which robots can deposit outgoing packages and courrier can take to load in their truck/van's"
}

MAP = [
    [ERROR_ZONE, ERROR_ZONE,  ROBOT_STATION, VOID],
    [STORAGE,    STORAGE,     NORMAL,        ZONE_IN],
    [STORAGE,    STORAGE,     NORMAL,        VOID],
    [STORAGE,    STORAGE,     NORMAL,        ZONE_IN],
]

# ROBOT RELATED ===================================================================================

JETANK = 1
JETRACER = 2
JETANK_HIWONDER = 3

ROBOT_TYPES = [
    JETANK,
    JETRACER,
    JETANK_HIWONDER,
]

ROBOT_NAMES = {
    JETANK          : "Jetank", 
    JETRACER        : "Jetracer", 
    JETANK_HIWONDER : "Jetank_Hiwonder", 
}

MAP_ROBOTS = [
    # TODO
]

# COLOR RELATED ===================================================================================
# colors for the SVG
# (fill , stroke , alpha)
ALPHA = 0.65
TILE_COLORS = {
    VOID:           ("#1A1A1A","#959595",0),
    ROBOT_STATION:  ("#1D293B","#5C79A3",ALPHA),
    STORAGE:        ("#392F3F","#9577A3",ALPHA),
    ZONE_IN:        ("#1F2F1E","#446E2C",ALPHA),
    ERROR_ZONE:     ("#512D2B","#D7817E",ALPHA),
    NORMAL:         ("#36210A","#996500",ALPHA),
    ZONE_OUT:       ("#1F2F1E","#446E2C",ALPHA),
    ADD_ZONE:       ("#BABDC0","#202020",ALPHA)
}

# colors for the Image
TILE_TEXTURES = {
    VOID            :  Image.open(os.path.join(script_path, "assets" , "png" , "Void.png")).convert("RGBA"),
    ROBOT_STATION   :  Image.open(os.path.join(script_path, "assets" , "png" , "Robot_Station.png")).convert("RGBA"),
    STORAGE         :  Image.open(os.path.join(script_path, "assets" , "png" , "Storage_Zone.png")).convert("RGBA"),
    ZONE_IN         :  Image.open(os.path.join(script_path, "assets" , "png" , "Zone_In.png")).convert("RGBA"),
    ERROR_ZONE      :  Image.open(os.path.join(script_path, "assets" , "png" , "Error_Zone.png")).convert("RGBA"),
    NORMAL          :  Image.open(os.path.join(script_path, "assets" , "png" , "Normal_Floor.png")).convert("RGBA"),
    ZONE_OUT        :  Image.open(os.path.join(script_path, "assets" , "png" , "Zone_Out.png")).convert("RGBA"),
    ADD_ZONE        :  Image.open(os.path.join(script_path, "assets" , "png" , "Zone_Add.png")).convert("RGBA"),
}

# additional images
path_to_check_true  =  os.path.join(script_path , "assets" , "svg" , "check_true2.svg")
path_to_check_false =  os.path.join(script_path , "assets" , "svg" , "check_false2.svg")
path_to_package     =  os.path.join(script_path , "assets" , "svg" , "package.svg")

# colors for the lines
LINE_COLOR = (98,252,0,255)
LINE_COLOR_CROSS = (186,189,192,255)
# colors for the dots
DOT_1 = (0,0,255,255)
DOT_2 = (255,0,0,255)

# DRAWING RELATED ===================================================================================
TILE_SIZE = 50
BORDER = 2
WIDTH = (len(MAP[0]) + BORDER) * TILE_SIZE
HEIGHT = (len(MAP) + BORDER) * TILE_SIZE
ROWS, COLS = len(MAP), len(MAP[0])