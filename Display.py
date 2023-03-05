import FolderCreator as fc
from ursina import *
from utils import file2list, calc_azimuth_and_elevation
from ursina.prefabs.first_person_controller import FirstPersonController
from ast import literal_eval
astar_list = file2list(os.getcwd() + '/Data/AStarRawData.csv')
from numpy import rad2deg, deg2rad, arccos, arcsin

app = Ursina()
window.title = 'ADCLander'

# Display Specific Constants
Y_HEIGHT = 128  # Default Value
RESET_LOC = (0, Y_HEIGHT*8, 0)  # Default PLAYER Value
SIZE_CONSTANT = fc.get_size_constant()
EDITOR_SCALE_FACTOR=3
PLAYER_SCALE_FACTOR=8

def latitude_from_rect(x: float, y: float) -> float:
    height = literal_eval(astar_list[y][x])[2]
    lat = rad2deg(arcsin(height/((1737.4 * 1000) + height)))
    return lat

def longitude_from_rect(x: float, y: float) -> float:
    height = literal_eval(astar_list[y][x])[2]
    lat = latitude_from_rect(x, y)
    long = rad2deg(arccos((x + round(int(fc.get_size_constant())/2))/(((1737.4 * 1000) + height)*cos(deg2rad(lat)))))
    return long

# TODO check this equation. I don't think it's right so far
def height_from_rect(x: float, y: float) -> float:
    height = literal_eval(astar_list[y][x])[2]
    height -= fc.get_min_z()

def slope_from_rect(x: float, y: float) -> float:
    return literal_eval(astar_list[y][x])[3]

ground_player = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    texture='moon_surface_texture.png',
    collider='box',
    scale=(SIZE_CONSTANT*10, Y_HEIGHT*PLAYER_SCALE_FACTOR, SIZE_CONSTANT*10),
    enabled=False
    )

ground_perspective = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    texture='moon_surface_texture.png',
    collider='box',
    scale=(SIZE_CONSTANT*3, Y_HEIGHT*EDITOR_SCALE_FACTOR, SIZE_CONSTANT*3),
    enabled=False
    )

editor_cam_player_loc = Entity(
    model='cube',
    scale=(20, 20, 20),
    color=color.red,
    enabled=False
)


slopemap = fc.parent_path + '/slopemap.png'
heightkey = fc.parent_path + '/heightkey.png'


t_lat = Text(text='Latitude:', x=-.8, y=.45, scale=1.1, enabled=False)
t_lon = Text(text='Longitude:', x=-.8, y=.40, scale=1.1, enabled=False)
t_ht = Text(text='Height:', x=-.8, y=.35, scale=1.1, enabled=False)
t_slope = Text(text='Slope:', x=-.8, y=.30, scale=1.1, enabled=False)
t_azi = Text(text='Azimuth:', x=-.8, y=.25, scale=1.1, enabled=False)
t_elev = Text(text='Elevation:', x=-.8, y=.20, scale=1.1, enabled=False)

t_info = Text(
    text='P for Path, R for Real, M for Moon, H for Heightmap, L for Slope Map, O for Reset',
    x=-.15, y=-.45, scale=1.1, color=color.black, enabled=False)


latitudes = file2list(fc.get_latitude_file_path())
longitudes = file2list(fc.get_longitude_file_path())
heights = file2list(fc.get_height_file_path())
slopes = file2list(fc.get_slope_file_path())


# Changes Sky Background to Black (0x000000)
class Sky(Entity):
    def __init__(self, **kwargs):
        from ursina.shaders import unlit_shader
        super().__init__(parent=render, name='sky', model='sky_dome', color='000000', scale=9900, shader=unlit_shader)
        for key, value in kwargs.items():
            setattr(self, key, value)
    def update(self):
        self.world_position = camera.world_position
sky=Sky()

'''
class MiniMap(Entity):

    def __init__(self, world_map2d, seed, world_size):
        self.world_size = world_size
        self.save_minimap(world_map2d, seed)
        self.map = Entity(
            parent=camera.ui,
            model="quad",
            scale=(0.3, 0.3),
            origin=(-0.5, 0.5),
            position=window.top_left,
            texture=self.path,
        )
'''

ec = EditorCamera(enabled=False, zoom_speed=4, orthographic_fov=5000)

player = FirstPersonController(position=RESET_LOC, speed=300, mouse_sensitivity=Vec2(25, 25), enabled=False)
player.cursor.scale = 0.00000000001 # Hides the Cursor from the App Display

# Shortcuts/Toggle Functions
def input(key):
    if key == 'r':
        player.set_position(RESET_LOC)
    if key == 'l':
        ground_player.texture = 'slopemap.png'
        ground_perspective.texture = 'slopemap.png'
    if key == 'h':
        ground_player.texture = 'heightkey.png'
        ground_perspective.texture = 'heightkey.png'
    if key == 'm':
        ground_player.texture = 'moon_surface_texture.png'
        ground_perspective.texture = 'moon_surface_texture.png'
    if key == 'x':
        player.enabled = not player.enabled
        ec.enabled = not ec.enabled
        ground_player.enabled = not ground_player.enabled
        ground_perspective.enabled = not ground_perspective.enabled
        editor_cam_player_loc.enabled = not editor_cam_player_loc.enabled
    if held_keys['left shift', 'q']:
        exit(0)
    if key == 'escape' and pause_bot.enabled == False:
        t_lat.enabled = False
        t_lon.enabled = False
        t_ht.enabled = False
        t_azi.enabled = False
        t_slope.enabled = False
        t_info.enabled = False
        t_elev.enabled = False
        player.enabled = False
        ec.enabled = False
        ground_player.enabled = False
        ground_perspective.enabled = False
        editor_cam_player_loc.enabled = False
        pause_bot.enabled = True
        t_pause.enabled = True
        t_quit.enabled = True


astar_array = file2list(fc.data_path + "/AStarRawData.csv")
def update():

    ''' ALL OF THIS IS TODO
    x, y, z = player.position.x, player.position.y, player.position.z

    # Corrected X and Z values for Calculations
    nx, nz = int(abs(x/10-638)), int(abs(z/10-638))

    # Calculating Data
    height = fc.get_max_z() - literal_eval(astar_array[nx][nz])[2]
    print(height * 8)
    print(height*3)


    #TODO: FIX AZI AND ELEV AND LAT/LONG/HT/SLOPE CALCULATIONS
    #azimuth, elevation = calc_azimuth_and_elevation(x, y, z, latitudes, longitudes, heights, slopes)

    #for scale testing
    print(f'\rx = {x}, y = {y}, z = {z}')
    editor_cam_player_loc.position = (x / 3.33, height*EDITOR_SCALE_FACTOR, z / 3.33)


    # Updating Variables
    t_lat.text = 'Latitude: ' + str(latitude_from_rect(nx, nz))
    t_lon.text = 'Longitude: ' + str(-1*longitude_from_rect(nx, nz))
    t_ht.text = 'Height: ' + str(height)
    t_slope.text = 'Slope: ' + str(slope_from_rect(nx, nz))
    #t_azi.text = 'Azimuth: ' + str(azimuth)
    #if str(elevation) == 'nan':
    #    t_elev.text = 'Elevation: 0'
    #else:
    #    t_elev.text = 'Elevation: ' + str(elevation)
    '''

    # Map Failsafes
    if player.position.y < -50:
         player.set_position(RESET_LOC)

    # Sprint Key
    if held_keys['left shift']:
        player.speed = 700
    else:
        player.speed = 300


# Create Start Menu
def start_game():
    ground_player.enabled = True
    player.enabled = True
    start_bot.enabled = False
    t_lat.enabled = True
    t_lon.enabled = True
    t_ht.enabled = True
    t_azi.enabled = True
    t_slope.enabled = True
    t_info.enabled = True
    t_elev.enabled = True
    t_start_menu.enabled = False

# Pause Button Function
def on_pause():
    ground_player.enabled = True
    player.enabled = True
    pause_bot.enabled = False
    t_pause.enabled = False
    t_lat.enabled = True
    t_lon.enabled = True
    t_ht.enabled = True
    t_azi.enabled = True
    t_slope.enabled = True
    t_info.enabled = True
    t_elev.enabled = True
    t_start_menu.enabled = False
    t_quit.enabled = False




t_start_menu = Text(text="Welcome to Team Cartographer's 2023 NASA ADC Application", x=-0.35, y=0.08)
start_bot = Button(text='Click to Begin', color=color.gray, highlight_color=color.dark_gray, scale=(0.2, 0.05))
start_bot.on_click = start_game

t_pause = Text(text="You are Currently Paused...", x=-0.16, y=0.08, enabled=False)
pause_bot = Button(text='Click to Unpause', color=color.gray, highlight_color=color.dark_gray, scale=(0.23, 0.05), enabled=False)
t_quit = Text(text="Press 'LShift+Q' to quit.", x=-0.14, y=-0.06, enabled=False)
pause_bot.on_click = on_pause


app.run()
