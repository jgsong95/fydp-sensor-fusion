from bound_box import BoundBox
import numpy as np

class BBParser:

    def __init__(self, lidar_data, camera_data):
        self.lidar_data = lidar_data
        self.camera_data = camera_data
        self.parsed_bboxes = []

    # Data comes from calibration as list of objects
    # data is list of bounding box coordinates (as tuples) and object class as string
    def parse(self):


        self.parsed_bboxes.append(self.weighted_avg_bb(bb))


    def find_matches(self, lidar_bb):
        for camera_bb in self.camera_data:
            if self.match(lidar_bb, camera_bb):


    # Sort both lists of bounding points by distance from origin
    # match points between sensors, create new bounding box with weighted scores
    def match(self, lidar_bb, camera_bb):

        # Check for equal amount of bounding coordinates and same object type (ie. 'car')
        if lidar_bb.object_class == camera_bb.object_class and len(camera_bb) == len(lidar_bb):
            for ax, ay, az in lidar_bb.data:
                for bx, by, bz in camera_bb.data:
                    self.compute_distance(np.array((ax, ay, az)), np.array((bx, by, bz)))


    def compute_distance(self, a, b):
        return np.linalg.norm(a-b)


    def weighted_avg_bb(self, matched_points):

        new_bb = []

        for a, b in matched_points:
            new_bb.append((((a.x - b.x) / 2),
                          ((a.y - b.y) / 2),
                          ((a.z - b.z) / 2)))
        return new_bb
