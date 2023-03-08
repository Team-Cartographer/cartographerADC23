"""
This program takes data from four csv files, latitude values, longitude values, height values, slope values. The
program then repackages this data as an array of objects and writes it to a csv file named "RawDataArray.csv". The
program then calculates the rectangular coordinates for each data point using formulas for converting latitude,
longitude, and height to Cartesian coordinates. It then writes this data to a csv file named
"RectangularCoordinateData.csv". Finally, the program sorts and formats the rectangular coordinate data in
preparation for use in an A-star algorithm and writes it to a csv file named "AStarRawData.csv".
"""

from ast import literal_eval
import csv
from sys import exit
import FolderCreator as fc
from utils import file2list, get_x_coord, get_y_coord, get_z_coord, calc_azimuth_and_elevation
from dotenv import set_key

DISTANCE_BETWEEN_POINTS = fc.get_dist_between_points()

# Creates Lists of each Data Type from the Paths Given.
latitude_list = file2list(fc.get_latitude_file_path())
longitude_list = file2list(fc.get_longitude_file_path())
height_list = file2list(fc.get_height_file_path())
slope_list = file2list(fc.get_slope_file_path())


def generate_data_array():
    if not len(longitude_list) == len(latitude_list) == len(height_list) == len(slope_list):
        fc.show_error("ADC App Data Processing Failure", f'Data List Row Lengths are Inconsistent.')
        return

    if not len(longitude_list[0]) == len(latitude_list[0]) == len(height_list[0]) == len(slope_list[0]):
        fc.show_error("ADC App Data Processing Failure", f'Data List Column Lengths are Inconsistent.')
        return

    rows = len(longitude_list)
    cols = len(longitude_list[0])
    xy_dim = len(longitude_list)

    # Change to {fc.archive_path} for final build.
    data_array_path_ = fc.data_path + "/RawDataArray.csv"

    with open(data_array_path_, mode="w", newline="") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in range(rows):
            for data_pt in range(cols):
                # dataArray[k][0] = Lat, dA[k][1] = long, dA[k][2] = ht, dA[k][3] = slope
                tmp = [latitude_list[row][data_pt], longitude_list[row][data_pt], height_list[row][data_pt],
                       slope_list[row][data_pt]]
                dataArray.append(tmp)
                csv_writer.writerow(tmp)

    f.close()
    print("Created RawDataArray.csv")

    return xy_dim, data_array_path_

def write_rect_file(data_arr):
    rect_coord_path = fc.data_path + "/RectangularCoordinateData.csv"
    xs, ys, zs, = [], [], []
    length = len(data_arr)
    with open(rect_coord_path, mode="w", newline="") as datafile:
        csv_writer = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(length):
            lat = data_arr[i][0]
            long = data_arr[i][1]
            height = data_arr[i][2]
            slope = float(data_arr[i][3])
            radius = fc.get_lunar_rad() + float(height)

            x = float(get_x_coord(lat, long, radius)) / DISTANCE_BETWEEN_POINTS
            y = float(get_y_coord(lat, long, radius)) / DISTANCE_BETWEEN_POINTS
            z = float(get_z_coord(lat, radius)) / DISTANCE_BETWEEN_POINTS # essentially height
            azi, elev = calc_azimuth_and_elevation(lat, long, height)

            if(elev < -7):
                print(azi, elev)

            csv_writer.writerow([x, y, z, slope, azi, elev, lat, long])
            xs.append(x), ys.append(y), zs.append(z)
            tmpDataArray.append([x, y, z, slope, azi, elev, lat, long])

        datafile.close()
    min_x_, min_y_, min_z_ = abs(min(xs)), abs(min(ys)), abs(min(zs))
    max_z = str(round(abs(min_z_) - abs(max(zs))))
    set_key('.env', 'MAX_Z', max_z)
    set_key('.env', 'MIN_Z', str(min_z_))
    set_key('.env', 'MIN_X', str(min_x_))
    set_key('.env', 'MIN_Y', str(min_y_))

    print("Created RectangularCoordinateData.csv")
    return rect_coord_path, min_x_, min_y_, min_z_


def write_astar_file(min_x_, min_y_, min_z_, temp_array):
    adj_array = []
    for i in range(len(temp_array)):
        # x[0], y[1], z(height)[2], slope[3], azi[4], elev[5], lat[6], long[7]
        tmp = [int(temp_array[i][0] + min_x_), int(temp_array[i][1] + min_y_), int(temp_array[i][2] + min_z_),
               temp_array[i][3], int(temp_array[i][4]), int(temp_array[i][5]), round(float(temp_array[i][6]),2),
               round(float(temp_array[i][7]), 2)]
        adj_array.append(tmp)

    sorted_array = sorted(adj_array, key=lambda x: x[1])

    array_to_be_written = []
    for i in range(1277):
        array_to_be_written.append([])

    for i in range(len(sorted_array)):
        array_to_be_written[i // 1277].append(sorted_array[i])

    for i in range(len(array_to_be_written)):
        array_to_be_written[i] = sorted(array_to_be_written[i], key=lambda x: x[0])

    for i in range(len(array_to_be_written)):
        for j in range(len(array_to_be_written[0])):
            array_to_be_written[j][i][0] = i
            array_to_be_written[j][i][1] = j

    # Retrofitted A-Star Data
    astar_path = fc.data_path + "/AStarRawData.csv"
    with open(astar_path, mode="w", newline="") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in array_to_be_written:
            csv_writer.writerow(row)
    f.close()
    print("Created AStarRawData.csv")

    return astar_path


def test_astar_file():
    astar_path = fc.data_path + "/AStarRawData.csv"
    with open(astar_path, mode="r", newline="") as f:
        astar_data = list(csv.reader(f))

    for j in range(len(astar_data)):
        for i in range(len(astar_data[0])):
            if literal_eval(astar_data[j][i])[0] != i:
                if literal_eval(astar_data[j][i])[1] != j:
                    print(astar_data[j][i])
                    print(i, j)
                    exit(2)


if __name__ == "__main__":
    # Latitude is DataArr[0], Longitude is DataArr[1], Height is DataArr[2], Slope is DataArr[3]
    dataArray = []
    tmpDataArray = []
    x_and_y_dim, data_array_path = generate_data_array()

    rect_file_path, min_x, min_y, min_z, = write_rect_file(dataArray)
    sorted_file_path = write_astar_file(min_x, min_y, min_z, tmpDataArray)
    # test_astar_file()
    print("Data Processing Success")
