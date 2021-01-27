import numpy as np
import matplotlib.pyplot as plt

class Test(object):
    """
    """

    def __init__(self):
        pass

    def noise_point(self):
        """
        A simulated dataset will be provided as below. The polynomial used is y = 5 * x + 20 * x2 + x3.
        """
        # we have 100 noise point
        noise_scale = 100
        # how many samples we use in this task
        number_of_samples = 50
        # uniform distribution column vector (m*1), between (0-0.8, 1-0.8)*25 = (-20, 5)
        self.x = 25 * (np.random.rand(number_of_samples, 1) - 0.8)
        # y =[-100, 1118]
        self.y = 5 * self.x + 20 * self.x ** 2 + 1 * self.x ** 3 + noise_scale * np.random.randn(number_of_samples, 1)
        plt.style.use('seaborn-whitegrid')
        plt.plot(self.x, self.y, 'ro')
        plt.show()

    @property
    def genetic_algorithm(self):
        """
        formula is y = a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f
        """
        # ground truth of target value
        y_actual = self.y
        # predict target value
        y_pred = None

        # create 100 six_element array of random numbers
        weight_arr = np.random.rand(100, 6)
        # initial repeat time
        REPEAT_TIME = 500

        x_arr = np.array(self.x**5,self.x**4)
        for i in range(0, REPEAT_TIME):
            pass


        return self.x, self.y, weight_arr, x_arr



