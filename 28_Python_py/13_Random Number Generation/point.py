from generator import LCG, SCG
import numpy as np

lcg = LCG()

class point():
    """

    """
    def __init__(self,num = 2000):
        self.num = np.int64(num)

    def coordinate(self):
        """

        :return:
        """
        random_list = lcg.seq_random(self.num)
        axis_list = []
        self.x_list = []
        self.y_list = []
        for i in range(np.int64(self.num/2)):
            self.x_axis = random_list[i] * 2 - 1
            self.y_axis = random_list[i+np.int64(self.num/2)] * 2 - 1
            self.x_list.append(self.x_axis)
            self.y_list.append(self.y_axis)
            axis_list.append((self.x_axis, self.y_axis))

        return axis_list, self.x_list, self.y_list

    def distance(self):
        """

        :return:
        """
        self.axis_distance = 0

#
# test_3 = point()
# test_3_list = test_3.coordinate()
# print(test_3_list[0:5])