import FolderCreator as fc
from ursina import *
from utils import get_azi_elev, latitude_from_rect, longitude_from_rect, get_radius, height_from_rect, slope_from_rect
from ursina.prefabs.first_person_controller import FirstPersonController

# Window Declarations and Formatting -------------
app = Ursina()
window.fps_counter.disable()
window.set_title('Team Cartographer\'s ADC Application')
window.cog_button.disable()
window.exit_button.color = color.dark_gray

# Display Specific Constants -------------
Y_HEIGHT = 128  # Default Value
SIZE_CONSTANT = fc.get_size_constant()
EDITOR_SCALE_FACTOR = 3
PLAYER_SCALE_FACTOR = 8
RESET_LOC = (0, Y_HEIGHT*PLAYER_SCALE_FACTOR, 0)  # Default PLAYER Positional Value



# Declaration of Entities -------------

# FirstPersonController Ground Plane
ground_player = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    texture='moon_surface_texture.png',
    collider='box',
    scale=(SIZE_CONSTANT*10, Y_HEIGHT*PLAYER_SCALE_FACTOR, SIZE_CONSTANT*10),
    enabled=False
    )

# EditorCamera Ground Plane
ground_perspective = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    texture='moon_surface_texture.png',
    collider='box',
    scale=(SIZE_CONSTANT*3, Y_HEIGHT*EDITOR_SCALE_FACTOR, SIZE_CONSTANT*3),
    enabled=False
    )

# EditorCamera Location Beacon
editor_cam_player_loc = Entity(
    model='cube',
    scale=(20, 1000, 20),
    color=color.red,
    enabled=False,
    )

# Minimap Image
minimap = Entity(
    parent=camera.ui,
    center=(0, 0, 0),
    model="quad",
    scale=(0.3, 0.3),
    origin=(-0.5, 0.5),
    position=window.top_left,
    texture='minimap.png',
    enabled=False
    )

# Minimap Dot Entity
mini_dot = Entity(
    parent=minimap,
    model='circle',
    scale=(0.03, 0.03),
    position=(0, 0, 0),
    color=color.red,
    enabled=False
    )

# Color Key Entity (Activates on Heightmap/Slopemap Toggle)
color_key = Entity(
    parent=camera.ui,
    model='quad',
    scale = (0.3, 0.11),
    position=(-0.74, 0.09, 0),
    texture='slopeKey.png',
    enabled=False
)

# Earth Entity (Scales to Player Position)
#earth = Entity(
#    model='sphere',
#    scale=(1000, 1000, 1000),
#    position=(0, 600, -9000),
#    texture='2k_earth_daymap.jpg',
#    enabled=True
#    )


# Slope and Height Toggle Image Pathing -------------
slopemap = fc.parent_path + '/slopemap.png'
heightkey = fc.parent_path + '/heightkey_surface.png'



# Textboxes  -------------
t_lat = Text(text='Latitude:', x=-.54, y=.48, scale=1.1, enabled=False)
t_lon = Text(text='Longitude:', x=-.54, y=.43, scale=1.1, enabled=False)
t_ht = Text(text='Height:', x=-.54, y=.38, scale=1.1, enabled=False)
t_slope = Text(text='Slope:', x=-.54, y=.33, scale=1.1, enabled=False)
t_azi = Text(text='Azimuth:', x=-.54, y=.28, scale=1.1, enabled=False)
t_elev = Text(text='Elevation:', x=-.54, y=.23, scale=1.1, enabled=False)
t_pos = Text(text='positional data', x=-0.883, y=0.185, z=0, enabled=False)
t_info = Text(
    #text='M for Moon, L for Slopemap, H for Heightmap, Esc for Pause, X for Switch',
    text='',
    x=-.15, y=-.45, scale=1.1, color=color.black, enabled=False)



# Player Interactable Declarations -------------

sky = Sky()
sky.color = '000000' # Black

ec = EditorCamera(enabled=False, zoom_speed=5, rotation_x=32.421871185302734, rotation_y=-26.388877868652344) # Note: THIS MUST BE INITIALIZED BEFORE <player> OR ZOOMS WON'T WORK.

player = FirstPersonController(position=RESET_LOC, speed=500, mouse_sensitivity=Vec2(25, 25), enabled=False)
#player.scale = (0.5, 1, 0.5)
player.cursor.scale = 0.00000000001 # Hides the Cursor from the App Display



# Input Functions and Toggles -------------
def input(key):

    # Reset Player
    if key == 'r':
        player.set_position(RESET_LOC)

    # Slopemap Toggle
    if key == 'l':
        ground_player.texture = 'slopemap.png'
        ground_perspective.texture = 'slopemap.png'
        editor_cam_player_loc.color = color.blue
        color_key.enable()
        color_key.texture='slopeKey.png'

    # Heightkey Toggle
    if key == 'h':
        ground_player.texture = 'heightkey_surface.png'
        ground_perspective.texture = 'heightkey_surface.png'
        editor_cam_player_loc.color = color.white
        color_key.enable()
        color_key.texture='heightKey.png'

    if key == 'p':
        ground_player.texture = 'AStar_Path.png'
        ground_perspective.texture = 'AStar_Path.png'

    # Moon Texture Toggle (Default)
    if key == 'm':
        ground_player.texture = 'moon_surface_texture.png'
        ground_perspective.texture = 'moon_surface_texture.png'
        editor_cam_player_loc.color = color.red
        color_key.disable()

    # Toggle between Player and EditorCamera
    if key == 'x' and start_bot.enabled is False:
        player.enabled = not player.enabled
        ec.enabled = not ec.enabled
        ground_player.enabled = not ground_player.enabled
        ground_perspective.enabled = not ground_perspective.enabled
        editor_cam_player_loc.enabled = not editor_cam_player_loc.enabled

    # Quit App
    if held_keys['left shift', 'q']:
        exit(0)

    # Pause
    if key == 'escape' and pause_bot.enabled is False:
        t_lat.disable()
        t_lon.disable()
        t_ht.disable()
        t_azi.disable()
        t_slope.disable()
        t_info.disable()
        t_elev.disable()
        player.disable()
        ec.disable()
        ground_player.disable()
        ground_perspective.disable()
        editor_cam_player_loc.disable()
        minimap.disable()
        mini_dot.disable()
        t_pos.disable()
        pause_bot.enable()
        t_pause.enable()
        t_quit.enable()
        color_key.disable()



# Game Loop Update() Functions -------------
def update():
    # Map Failsafe
    if -6150 > player.position.x or player.position.x > 6150 or -6150 > player.position.z or player.position.z > 6150:
        player.set_position(RESET_LOC)

    # Positions
    x, y, z = player.position.x, player.position.y, player.position.z

    # Corrected X and Z values for Calculations
    # Note that in Ursina, 'x' and 'z' are the Horizontal (Plane) Axes, and 'y' is vertical.
    nx, nz = int(x / 10 + 638), abs(int(z / 10 - 638))
    #print(f'({nx}, {nz})')

    t_pos.text = f'Position: ({int(x)}, {int(y)}, {int(z)})'
    editor_cam_player_loc.position = (x / (10 / 3), 0, z / (10 / 3))


    # Calculating Data
    rad = get_radius(nx, nz)
    lat = float(latitude_from_rect(nx, nz, rad))
    long = -float(longitude_from_rect(nx, nz, rad))
    slope = slope_from_rect(nx, nz)
    height = height_from_rect(nx, nz)
    azimuth, elevation = get_azi_elev(nx, nz)

    # Updating Variables
    t_lat.text = f'Latitude: {round(lat, 4)}° S'
    t_lon.text = f'Longitude: {round(long, 4)}° E'
    t_ht.text = 'Height: ' + str(height) + 'm'
    t_slope.text = 'Slope: ' + str(slope) + '°'
    t_azi.text = 'Azimuth: ' + str(round(azimuth, 4)) + '°'
    t_elev.text = 'Elevation: ' + str(round(elevation, 4)) + '°'

    # Sprint Key
    if held_keys['left shift']:
        player.speed = 1500
    else:
        player.speed = 500


    # Mini-Map Dot Positioning
    mx, mz = (x/12770) + 0.5, (z/12770)-0.5
    mini_dot.position = (mx, mz, 0)

    # Earth Positioning
    #earth.position = (earth.x, 400*(elevation), earth.z)



# Create Start Menu -------------
def start_game():
    ground_player.enable()
    player.enable()
    start_bot.disable()
    t_lat.enable()
    t_lon.enable()
    t_ht.enable()
    t_azi.enable()
    t_slope.enable()
    t_info.enable()
    t_elev.enable()
    t_start_menu.disable()
    t_start_menu_creds.disable()
    minimap.enable()
    mini_dot.enable()
    t_pos.enable()


# Unpause Button Function -------------
def on_unpause():
    ground_player.enable()
    player.enable()
    pause_bot.disable()
    t_pause.disable()
    t_lat.enable()
    t_lon.enable()
    t_ht.enable()
    t_azi.enable()
    t_slope.enable()
    t_info.enable()
    t_elev.enable()
    t_start_menu.disable()
    t_quit.disable()
    minimap.enable()
    mini_dot.enable()
    t_pos.enable()


# Start Menu Text and Buttons -------------
t_start_menu = Text(text="Welcome to Team Cartographer's 2023 NASA ADC Application", x=-0.35, y=0.08)
t_start_menu_creds = Text(text="https://github.com/abhi-arya1/NASA-ADC-App \n \n      https://github.com/pokepetter/ursina", x=-0.275, y=-0.07, color=color.dark_gray)
start_bot = Button(text='Click to Begin', color=color.gray, highlight_color=color.dark_gray, scale=(0.2, 0.05))
start_bot.on_click = start_game


# Pause Menu Text and Buttons -------------
t_pause = Text(text="You are Currently Paused...", x=-0.16, y=0.08, enabled=False)
pause_bot = Button(text='Click to Unpause', color=color.gray, highlight_color=color.dark_gray, scale=(0.23, 0.05), enabled=False)
t_quit = Text(text="Press 'LShift+Q' to quit.", x=-0.14, y=-0.06, enabled=False)
pause_bot.on_click = on_unpause


# Runs Display.py -------------
app.run(info=False)
