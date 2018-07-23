from bound_box import BoundBox
import numpy as np
from datapoint import DataPoint


# 2 lists of bounding boxes
# Find matching bounding boxes
# Apply kalman filter
class BBParser:
    # used to determine whether objects are the same between different sensor data
    error_threshold = 20.00

    def __init__(self, lidar_data, camera_data):
        self.lidar_data = lidar_data
        self.camera_data = camera_data
        self.parsed_bboxes = []

    def find_matches(self):

        sorted_lidar_data = sorted(self.lidar_data, key=self.centroid)
        sorted_camera_data = sorted(self.camera_data, key=self.centroid)

        # Search for matching bounding boxes between sensors
        for camera_bb in sorted_camera_data:
            for lidar_bb in sorted_lidar_data:

                match = self.match(camera_bb, lidar_bb)

                if match:
                    camera_bb.matched = True
                    lidar_bb.matched = True
                    self.parsed_bboxes.append((camera_bb, lidar_bb))

        # Add bounding boxes that didnt have matches to list
        for camera_bb in sorted_camera_data:
            if not camera_bb.matched:
                self.parsed_bboxes.append((camera_bb, self.empty_bb()))

        for lidar_bb in sorted_lidar_data:
            if not lidar_bb.matched:
                self.parsed_bboxes.append((lidar_bb, self.empty_bb()))

        return self.parsed_bboxes

    # Sort both lists of bounding points by distance from origin
    # match points between sensors, create new bounding box with weighted scores
    def match(self, camera_bb, lidar_bb):

        # Check for equal amount of bounding coordinates and same object type (ie. 'car')
        if lidar_bb.classifier == camera_bb.classifier:

            sorted_lidar_bb = sorted(lidar_bb.data, key=self.compute_datapoint_to_origin)
            sorted_camera_bb = sorted(camera_bb.data, key=self.compute_datapoint_to_origin)

            for i in range(8):
                error = self.compute_distance(sorted_lidar_bb[i], sorted_camera_bb[i])
                if error >= self.error_threshold:
                    return False
            return True

    def compute_distance(self, a, b):

        a_point = np.array((a.x, a.y, a.z))
        b_point = np.array((b.x, b.y, b.z))

        return np.linalg.norm(a_point - b_point)

    def compute_distance_origin(self, a):
        origin = np.array((0, 0, 0))

        return np.linalg.norm(a - origin)

    def compute_datapoint_to_origin(self, datapoint):
        origin = np.array((0, 0, 0))
        a = np.array((datapoint.x, datapoint.y, datapoint.z))
        return np.linalg.norm(a - origin)

    def centroid(self, bb):

        x = 0
        y = 0
        z = 0

        for datapoint in bb.data:
            x += datapoint.x
            y += datapoint.y
            z += datapoint.z

        centroid = np.array((x / 8, y / 8, z / 8))

        return self.compute_distance_origin(centroid)

    def empty_bb(self):
        return BoundBox('empty', [DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0),
                                  DataPoint(0, 0, 0)])
