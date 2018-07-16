class DataPoint:

    def __init__(self, d):
        self.timestamp = d['timestamp']
        self.datatype = d['datatype']
        self.raw_data = []
        self.data = []

        if self.datatype == 'lidar':
            self.data = [d['x'],
                         d['y'],
                         d['z'],
                         d['class']]

        if self.datatype == 'camera':
            self.data = [d['x'],
                         d['y'],
                         d['class']]

        if self.datatype == 'radar':
            self.data = [d['rho'],
                         d['phi'],
                         d['theta'],
                         d['class']]

    def get_timestamp(self):
        return self.timestamp

    def get(self):
        return self.data

    def get_type(self):
        return self.datatype