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

    # Change to Archive Path for final build.
    dataArrayPath = fc.data_path + "/RawDataArray.csv"

    with open(dataArrayPath, mode="w", newline="") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in range(rows):
            for data_pt in range(cols):
                # dataArray[k][0] = Lat, dA[k][1] = long, dA[k][2] = ht, dA[k][3] = slope
                tmp = [latitude_list[row][data_pt], longitude_list[row][data_pt], height_list[row][data_pt],
                    slope_list[row][data_pt]]
                dataArray.append(tmp)
                csv_writer.writerow(tmp)
    f.close()


    return xy_dim, dataArrayPath


# Helper Functions for Math
def get_x_coord(lat, long, rad):  # takes in degrees latitude and longitude
    return float(rad) * cos(float(lat)) * cos(float(long))
def get_y_coord(lat, long, rad):
    return float(rad) * cos(float(lat)) * sin(float(long))
def get_z_coord(lat, long, rad):  # long is technically not used here. I kept it for consistency. -JL
    return float(rad) * sin(float(lat))

def write_rect_file(data_arr):
    rect_coord_path = fc.data_path + "/RectangularCoordinateData.csv"  # Processed Data Folder given from FolderCreator.py
    xs, ys, zs, = [], [], []
    with open(rect_coord_path, mode="w", newline="") as datafile:
        csv_writer = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(data_arr)):
            lunar_rad = (1737.4 * 1000)  # converts provided lunar rad data to meters
            lat = data_arr[i][0]
            long = data_arr[i][1]
            height = data_arr[i][2]
            slope = float(data_arr[i][3])
            radius = lunar_rad + float(height)

            x = float(get_x_coord(lat, long, radius))
            y = float(get_y_coord(lat, long, radius))
            z = float(get_z_coord(lat, long, radius))

            csv_writer.writerow([x, y, z, slope])
            xs.append(x), ys.append(y), zs.append(z)
            zeroArray.append([x, y, z, slope])

        datafile.close()
    min_x, min_y, min_z = abs(min(xs)), abs(min(ys)), abs(min(zs))
    return rect_coord_path, min_x, min_y, min_z

# TODO: finish astar data function
def write_astar_data(data_arr):
    astar_data_path = fc.data_path + "/AstarData.csv"  # Processed Data Folder given from FolderCreator.py

    with open(astar_data_path, mode="w", newline="") as astar_data_file:

        astar_data_file.close()

    return astar_data_path


# Helper Methods for Finding Maximums and Minimums of Each Attribute of <DataArray>
def find_max_value(data_arr, attr):
    return max(data_arr[attr], axis='columns')
def find_min_value(data_arr, attr):
    return min(data_arr[attr], axis='columns')

def write_zeroed_file(xmin, ymin, zmin, zeroArray):
    adjusted_path = fc.data_path + "/AdjustedCoordinateData.csv"
    with open(adjusted_path, mode="w", newline="") as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(zeroArray)):
            csv_writer.writerow([(zeroArray[i][0] + xmin)/40, (zeroArray[i][1] + ymin)/40,
                                 (zeroArray[i][2] + zmin)/40, zeroArray[i][3]])
        f.close()



if __name__ == "__main__":
    # Latitude is DataArr[0], Longitude is DataArr[1], Height is DataArr[2], Slope is DataArr[3]
    dataArray = []
    zeroArray = []
    x_and_y_dim, data_array_path = generate_data_array()

    rect_file_path, min_x, min_y, min_z, = write_rect_file(dataArray)
    adj_file_path = write_zeroed_file(min_x, min_y, min_z, zeroArray)

    # print("Data Processing Success")
