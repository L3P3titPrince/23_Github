import pandas as pd
import numpy as np
import re

class EdaData(object):
    """
    Try to use this class to answer first task
    """
    def __init__(self):
        pass

    def eda_data(self):
        """

        :return:
        """
        # read data
        self.df = pd.read_csv("03_data/res_purchase_2014.csv", low_memory=False)

        return self.df

    def convert_float(self, x):
        """
        Input is each individual element
        :param x:
        :return:
        """
        if x[0] == '(' and x[-1] == ')':
            x_new = re.findall("\d*\.?\d+", x)
            return -float(x_new[0])
        else:
            # we can ignore there type, just treate them as str and extract them
            x_new = re.findall("\d*\.?\d+", x)
            # transform to float
            return float(x_new[0])

    def clean_data(self):
        """
        When we observe, we see ($29.99) to represent negative
        And there are some number have word, like zero, in this column
        :return:
        """
        # we need clean this column data to float
        # apply() input is each element
        self.df['Cleaned_Amount'] = self.df['Amount'].apply(self.convert_float)
        return self.df


        # *************NOT EFFICIENT WAY****************************
        # there are various data type and differnt context in ['amount'] column
        # we need clean data before analysis
        # for idx, i in tqdm(enumerate(amount_series)):
        #     # first data are float type
        #     if isinstance(i, float):
        #         #         print(i)
        #         pass
        #     # we filter data from minority
        #     elif i[0] == '(' and i[-1] == ')':
        #         #         print(i)
        #         # this is specify for data($29,99)
        #         i_new = i.replace('(', '')
        #         i_new = i_new.replace(')', '')
        #         # replace $ with - and transform to float
        #         i_new = float(i_new.replace('$', '-'))
        #         #         print(i_new, type(i_new))
        #         # replace dataframe with new clean data
        #         self.df.iloc[idx, 6] = i_new
        #     elif type(i) == str:
        #         # use regex to extract float format numerical data
        #         #         print(idx, type(i), i)
        #         i_new = re.findall('\d*\.?\d+', i)
        #         self.df.iloc[idx, 6] = float(i_new[0])
        #     elif type(i) == int:
        #         #         pass
        #         # transform int to float
        #         self.df.iloc[idx, 6] = float(i)
        #     #         print(i)
        #     # if former filter cannot process some data then print these unprocessed data
        #     else:
        #         print(idx, type(i))

        # save to clean csv
        # self.df.to_csv("03_data/cleaned_purchase_2014.csv")
        #
        # return self.df




