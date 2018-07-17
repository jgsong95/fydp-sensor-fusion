from bound_box import BoundBox
import numpy as np

# 2 lists of bounding boxes
# Find matching bounding boxes
# Apply kalman filter
class BBParser:

    # used to determine whether objects are the same between different sensor data
    error_threshold = 10.00

    def __init__(self, lidar_data, camera_data):
        self.lidar_data = lidar_data
        self.camera_data = camera_data
        self.parsed_bboxes = []

    # Data comes from calibration as list of objects
    # data is list of bounding box coordinates (as tuples) and object class as string
    def parse(self):
        self.find_matches()






    def find_matches(self):

        sorted_lidar_data = sorted(self.lidar_data, key=self.centroid)
        sorted_camera_data = sorted(self.camera_data, key=self.centroid)

        for camera_bb in sorted_camera_data:
            for lidar_bb in sorted_lidar_data:
                if self.match(lidar_bb, camera_bb):
                    self.parsed_bboxes.append((lidar_bb, camera_bb))

    # Sort both lists of bounding points by distance from origin
    # match points between sensors, create new bounding box with weighted scores
    def match(self, lidar_bb, camera_bb):

        # Check for equal amount of bounding coordinates and same object type (ie. 'car')
        if lidar_bb.object_class == camera_bb.object_class:

            sorted_lidar_bb = sorted(lidar_bb.data, key=self.compute_distance_origin)
            sorted_camera_bb = sorted(camera_bb.data, key=self.compute_distance_origin)

            for i in range(8):
                error = self.compute_distance(sorted_lidar_bb[i], sorted_camera_bb[i])
                if error >= self.error_threshold:
                    return False
            return True


    def compute_distance(self, a, b):
        return np.linalg.norm(a-b)


    def compute_distance_origin(self, a):
        origin = np.array((0, 0, 0))
        return np.linalg.norm(a-origin)


    def centroid(self, bb):

        x = 0
        y = 0
        z = 0

        for bb_x, bb_y, bb_z, classifier in bb:
            x += bb_x
            y += bb_y
            z += bb_z

        centroid = np.array((x/8, y/8, z/8))

        return self.compute_distance_origin(centroid)
