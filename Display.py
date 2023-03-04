import FolderCreator as fc
import numpy as np
from ursina import *
from Helpers import file2list, calc_azimuth_and_elevation
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.title = 'ADCLander'
Y_HEIGHT = 90  # Default Value
RESET_LOC = (0, 1000, 0)  # Default PLAYER Value
SIZE_CONSTANT = fc.get_size_constant()



ground_player = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    texture='moon_surface_texture.png',
    collider='box',
    scale=(SIZE_CONSTANT*10, 1000, SIZE_CONSTANT*10),
    enabled=False
    )

ground_perspective = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    texture='moon_surface_texture.png',
    collider='box',
    scale=(SIZE_CONSTANT*3, 360, SIZE_CONSTANT*3),
    enabled=False
    )

editor_cam_player_loc = Entity(
    model='cube',
    scale=(15, 15, 15),
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
Sky()

ec = EditorCamera(enabled=False, zoom_speed=4, orthographic_fov=5000)

player = FirstPersonController(position=RESET_LOC, speed=250, mouse_sensitivity=Vec2(25, 25), enabled=False)
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

def update():
    x, y, z = player.position.x, player.position.y, player.position.z
    if held_keys['left shift']:
        player.speed = 500
    else:
        player.speed = 250

    #TODO: FIX AZI AND ELEV AND LAT/LONG/HT/SLOPE CALCULATIONS
    #azimuth, elevation = calc_azimuth_and_elevation(x, y, z, latitudes, longitudes, heights, slopes)

    #for scale testing
    print(f'\rx = {x}, y = {y}, z = {z}')
    editor_cam_player_loc.position = (x/3.33, 350, z/3.33)



    # Updating Variables
    t_lat.text = 'Latitude: '
    t_lon.text = 'Longitude: '
    t_ht.text = 'Height: '
    t_slope.text = 'Slope: '
    #t_azi.text = 'Azimuth: ' + str(azimuth)
    #if str(elevation) == 'nan':
    #    t_elev.text = 'Elevation: 0'
    #else:
    #    t_elev.text = 'Elevation: ' + str(elevation)

    if player.position.y < -50:
         player.set_position(RESET_LOC)


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

t_start_menu = Text(text="Welcome to Team Cartographer's 2023 NASA ADC Application", x=-0.35, y=0.08)
start_bot = Button(text='Click to Begin', color=color.gray, highlight_color=color.dark_gray, scale=(0.2, 0.05))
start_bot.on_click = start_game


app.run()
