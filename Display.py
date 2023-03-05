import FolderCreator as fc
from PIL import Image
from ursina import *
from utils import file2list, calc_azimuth_and_elevation, latitude_from_rect, longitude_from_rect, get_radius, height_from_rect, slope_from_rect
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import camera

app = Ursina()
window.title = 'ADCLander'

# Display Specific Constants
Y_HEIGHT = 128  # Default Value
RESET_LOC = (0, Y_HEIGHT*8, 0)  # Default PLAYER Value
SIZE_CONSTANT = fc.get_size_constant()
EDITOR_SCALE_FACTOR = 3
PLAYER_SCALE_FACTOR = 8

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

minimap = Entity(
    parent = camera.ui,
    model="quad",
    scale=(0.3, 0.3),
    origin=(-0.5, 0.5),
    position=window.top_left,
    texture='minimap.png',
    enabled = False
)

mini_dot = Entity(
    parent = minimap,
    model='quad',
    scale = (0.05, 0.05),
    color = color.red
    )

slopemap = fc.parent_path + '/slopemap.png'
heightkey = fc.parent_path + '/heightkey.png'


t_lat = Text(text='Latitude:', x=-.54, y=.48, scale=1.1, enabled=False)
t_lon = Text(text='Longitude:', x=-.54, y=.43, scale=1.1, enabled=False)
t_ht = Text(text='Height:', x=-.54, y=.38, scale=1.1, enabled=False)
t_slope = Text(text='Slope:', x=-.54, y=.33, scale=1.1, enabled=False)
t_azi = Text(text='Azimuth:', x=-.54, y=.28, scale=1.1, enabled=False)
t_elev = Text(text='Elevation:', x=-.54, y=.23, scale=1.1, enabled=False)

t_info = Text(
    text='M for Moon, L for Slopemap, H for Heightmap, Esc for Pause, X for Switch',
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
sky = Sky()


player = FirstPersonController(position=RESET_LOC, speed=300, mouse_sensitivity=Vec2(25, 25), enabled=False)
ec = EditorCamera(enabled=False, zoom_speed=5)

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
    if key == 'x' and start_bot.enabled is False:
        player.enabled = not player.enabled
        ec.enabled = not ec.enabled
        ground_player.enabled = not ground_player.enabled
        ground_perspective.enabled = not ground_perspective.enabled
        editor_cam_player_loc.enabled = not editor_cam_player_loc.enabled
        minimap.enabled = not minimap.enabled
    if held_keys['left shift', 'q']:
        exit(0)
    if key == 'escape' and pause_bot.enabled is False:
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
        minimap.enabled = False

def update():

    x, y, z = player.position.x, player.position.y, player.position.z

    # Corrected X and Z values for Calculations
    nx, nz = int(x/10+638), int(z/10+638)

    # Calculating Data
    rad = get_radius(nx, nz)
    lat = str(latitude_from_rect(nx, nz, rad))
    long = str(-longitude_from_rect(nx, nz, rad))
    slope = str(slope_from_rect(nx, nz))
    height = str(height_from_rect(nx, nz))

    #TODO: FIX AZI AND ELEV AND LAT/LONG/HT/SLOPE CALCULATIONS
    azimuth, elevation = calc_azimuth_and_elevation(float(lat), float(long), float(height))

    #for scale testing
    #print(f'\rx = {x}, y = {y}, z = {z}')
    #editor_cam_player_loc.position = (x / 3.33, height*EDITOR_SCALE_FACTOR, z / 3.33)

    # Updating Variables
    t_lat.text = 'Latitude: ' + lat
    t_lon.text = 'Longitude: ' + long
    t_ht.text = 'Height: ' + str(height)
    t_slope.text = 'Slope: ' + slope
    t_azi.text = 'Azimuth: ' + str(azimuth)

    if str(elevation) == 'nan':
        t_elev.text = 'Elevation: 0'
    else:
        t_elev.text = 'Elevation: ' + str(elevation)


    # Map Failsafes
    if player.position.y < -50:
         player.set_position(RESET_LOC)

    # Sprint Key
    if held_keys['left shift']:
        player.speed = 1500
    else:
        player.speed = 300


    # TODO Fix Minimap Positioning
    mx, mz = abs(int((x/10)/12-60)),(int((z/10)/12-60))



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
    minimap.enabled = True

# Unpause Button Function
def on_unpause():
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
    minimap.enabled = True




t_start_menu = Text(text="Welcome to Team Cartographer's 2023 NASA ADC Application", x=-0.35, y=0.08)
start_bot = Button(text='Click to Begin', color=color.gray, highlight_color=color.dark_gray, scale=(0.2, 0.05))
start_bot.on_click = start_game

t_pause = Text(text="You are Currently Paused...", x=-0.16, y=0.08, enabled=False)
pause_bot = Button(text='Click to Unpause', color=color.gray, highlight_color=color.dark_gray, scale=(0.23, 0.05), enabled=False)
t_quit = Text(text="Press 'LShift+Q' to quit.", x=-0.14, y=-0.06, enabled=False)
pause_bot.on_click = on_unpause


app.run()
