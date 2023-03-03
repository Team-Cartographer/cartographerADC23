import FolderCreator as fc
import numpy as np
from ursina import *
from Helpers import file2list, calc_azimuth_and_elevation
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

ground = Entity(
    model=Terrain(heightmap='processed_heightmap.png'),
    texture='grass',
    collider='box',
    scale=(12770, 1000, 12770)
    )

slopemap = fc.parent_path + '/slopemap.png'
heightkey = fc.parent_path + '/heightkey.png'


t_lat = Text(text='Latitude:', x=-.8, y=.45, scale=1.1)
t_lon = Text(text='Longitude:', x=-.8, y=.40, scale=1.1)
t_ht = Text(text='Height:', x=-.8, y=.35, scale=1.1)
t_slope = Text(text='Slope:', x=-.8, y=.30, scale=1.1)
t_azi = Text(text='Azimuth:', x=-.8, y=.25, scale=1.1)
t_elev = Text(text='Elevation:', x=-.8, y=.20, scale=1.1)

t_info = Text(
    text='P for Path, R for Real, M for Moon, H for Heightmap, L for Slope Map, O for Reset',
    x=-.15, y=-.45, scale=1.1, color=color.black
)

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

player = FirstPersonController(position= (200, 5000, 200), speed=250, mouse_sensitivity=Vec2(25, 25))

# Shortcuts/Toggle Functions
def input(key):
    if key == 'o':
        player.set_position((200, 700, 200))
    if key == 'l':
        ground.texture = 'slopemap.png'
    if key == 'h':
        ground.texture = 'heightkey.png'
    if key == 'm':
        ground.texture = 'moon9'
    if key == 'r':
        ground.texture = 'moon17'
    if key == 'p':
        ground.texture = 'LunarPath'


def update():
    x, y, z = player.position.x, player.position.y, player.position.z

    #azimuth, elevation = calc_azimuth_and_elevation(x, y, z, latitudes, longitudes, heights, slopes)

    #for scale testing
    #print(f'x = {x}, y = {y}, z = {z}')

    # Updating Variables
    t_lat.text = 'Latitude: ' + latitudes[int(x) + 620][int(abs(z-620))]
    t_lon.text = 'Longitude: ' + longitudes[int(x) + 620][int(abs(z-620))]
    t_ht.text = 'Height: ' + heights[int(x) + 620][int(abs(z-620))]
    t_slope.text = 'Slope: ' + slopes[int(x) + 620][int(abs(z-620))]
    #t_azi.text = 'Azimuth: ' + str(azimuth)
    #if str(elevation) == 'nan':
    #    t_elev.text = 'Elevation: 0'
    #else:
    #    t_elev.text = 'Elevation: ' + str(elevation)


    if player.position.y < -50:
         player.set_position((200, 200, 200))


#EditorCamera()
app.run()
