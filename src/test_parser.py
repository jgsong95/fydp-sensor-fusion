import json
from bound_box import BoundBox
from datapoint import DataPoint
from bb_parser import BBParser
import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

with open('..\\test_data\\test_camera_data.json') as f:
    camera_data = json.load(f)

camera_bbs = []
for box in camera_data['boxes']:
    data_points = []
    for data_point in box['data_points']:
        data_points.append(DataPoint(data_point['x'], data_point['y'], data_point['z']))

    camera_bbs.append(BoundBox(box['class'], data_points))

with open('..\\test_data\\test_lidar_data.json') as f:
    lidar_data = json.load(f)
lidar_bbs = []
for box in lidar_data['boxes']:
    data_points = []
    for data_point in box['data_points']:
        data_points.append(DataPoint(data_point['x'], data_point['y'], data_point['z']))

    lidar_bbs.append(BoundBox(box['class'], data_points))

bb_parser = BBParser(camera_bbs, lidar_bbs)
matched_list = bb_parser.find_matches()

for lidar, camera in matched_list:
    lidar_points = np.array([[lidar.data[0].x, lidar.data[0].y, lidar.data[0].z],
                             [lidar.data[1].x, lidar.data[1].y, lidar.data[1].z],
                             [lidar.data[2].x, lidar.data[2].y, lidar.data[2].z],
                             [lidar.data[3].x, lidar.data[3].y, lidar.data[3].z],
                             [lidar.data[4].x, lidar.data[4].y, lidar.data[4].z],
                             [lidar.data[5].x, lidar.data[5].y, lidar.data[5].z],
                             [lidar.data[6].x, lidar.data[6].y, lidar.data[6].z],
                             [lidar.data[7].x, lidar.data[7].y, lidar.data[7].z]])
    camera_points = np.array([[camera.data[0].x, camera.data[0].y, camera.data[0].z],
                              [camera.data[1].x, camera.data[1].y, camera.data[1].z],
                              [camera.data[2].x, camera.data[2].y, camera.data[2].z],
                              [camera.data[3].x, camera.data[3].y, camera.data[3].z],
                              [camera.data[4].x, camera.data[4].y, camera.data[4].z],
                              [camera.data[5].x, camera.data[5].y, camera.data[5].z],
                              [camera.data[6].x, camera.data[6].y, camera.data[6].z],
                              [camera.data[7].x, camera.data[7].y, camera.data[7].z]])

    fig = plot.figure()
    ax = Axes3D(fig)

    lidar_x_vals = [lidar.data[0].x,
                    lidar.data[1].x,
                    lidar.data[2].x,
                    lidar.data[3].x,
                    lidar.data[4].x,
                    lidar.data[5].x,
                    lidar.data[6].x,
                    lidar.data[7].x]
    lidar_y_vals = [lidar.data[0].y,
                    lidar.data[1].y,
                    lidar.data[2].y,
                    lidar.data[3].y,
                    lidar.data[4].y,
                    lidar.data[5].y,
                    lidar.data[6].y,
                    lidar.data[7].y]
    lidar_z_vals = [lidar.data[0].z,
                    lidar.data[1].z,
                    lidar.data[2].z,
                    lidar.data[3].z,
                    lidar.data[4].z,
                    lidar.data[5].z,
                    lidar.data[6].z,
                    lidar.data[7].z]

    camera_x_vals = [camera.data[0].x,
                     camera.data[1].x,
                     camera.data[2].x,
                     camera.data[3].x,
                     camera.data[4].x,
                     camera.data[5].x,
                     camera.data[6].x,
                     camera.data[7].x]
    camera_y_vals = [camera.data[0].y,
                     camera.data[1].y,
                     camera.data[2].y,
                     camera.data[3].y,
                     camera.data[4].y,
                     camera.data[5].y,
                     camera.data[6].y,
                     camera.data[7].y]
    camera_z_vals = [camera.data[0].z,
                     camera.data[1].z,
                     camera.data[2].z,
                     camera.data[3].z,
                     camera.data[4].z,
                     camera.data[5].z,
                     camera.data[6].z,
                     camera.data[7].z]

    ax.scatter(lidar_x_vals, lidar_y_vals, lidar_z_vals, c='r')
    ax.scatter(camera_x_vals, camera_y_vals, camera_z_vals, c='b')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plot.show()
