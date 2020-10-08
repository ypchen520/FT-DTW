import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .knndtw import KnnDtw


class ActivityRecognizer:
    def __init__(self, train_data_dir=None, test_data_dir=None, act_record_csv=None):
        self.train_raw_files = sorted(os.listdir(train_data_dir))
        self.train_data = []
        self.train_label = []
        self.test_raw_files = sorted(os.listdir(test_data_dir))
        self.test_data = []
        self.test_label = []
        self.act_record = pd.read_csv(act_record_csv) # read activity record

        data_list = []
        for file in self.train_raw_files:
            raw_data = pd.read_json(os.path.join(train_data_dir, file))
            data_list.append(raw_data)
        train_data_raw = pd.concat(data_list)
        self.extract_activity(train_data_raw)


    def select_period(self, start, end, input):
        start = pd.to_datetime(start, format="%d/%m/%Y %H:%M:%S%z")
        end = pd.to_datetime(end, format="%d/%m/%Y %H:%M:%S%z")
        # print(type(input))
        return input[(input['timestamp'] > start) & (input['timestamp'] <= end)].copy()

    def extract_activity(self, train_data_raw):
        """
        This function generates the following two outputs:
        1. a list of activities
        2. a list of corresponding labels
        Each activity is recorded using a dictionary with keys accelX, accelY, and accelZ.
        The activity index will match the label index.

        For example,
        Assume there are ACTIVITY 1, ACTIVITY 2, and ACTIVITY 3, which correspond to
        the 4th, the 7th, and the 9th activities in the document, the data and label will look like:

          train_data = [{ACTIVITY 1}, {ACTIVITY 2}, {ACTIVITY 3}, ...]
          train_label = [4, 7, 9, ...]

        """
        data_list = []
        for i in range(self.act_record.shape[0]):
            data_dict = {}

            # extract activity by cropping raw data
            # based on the activity time record
            # return type: pandas.core.series.Series
            start_time = self.act_record.iloc[i, 0]
            end_time = self.act_record.iloc[i, 1]
            print(f"activity {self.act_record.iloc[i, 2]}: start: {start_time}, end: {end_time}")
            act = self.select_period(start_time, end_time, train_data_raw)

            # extract accelerometer X, Y, and Z
            # use to_numpy() to convert the type from pandas.core.series.Series to numpy.ndarray
            data_dict.setdefault('accelX', []).extend(act['accelX'].to_numpy())
            data_dict.setdefault('accelY', []).extend(act['accelY'].to_numpy())
            data_dict.setdefault('accelZ', []).extend(act['accelZ'].to_numpy())
            self.train_data.append(data_dict)

            # extract label
            self.train_label.append(self.act_record.iloc[i, 2])
        # print(self.train_label)
        # print(self.train_data[0]['accelX'])

    def visualize(self, act_index):
        """
        act_index: the 1-based index of the activity that will be visualized, this should not be the activity number
        """
        x = self.train_data[act_index-1]['accelX']
        y = self.train_data[act_index-1]['accelY']
        z = self.train_data[act_index-1]['accelZ']
        index = [i for i in range(len(x))]
        plt.plot(index, x, 'r-', label='X')
        plt.plot(index, y, 'b-', label='Y')
        plt.plot(index, z, 'g-', label='Z')

        plt.title('Accelerometer data for Activity #%d' % self.train_label[act_index - 1])
        plt.xlabel('index')
        plt.ylabel('Accelerometer Value')
        plt.legend()
        plt.show()
# class ManagementUtility:
#     def __init__(self):
#         self.gestureFolder = os.path.join(os.getcwd(), GESTURE_FOLDER_NAME)
#         self.train_labels = []
#         self.test_labels = []
#         self.train_data_raw = []
#         self.test_data_raw = []
#         # self.timeOfTemplate = datetime.datetime.today().strftime("%d-%B-%Y-%H-%M-%S") + "-" + str(
#         #     datetime.datetime.today().microsecond)

