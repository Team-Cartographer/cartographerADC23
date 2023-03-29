from numpy import sin, cos, degrees, radians, arctan2, column_stack, min, array_split, arange, loadtxt, sqrt, arcsin
from constants import LUNAR_RADIUS, EARTH_X, EARTH_Y, EARTH_Z, EARTH_LAT, EARTH_LONG
from utils import push_to_json, timeit
from file_manager import FileManager
from concurrent.futures import ProcessPoolExecutor

@timeit
def process_data():
    latitude_list, longitude_list, height_list, height_list, slope_list = load_files()

    latitude_radians = radians(latitude_list)
    longitude_radians = radians(longitude_list)

    radius = LUNAR_RADIUS + height_list

    x, y, z = calculate_cartesian_coordinates(radius, latitude_radians, longitude_radians)
    elevation = calculate_elevation(x, y, z, latitude_radians, longitude_radians)
    azimuth = calculate_azimuth(latitude_radians, longitude_radians)

    processed_data = column_stack((x.flatten(), y.flatten(), z.flatten(), slope_list.flatten(), azimuth.flatten(),
                                   elevation.flatten(), latitude_list.flatten(), longitude_list.flatten(),
                                   height_list.flatten()))

    processed_data[:, 0] += abs(min(processed_data[:, 0]))
    processed_data[:, 1] += abs(min(processed_data[:, 1]))
    processed_data[:, 2] += abs(min(processed_data[:, 2]))

    processed_data = processed_data[processed_data[:, 1].argsort()]

    formatted_data = format_array(processed_data)
    formatted_data = ndarray2list(formatted_data)

    push_to_json(fm.astar_json_path, formatted_data)


def load_file(file_path, delimiter=',', dtype=float):
    return loadtxt(file_path, delimiter=delimiter, dtype=dtype, encoding='utf-8')


def load_files():
    with ProcessPoolExecutor() as executor:
        latitude_future = executor.submit(load_file, fm.latitude_path)
        longitude_future = executor.submit(load_file, fm.longitude_path)
        height_future = executor.submit(load_file, fm.height_path)
        slope_future = executor.submit(load_file, fm.slope_path)

        latitude_list = latitude_future.result()
        longitude_list = longitude_future.result()
        height_list = height_future.result()
        slope_list = slope_future.result()

    return latitude_list, longitude_list, height_list, height_list, slope_list


@timeit
def calculate_cartesian_coordinates(radius, latitude_radians, longitude_radians):
    x = radius * cos(latitude_radians) * cos(longitude_radians)
    y = radius * cos(latitude_radians) * sin(longitude_radians)
    z = radius * sin(latitude_radians)

    return x, y, z


@timeit
def calculate_elevation(x, y, z, latitude, longitude):
    dx, dy, dz = EARTH_X - x, EARTH_Y - y, EARTH_Z - z
    r = sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    rz = dx * cos(latitude) * cos(longitude) + dy * cos(latitude) * sin(longitude) + dz * sin(latitude)

    return degrees(arcsin(rz / r))


@timeit
def calculate_azimuth(latitude, longitude):
    c1 = sin(EARTH_LONG - longitude) * cos(EARTH_LAT)
    c2 = (cos(latitude) * sin(EARTH_LAT)) - (sin(latitude) * cos(EARTH_LAT) * cos(EARTH_LONG - longitude))

    return degrees(arctan2(c1, c2))


@timeit
def format_array(array):
    num_arrays = len(array) // fm.size + (1 if len(array) % fm.size > 0 else 0)
    formatted_array = array_split(array, num_arrays)

    for i in range(len(formatted_array)):
        formatted_array[i] = formatted_array[i][formatted_array[i][:, 0].argsort()]

    row_indices = arange(len(formatted_array)).reshape(-1, 1)
    col_indices = arange(len(formatted_array[0])).reshape(1, -1)

    for i, subarray in enumerate(formatted_array):
        formatted_array[i][:, 0] = row_indices[i].flatten()
        formatted_array[i][:, 1] = col_indices.flatten()

    return formatted_array


@timeit
def ndarray2list(array):
    return [arr.tolist() for arr in array]


if __name__ == "__main__":
    fm = FileManager()
    process_data()