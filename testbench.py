

# import numpy as np
#
#
# import matplotlib.pyplot as plt
# import math
#
# def find_points_on_line(array, x, y, angle):
#     # Convert angle to radians
#     radians = math.radians(angle)
#
#     # Calculate slope of the line
#     slope = math.tan(radians)
#
#     # Determine orientation of the line (vertical or horizontal)
#     if abs(angle) < 45 or abs(angle) > 135:
#         # Line is more horizontal than vertical
#         horizontal = True
#     else:
#         # Line is more vertical than horizontal
#         horizontal = False
#
#     # Calculate y-intercept of the line
#     y_intercept = y - slope * x
#
#     # Initialize set to store coordinates on the line
#     points = set()
#
#     # Iterate over rows or columns of the array, depending on orientation of the line
#     if horizontal:
#         for i in range(len(array[0])):
#             # Calculate corresponding y-coordinate on the line
#             y_line = slope * i + y_intercept
#
#             # Round y-coordinate to nearest integer
#             y_coord = round(y_line)
#
#             # Check if calculated coordinate is within bounds of the array
#             if y_coord >= 0 and y_coord < len(array):
#                 points.add((y_coord, i))
#     else:
#         for i in range(len(array)):
#             # Calculate corresponding x-coordinate on the line
#             x_line = (i - y_intercept) / slope
#
#             # Round x-coordinate to nearest integer
#             x_coord = round(x_line)
#
#             # Check if calculated coordinate is within bounds of the array
#             if x_coord >= 0 and x_coord < len(array[0]):
#                 points.add((i, x_coord))
#
#     return points
#
# # Define the array
# array = np.array([
#     [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10],
#     [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
#     [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
#     [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
#     [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
#     [51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
#     [61, 62, 63, 64, 65, 66, 67, 68, 69, 70],
#     [71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
#     [81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
#     [91, 92, 93, 94, 95, 96, 97, 98, 99,100]
# ])
#
# # Define the starting point and the angle in degrees
# start_point = (5, 5)
# angle = 178
#
# # Find the points on the line passing through the starting point
# points_on_line = find_points_on_line(array, start_point[0], start_point[1], angle)
#
# # Set up the plot
# fig, ax = plt.subplots(figsize=(10, 10))
#
# # Display the array as an image
# ax.imshow(array, cmap='gray')
#
# # Plot dots for each node in the array, with different colors for the starting point, nodes on the line, and other nodes
# for i in range(array.shape[0]):
#     for j in range(array.shape[1]):
#         color = 'k'  # default color is black
#         if (i, j) == start_point:
#             color = 'y'  # starting point is yellow
#         elif (i, j) in points_on_line:
#             color = 'b'  # points on the line are blue
#         ax.scatter(j, i, color=color)
#
# # Set the axis labels and title
# ax.set_xlabel('Columns')
# ax.set_ylabel('Rows')
# ax.set_title('Array Visualization')
#
# # Show the plot
# plt.show()

import chardet
with open('C:/Users/ashwa/Desktop/Regional Data Files/RegLat.csv', 'rb') as f:
    result = chardet.detect(f.read())
print(result['encoding'])