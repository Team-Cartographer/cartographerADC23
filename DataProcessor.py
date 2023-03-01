# This program takes the files from the csv and repackages them as an array of objects

import csv
import FolderCreator as fc
from numpy import cos, sin


pathfile_path = fc.appfiles_path + '\Paths to Data.txt'
with open(pathfile_path, mode="r") as f:

    paths = list(csv.reader(f, delimiter='\n'))
    for i in range(len(paths)):
        paths[i] = paths[i][0]

    f.close()



DISTANCE_BETWEEN_POINTS = str(paths[4]).rstrip("\n")
latitude_path = str(paths[0]).replace("\\", "/").rstrip("\n")
longitude_path = str(paths[1]).replace("\\", "/").rstrip("\n")
height_path = str(paths[2]).replace("\\", "/").rstrip("\n")
slope_path = str(paths[3]).replace("\\", "/").rstrip("\n")

# Creates Lists of each Data Type from the Paths Given.
with open(latitude_path) as csv_file:
    latitude_list = list(csv.reader(csv_file, delimiter=','))
    csv_file.close()
with open(longitude_path) as csv_file:
    longitude_list = list(csv.reader(csv_file, delimiter=','))
    csv_file.close()
with open(height_path) as csv_file:
    height_list = list(csv.reader(csv_file, delimiter=','))
    csv_file.close()
with open(slope_path) as csv_file:
    slope_list = list(csv.reader(csv_file, delimiter=','))
    csv_file.close()


# Call from each file instead of class specific calls.
def generate_data_array():
    if not len(longitude_list) == len(latitude_list) == len(height_list) == len(slope_list):
        print("Number of rows are inconsistent")
        return

    if not len(longitude_list[0]) == len(latitude_list[0]) == len(height_list[0]) == len(slope_list[0]):
        print("Number of columns are inconsistent")
        return

    rows = len(longitude_list)
    cols = len(longitude_list[0])
    xy_dim = len(longitude_list)

    for row in range(rows):
        for data_pt in range(cols):
            # dataArray[k][0] = Lat, dA[k][1] = long, dA[k][2] = ht, dA[k][3] = slope
            dataArray.append(
                # TODO: Double Check the Correctness of this Statement.
                [latitude_list[row][data_pt], longitude_list[row][data_pt], height_list[row][data_pt],
                 slope_list[row][data_pt]]
            )

    return xy_dim


# Helper Functions for Math
def get_x_coord(lat, long, rad):  # takes in degrees latitude and longitude
    return float(rad) * cos(float(lat)) * cos(float(long))


def get_y_coord(lat, long, rad):
    return float(rad) * cos(float(lat)) * sin(float(long))


def get_z_coord(lat, long, rad):  # long is technically not used here. I kept it for consistency. -JL
    return float(rad) * sin(float(lat))


def write_rect_file(data_arr):
    rect_coord_path = fc.data_path + "/RectangularCoordinateData.csv"  # Processed Data Folder given from FolderCreator.py

    with open(rect_coord_path, mode="w", newline="") as datafile:
        csv_writer = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(data_arr)):
            lunar_rad = (1737.4 * 1000)  # converts provided lunar rad data to meters
            lat = data_arr[i][0]
            long = data_arr[i][1]
            height = data_arr[i][2]
            slope = data_arr[i][3]
            radius = lunar_rad + float(height)

            x = get_x_coord(lat, long, radius)
            y = get_y_coord(lat, long, radius)
            z = get_z_coord(lat, long, radius)

            csv_writer.writerow([x, y, z, slope])
        datafile.close()

    return rect_coord_path

# TODO: finish astar data function
def write_astar_data(data_arr):
    astar_data_path = fc.data_path + "/AstarData.csv"  # Processed Data Folder given from FolderCreator.py

    with open(astar_data_path, mode="w", newline="") as astar_data_file:

        astar_data_file.close()

    return astar_data_path


# Deprecated
def write_misc_file(min_height):
    misc_path = fc.data_path + "/MiscData.csv"

    with open(misc_path, mode="w", newline="") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([x_and_y_dim])  # Line 1
        csv_writer.writerow([DISTANCE_BETWEEN_POINTS])  # Line 2
        csv_writer.writerow([min_height])  # Line 3

    f.close()
    return misc_path


# Helper Methods for Finding Maximums and Minimums of Each Attribute of <DataArray>
def find_max_value(data_arr, attr):
    return max(data_arr[attr])
def find_min_value(data_arr, attr):
    return min(data_arr[attr])



# Latitude is DataArr[0], Longitude is DataArr[1], Height is DataArr[2], Slope is DataArr[3]
def find_min_height(data_arr):
    return find_min_value(data_arr, 2)
def find_min_lon(data_arr):
    return find_min_value(data_arr, 1)
def find_min_lat(data_arr):
    return find_min_value(data_arr, 0)
def find_min_slope(data_arr):
    return find_min_value(data_arr, 3)

#TODO: new file that puts minimum of lat/long/height/slope and then scale it
def write_zeroed_file():
    adjusted_path = fc.data_path + "/AdjustedCoordinateData.csv"
    min_lat = abs(float(find_min_lat(dataArray)))
    min_lon = abs(float(find_min_lon(dataArray)))
    min_slope = abs(float(find_min_slope(dataArray)))
    min_height = abs(float(find_min_height(dataArray)))
    with open(adjusted_path, mode="w", newline="") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(dataArray)):
            lunar_rad = (1737.4 * 1000)  # converts provided lunar rad data to meters
            lat = float(dataArray[i][0]) + min_lat
            long = float(dataArray[i][1]) + min_lon
            height = float(dataArray[i][2]) + min_height
            slope = float(dataArray[i][3]) + min_slope
            radius = lunar_rad + float(height)

            x = get_x_coord(lat, long, radius)
            y = get_y_coord(lat, long, radius)
            z = get_z_coord(lat, long, radius)

            csv_writer.writerow([x, y, z, slope])
        f.close()



if __name__ == "__main__":
    dataArray = []
    x_and_y_dim = generate_data_array()

    # absolute_min_height = find_min_height(dataArray)
    # absolute_max_height = find_max_height(dataArray)
    # abs_zero_height_scale = (abs(absolute_max_height) + abs(absolute_min_height))

    rect_file_path = write_rect_file(dataArray)
    adj_file_path = write_zeroed_file()
    # misc_path = write_misc_file(absolute_min_height)
    print("Data Processing Success")
