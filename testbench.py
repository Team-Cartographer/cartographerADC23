from PIL import Image
import random
from utils import load_json, timeit
import os
import numpy as np
import cv2
import FileManager as fm
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np
# import FileManager as fm
#
# parsed_arr = np.array(fm.load_json(fm.data_path + "/AStarRawData.json"))
# # x[0], y[1], z[2], slope[3], azi[4], elev[5], lat[6], long[7], height[8]
#
# # Create the array of height values
# # heights = np.array([[[x, y, x**2 + y**2] for x in range(20)] for y in range(20)])
#
# # Extract the height values
# heights = parsed_arr[:, :, 8]
# #print(np.max(z))
# # Create the x and y coordinate arrays
# x, y = np.meshgrid(range(heights.shape[0]), range(heights.shape[1]))
#
# # Show height map in 3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(x, y, heights)
# plt.title('z as 3d height map')
# plt.show()
#
# # Show height map in 2D
# plt.figure()
# plt.title('z as 2d heat map')
# p = plt.imshow(heights)
# plt.colorbar(p)
# plt.show()


if __name__ == '__main__':
    pass
