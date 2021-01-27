import numpy as np
import datetime

# question 1 Define class
class Rectangular(object):
    """

    """
    def __init__(self, length ,width):
        """

        """
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * ( self.length + self.width )

length_arr = np.arange(1,11)
width_arr = np.arange(1,11)
myRec = Rectangular(length_arr, width_arr)
print(myRec.area())
print(myRec.perimeter())



# question 2 Display time
class addTime(object):
    """

    """
    def __init__(self, hour, minute, second):
        """
        Initial them
        :param hour:
        :param minute:
        :param second:
        """
        self.hours = hour
        self.minutes = minute
        self.seconds = second
        print(f"Your initial time is {self.hours}h:{self.minutes}m:{self.seconds}s")



    def add(self, hour_2, min_2, sec_2):
        """
        I have tried several time type, including np.datetime64, datatime.
        ONLY (datetime.datetime + datetime.timedelta) can do sum operation
        time_1 is inherred from __init___
        time_2 is the "datetime" formation of time_1
        time_3 is the new input "timedelta"
        sum_time is the sum of time_2 and time_3
        :return:
        """
        # transform hours value to "timedelta" format
        hour_1 = datetime.timedelta(hours = int(self.hours))
        min_1 = datetime.timedelta(minutes=int(self.minutes))
        sec_1 = datetime.timedelta(seconds=int(self.seconds))
        time_1 = hour_1 + min_1 + sec_1
        # we can't use timedelta format to caculate directly, we need transform it "datetime" format
        # basicaly, two add items must be "datetime" and "timedelta"
        time_2 = datetime.datetime.strptime('000000', '%H%M%S') + time_1
        # For now, we have got a datetime format initial  "time_2"
        # initial our second input time
        hour_3 = datetime.timedelta(hours=int(hour_2))
        min_3 = datetime.timedelta(minutes=int(min_2))
        sec_3 = datetime.timedelta(seconds=int(sec_2))
        time_3 = hour_3 + min_3 + sec_3
        print(f"Our second input time is {hour_2}h:{self.minutes}m:{self.seconds}s")
        self.sum_time = time_2 + time_3
        print(self.sum_time.strftime("%H:%M:%S"))
        return self.sum_time

    def displayTime(self):
        print(f"Your initial time is {self.hours}h:{self.minutes}m:{self.seconds}s")

    def displaySecond(self):
        hour_4 = datetime.timedelta(hours = self.sum_time.hour)
        min_4 = datetime.timedelta(minutes=self.sum_time.hour)
        sec_4 = datetime.timedelta(seconds=self.sum_time.hour)
        time_4 = hour_4 + min_4 + sec_4
        print(f"The totoal seconds of two time sum is {time_4.total_seconds()}")

        return None

c = addTime(1,2,3)
sum_time = c.add(1,2,3)
c.displayTime()
c.displaySecond()



# add_time = addTime()
# sum_1 = add_time.add()