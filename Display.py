import FileManager as fm
from ursina import *
from utils import get_azi_elev, \
    latitude_from_rect, longitude_from_rect, \
    height_from_rect, slope_from_rect, show_error
from ursina.prefabs.first_person_controller import FirstPersonController
from random import choice 
from ursina.application import quit  # USE THIS, NOT PYTHON quit()

# Window Declarations and Formatting -------------
app = Ursina()
window.set_title('Team Cartographer\'s ADC Application')
window.cog_button.disable()
window.exit_button.color = color.dark_gray

# Display Specific Constants -------------
Y_HEIGHT = 128  # Default Value
SIZE_CONSTANT = fm.get_size_constant()
EDITOR_SCALE_FACTOR = 3
PLAYER_SCALE_FACTOR = 10
RESET_LOC = (0, 400, 0)  # Default PLAYER Positional Value
VOLUME = 0.15

# Load the Data
try:
    AStarData = fm.load_json("Data/AStarRawData.json")
except FileNotFoundError:
    show_error("Display Error", "Data Not Processed!")
    quit()


try:
    infodata = fm.load_json("info.json")
except FileNotFoundError:
    show_error("Display Error", "Data Not Processed!")
    quit()


# This File is meant for any Ursina Helper Methods/Classes

# Declaration of Entities -------------

# FirstPersonController Ground Plane
ground_player = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    #color = color.gray,
    texture='moon_surface_texture.png',
    collider='mesh',
    scale=(SIZE_CONSTANT*PLAYER_SCALE_FACTOR, Y_HEIGHT*PLAYER_SCALE_FACTOR, SIZE_CONSTANT*PLAYER_SCALE_FACTOR),
    enabled=False
    )


# EditorCamera Ground Plane
ground_perspective = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    #color=color.gray,
    texture='moon_surface_texture.png',
    collider='box',
    scale=(SIZE_CONSTANT*3, Y_HEIGHT*EDITOR_SCALE_FACTOR, SIZE_CONSTANT*3),
    enabled=False
    )

# ViewCamera Player Location Beacon
view_cam_player_loc = Entity(
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
#    texture='earth_texture.jpg',
#    enabled=True
#    )


# Slope and Height Toggle Image Pathing -------------
slopemap = fm.parent_path + '/slopemap.png'
heightkey = fm.parent_path + '/heightkey_surface.png'


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

vc = EditorCamera(enabled=False, zoom_speed=2) # Note: THIS MUST BE INITIALIZED BEFORE <player> OR ZOOMS WON'T WORK.

player = FirstPersonController(position=RESET_LOC, speed=500, mouse_sensitivity=Vec2(25, 25), enabled=False, gravity=False)
player.cursor.scale = 0.00000000001 # Hides the Cursor from the App Display

track_list = ['Audio/track_1.mp3', 'Audio/track_2.mp3', 'Audio/track_3.mp3', 'Audio/bouyer_sonata_csharp_minor.mp3']
menu_track_list = ['Audio/bouyer_lonely_wasteland.mp3', 'pause_track.mp3']
run_music = Audio(
    # TODO Make a Tracklist Randomizer
    choice(track_list), # Change this for different tracks.
    # TODO Make a Track Picker and Volume Control
    volume=VOLUME,
    loop=True,
)
run_music.stop(destroy=False)

pause_music = Audio(
    menu_track_list[1],
    volume=VOLUME,
    loop=True
)
pause_music.stop(destroy=False)

start_menu_music = Audio(
    menu_track_list[0],
    volume=VOLUME,
    loop=True
)

def play_run_music():
    #run_music.clip(choice(track_list))
    run_music.play()


# Input Functions and Toggles -------------
def input(key):

    # Reset Player
    if key == 'r':
        player.set_position(RESET_LOC)

    # Slopemap Toggle
    if key == 'l':
        ground_player.texture = 'slopemap.png'
        ground_perspective.texture = 'slopemap.png'
        view_cam_player_loc.color = color.green
        color_key.enable()
        color_key.texture='slopeKey.png'

    # Heightkey Toggle
    if key == 'h':
        ground_player.texture = 'heightkey_surface.png'
        ground_perspective.texture = 'heightkey_surface.png'
        view_cam_player_loc.color = color.white
        color_key.enable()
        color_key.texture='heightKey.png'

    if key == 'p':
        ground_player.texture = 'AStar_Path.png'
        ground_perspective.texture = 'AStar_Path.png'
        color_key.disable()

    # Moon Texture Toggle (Default)
    if key == 'm':
        ground_player.texture = 'moon_surface_texture.png'
        ground_perspective.texture = 'moon_surface_texture.png'
        view_cam_player_loc.color = color.red
        color_key.disable()

    # Toggle between Player and EditorCamera
    if key == 'x' and start_button.enabled is False:
        player.enabled = not player.enabled
        vc.enabled = not vc.enabled
        ground_player.enabled = not ground_player.enabled
        ground_perspective.enabled = not ground_perspective.enabled
        view_cam_player_loc.enabled = not view_cam_player_loc.enabled

    # Quit App
    if held_keys['left shift', 'q']:
        exit(0)

    # Pause
    if key == 'escape' and pause_button.enabled is False and volume_slider.enabled is False and start_button.enabled is False:
        t_lat.disable()
        t_lon.disable()
        t_ht.disable()
        t_azi.disable()
        t_slope.disable()
        t_info.disable()
        t_elev.disable()
        player.disable()
        vc.disable()
        ground_player.disable()
        ground_perspective.disable()
        view_cam_player_loc.disable()
        minimap.disable()
        mini_dot.disable()
        t_pos.disable()
        pause_button.enable()
        t_pause.enable()
        t_quit.enable()
        color_key.disable()
        return_button.enable()
        pause_music.play()
        run_music.stop(destroy=False)


# Game Loop Update() Functions -------------
height_vals = ground_player.model.height_values
def update():
    # Audio Update
    VOLUME = volume_change()
    pause_music.volume = VOLUME
    start_menu_music.volume = VOLUME
    run_music.volume = VOLUME


    # Map Failsafe
    bound = SIZE_CONSTANT*10/2 - 200
    if -bound > player.position.x or player.position.x > bound or -bound > player.position.z or player.position.z > bound:
        player.set_position(RESET_LOC)

    # Positions
    x, y, z = player.position.x, player.position.y, player.position.z
    player.y = terraincast(player.world_position, ground_player, height_vals) + 50 # Sets correct height

    # Corrected X and Z values for Calculations
    # Note that in Ursina, 'x' and 'z' are the Horizontal (Plane) Axes, and 'y' is vertical.
    nx, nz = int(x / 10 + int(SIZE_CONSTANT/2)), abs(int(z / 10 - int(SIZE_CONSTANT)/2))

    # Updating Position and Viewer Cam Position Labels
    t_pos.text = f'Position: ({int(x)}, {int(y)}, {int(z)})'
    view_cam_player_loc.position = (x / (10 / EDITOR_SCALE_FACTOR), 0, z / (10 / EDITOR_SCALE_FACTOR))

    # Calculating Data
    lat = float(latitude_from_rect(nx, nz, AStarData))
    long = float(longitude_from_rect(nx, nz, AStarData))
    slope = slope_from_rect(nx, nz, AStarData)
    height = height_from_rect(nx, nz, AStarData, infodata)
    azimuth, elevation = get_azi_elev(nx, nz, AStarData)

    # Updating Variables
    t_lat.text = f'Latitude: {round(lat, 4)}° N'
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
    mmsc: int = SIZE_CONSTANT * 10  # minimap size constant
    mx, mz = (x/mmsc) + 0.5, (z/mmsc) - 0.5
    mini_dot.position = (mx, mz, 0)

    # Earth Positioning
    #earth.position = (earth.x, 400*(elevation), earth.z)

    # Raycasting Tests
    #hit_z = raycast(origin=player, direction=(0, 0, 1), distance=100000, traverse_target=ground_player, ignore=list(), debug=True)
    #hit_x = raycast(origin=player, direction=(-1, 0, 0), distance=100000, traverse_target=ground_player, ignore=list(), debug=True)
    #if hit_z.hit:
    #    print(f'Z: {hit_z}')
    #if hit_x.hit:
    #    print(f'X: {hit_x}')




# Create Start Menu -------------
def start_game():
    ground_player.enable()
    player.enable()
    start_button.disable()
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
    load_button.disable()
    launch_button.disable()
    t_current_site.disable()
    volume_slider.disable()
    sens_slider.disable()
    play_run_music()
    pause_music.stop(destroy=False)


# Unpause Button Function -------------
def on_unpause():
    if str(ground_player.texture) == 'heightkey_surface.png' or str(ground_player.texture) == 'slopemap.png':
        color_key.enable()

    ground_player.enable()
    player.enable()
    pause_button.disable()
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
    return_button.disable()
    pause_music.stop(destroy=False)
    play_run_music()

def load_button_init():
    import tkinter as tk
    from tkinter.filedialog import askdirectory
    root = tk.Tk()
    root.withdraw()
    save_folder = askdirectory()
    # This currently does nothing, just leave it here for saves later on.
    #quit() # USE URSINA QUIT, NOT PYTHON QUIT.
    #fm.load_save(save_folder) # Proof of Concept Shtuff
    #print(save_folder) # This is Reachable.


# Start Menu Text and Buttons -------------
t_start_menu = Text(text="Welcome to Team Cartographer's 2023 NASA ADC Application", x=-0.35, y=0.08)
t_start_menu_creds = Text(text="https://github.com/abhi-arya1/NASA-ADC-App \n \n      https://github.com/pokepetter/ursina", x=-0.275, y=-0.135, color=color.dark_gray)

start_button = Button(text='Main Menu', color=color.gray, highlight_color=color.dark_gray, scale=(0.2, 0.05), y=-0.01)
def main_menu_returner():
    t_start_menu.disable(), t_start_menu_creds.disable(), start_button.disable()
    creds_button.disable()
    start_menu_music.stop(destroy=False)
    t_current_site.enable()
    launch_button.enable()
    load_button.enable()
    pause_button.disable()
    t_quit.disable()
    t_pause.disable()
    return_button.disable()
    pause_music.play()
    volume_slider.enable()
    sens_slider.enable()


start_button.on_click = main_menu_returner

creds_button = Button(text='Credits', color=color.gray, highlight_color=color.dark_gray, scale=(0.2, 0.05), y=-0.07)
def creds_init():
    # TODO: ADD PROPER CREDITS
    pass

# For Main Menu
def volume_change():
    return volume_slider.value

def sens_change():
    sens = sens_slider.value * 65 # Sensitivity Scaler
    player.mouse_sensitivity = Vec2(sens, sens)

t_current_site = Text(text=f"Currently Visiting: Shackleton", x=-0.2, y=0.1, scale=1.25, enabled=False)
launch_button = Button(text="Visualize Site",  color=color.gray, highlight_color=color.dark_gray, scale=(0.25, 0.06), x=0, y=0.0, enabled=False)
load_button = Button(text="Load A Site", color=color.dark_gray, highlight_color=Color(0.15, 0.15, 0.15, 1.0), scale=(0.25, 0.06), x=0, y=-0.08, enabled=False)
volume_slider = ThinSlider(text='Volume', value=0.15, dynamic=True, on_value_changed=volume_change, enabled=False, x=-0.23, y=-0.2)
sens_slider = ThinSlider(text='Sensitivity', value=0.5, dynamic=True, on_value_changed=sens_change, enabled=False, x=-0.23, y=-0.27)

launch_button.on_click = start_game
load_button.on_click = load_button_init


# Pause Menu Text and Buttons -------------
t_pause = Text(text="You are Currently Paused...", x=-0.16, y=0.08, enabled=False)
pause_button = Button(text='Click to Unpause', color=color.gray, highlight_color=color.dark_gray, scale=(0.23, 0.05), enabled=False)
t_quit = Text(text="Press 'LShift+Q' to quit.", x=-0.14, y=-0.135, enabled=False)
pause_button.on_click = on_unpause

return_button = Button(text='Main Menu', color=color.gray, highlight_color=color.dark_gray, scale=(0.23, 0.06), enabled=False, x=0, y=-0.07)
return_button.on_click = main_menu_returner

# Runs Display.py -------------
if __name__ == '__main__':
    app.run(info=False)
