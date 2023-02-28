from csv import reader as r
import numpy as np
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

ground = Entity(
    # model = 'testBlenderProgram'
    model=Terrain(heightmap='htmap6'),
    texture='moon9',
    #collider='box',
    collider='box',
    scale=(1240, 150, 1240)
)

'''
ship = Entity(
    model='C:/Users/ashwa/Downloads/lunar_lander.blend',
    collider='mesh',
    scale=(100, 50, 100)
)
'''


t_lat = Text(text='Latitude:', x=-.8, y=.45, scale=1.1)
t_lon = Text(text='Longitude:', x=-.8, y=.40, scale=1.1)
t_ht = Text(text='Height:', x=-.8, y=.35, scale=1.1)
t_slope = Text(text='Slope:', x=-.8, y=.30, scale=1.1)
t_azi = Text(text='Azimuth:', x=-.8, y=.25, scale=1.1)
t_elev = Text(text='Elevation:', x=-.8, y=.20, scale=1.1)

t_info = Text(
    text='P for Path, R for Real, M for Moon, H for Heightmap, L for Slope Map, O for Reset',
    x=-.15,
    y=-.45,
    scale=1.1,
    color=color.black
)

latitudes, longitudes, heights, slopes = [], [], [], []
with open('C:/Users/ashwa/Downloads/RegLat.csv') as csv_file:
    reads = r(csv_file)
    for row in reads:
        latitudes.append(row)
with open('C:/Users/ashwa/Downloads/RegLong.csv') as csv_file:
    reads = r(csv_file)
    for row in reads:
        longitudes.append(row)
with open('C:/Users/ashwa/Downloads/RegHeight.csv') as csv_file:
    reads = r(csv_file)
    for row in reads:
        heights.append(row)
with open('C:/Users/ashwa/Downloads/RegSlope.csv') as csv_file:
    reads = r(csv_file)
    for row in reads:
        slopes.append(row)


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

player = FirstPersonController(position= (200, 1000, 200), speed=50, mouse_sensitivity=Vec2(25, 25))

# Shortcuts/Toggle Functions
def input(key):
    if key == 'o':
        player.set_position((200, 200, 200))
    if key == 'l':
        ground.texture = 'slopemap_test'
    if key == 'h':
        ground.texture = 'color_heights_test'
    if key == 'm':
        ground.texture = 'moon9'
    if key == 'r':
        ground.texture = 'moon17'
    if key == 'p':
        ground.texture = 'LunarPath'


def update():
    x, y, z = player.position.x, player.position.y, player.position.z

    # Azimuth Angle and Elevation Calculation
    latE, longE = 29.5593, 95.0900 # Latitude and Longitude of Johnson Space Center.
    latM, longM = float(latitudes[int(x) + 620][int(abs(z-620))]), float(longitudes[int(x) + 620][int(abs(z-620))])

    rad_earth = 6378000
    xE = rad_earth * cos(latE) * cos(longE)
    yE = rad_earth * cos(latE) * sin(longE)
    zE = rad_earth * sin(latE)

    xM = latM * cos(float(longM) * math.pi / 180)
    yM = latM * sin(float(longM) * math.pi / 180)
    zM = float(heights[int(x) + 620][int(abs(z-620))])

    resultant_vector = [xE-xM, yE-yM, zE-zM]

    range = sqrt(resultant_vector[0] ** 2 + resultant_vector[1] ** 2 + resultant_vector[2] ** 2)

    rz = resultant_vector[0] * cos(latM) * cos(longM) + resultant_vector[1] * cos(latM) * cos(longM) + resultant_vector[2] * sin(latM)

    c1 = sin(longE - longM) * cos(latE)
    c2 = (cos(latM) * sin(latE)) - (sin(latM) * cos(latE) * cos(longE - longM))

    # Elevation Value
    elev = np.arcsin(rz/range)

    # Azimuth Angle Value
    azimuth = np.arctan2(c1, c2)

    #for scale testing
    #print(f'x = {x}, y = {y}, z = {z}')

    # Updating Variables
    t_lat.text = 'Latitude: ' + latitudes[int(x) + 620][int(abs(z-620))]
    t_lon.text = 'Longitude: ' + longitudes[int(x) + 620][int(abs(z-620))]
    t_ht.text = 'Height: ' + heights[int(x) + 620][int(abs(z-620))]
    t_slope.text = 'Slope: ' + slopes[int(x) + 620][int(abs(z-620))]
    t_azi.text = 'Azimuth: ' + str(azimuth)
    if str(elev) == 'nan':
        t_elev.text = 'Elevation: 0'
    else:
        t_elev.text = 'Elevation: ' + str(elev)


    if player.position.y < -50:
         player.set_position((200, 200, 200))


#EditorCamera()

app.run()

