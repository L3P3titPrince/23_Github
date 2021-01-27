import pandas as pd
import numpy as np
import time

class Energy(object):
    """
    """

    def __init__(self):
        pass

    def import_data(self):
        """
        ONLY for read data
        """
        self.balance_sheet_df = pd.read_excel('03_data/Energy.xlsx')
        self.rating_df = pd.read_excel('03_data/EnergyRating.xlsx')
        print("*"*30,"5.1 Read ’Energy.xlsx’ and ’EnergyRating.xlsx’","*"*30)
        print(f"Energy.xlsx is a {self.balance_sheet_df.shape} BalanceSheet")
        print(f"EnergyRating.xlsx is a {self.rating_df.shape} Ratings")
        print("*" * 40, "END", "*" * 40, '\n'*3)
        return self.balance_sheet_df, self.rating_df

    def clean_data(self, df):
        """
        we need import t
        Arugs:
        ----
        df:DataFrame
            should be balance_sheet_df and rating_df
        Return:
        ------
        df:DataFrame
            cleaned DataFrame after drop and fillna with mean
        """
        # if we find 90% percential is zero or nan, then we think more than 90% value
        # in this column is 0 or missing value
        quantile_9_series = df.quantile(q=0.9, axis=0)
        # initial drop column list
        drop_list = []
        # these two list is not used yet
        suspicion_list = []
        remain_list = []
        # if we find its 90% quantile is still zero or np.nan, then we drop this how column
        for index, value in quantile_9_series.items():
            # if this column have 90% zero or np.nan value, we add this column name into drop list
            if value == 0 or value == np.nan:
                # print(index, value)
                drop_list.append(index)
            # except use value to judge, we also can use df.isna() and df.isnull() to help
            elif df[index].isna().all() or df[index].isnull().all():
                # print("*" * 20, index, value, "*" * 20, end='\n')
                drop_list.append(index)
            # if we find its 90% is less than 10, we add it into suspicious list
            elif value < 10:
                # print("*" * 20, index, value, "*" * 20, end='\n')
                suspicion_list.append(index)
            else:
                remain_list.append(index)
        # then we drop these column
        df = df.drop(columns=drop_list)
        print("*"*30,"5.2 Drop the column if more than 90% value in this colnmn is 0’","*"*30)
        print(f"Total {len(drop_list)} columns has been dropped")
        print("*" * 40, "END", "*" * 40, '\n'*3)

        # print(f"In {df.__name__}")
        # before cleaned, the True/False for nan value
        print("*" * 30, "5.3 Replace all None or NaN with average value of each column’", "*" * 30)
        print(f"Before fill nan, \n"
              f"we have {df.isnull().any().value_counts()[0]} columns don't contain np.nan value,\n"
              f"we have {df.isnull().any().value_counts()[1]} columns contain np.nan value",end='\n')
        # we use current column mean value to fill nan value in DataFrame
        # df.mean(axis=0) will provide column mean for each column
        df = df.fillna(df.mean(axis = 0))
        # after cleaned, the True/False for nan value
        print(f"After fill nan, \n"
              f"we have {df.isnull().any().value_counts()[0]} columns don't have np.nan value",end='\n')
        print("*" * 40, "END", "*" * 40, '\n'*3)

        return df

    def normalize(self, df, exclude_list):
        """
        Two step, first is identify which column is nurmical, second is normalize these columns
        because we only process balance_sheet_df, so this function is only fit this DataFrame
        Argus:
        -----

        Returns:
        -------
            normalized DataFrame with MinMax() method
        """
        print("*" * 30, "5.4 Normalize the table", "*" * 30)
        start_time = time.time()
        # initial columns value dtype pands.Series
        col_dtype_series = df.dtypes
        # initial the remain column list
        numerical_list = []
        object_list = []
        # we use items() to begin our iteration process
        for index, value in col_dtype_series.items():
            # typically we only have three dtype: int64, float64 and object
            if value == 'int64' or value == 'float64':
                # restore these columns names (value) in numerical_list
                numerical_list.append(index)
            else:
                # maybe create a dictionary to restore index(column name) and value(dtype) is better
                object_list.append(index)

        # next step we need only reserve the column should be normialization
        # Date, year, month and company number should not be include
        # for column names, should be in numerical_list but not in exculde_list
        normalize_list = [item for item in numerical_list if item not in exclude_list]

        # use apply() + function() to complete normalization
        # apply need act on a DataFrame, not a pandas.Series, which means df[normalize_list] actually return
        # a DataFrame to norm_df, not a single column/line
        # all processing in lambda target function (min_max()) input is always a singal whole column
        norm_df = df[normalize_list].apply(lambda x: self.min_max(x), axis= 0)
        # three way for apply function, the result is same
        # alone column direct to process min_max() function
        # norm_df = df.apply(self.min_max, axis = 0)
        # norm_df = df.apply(lambda x:(x - np.min(x)) / (np.max(x) - np.min(x)))
        print(f"There are {len(normalize_list)} columns are numerical by MinMax method.")
        cost_time = round((time.time() - start_time), 4)
        print("*" * 30, "End normalize() with {} second".format(cost_time), "*" * 30, '\n'*3)

        return norm_df

    def min_max(self, series):
        """
        We can directly use this function on DataFrame

        :param series: input should be a column from dataframe and then we use MinMax() scalar for nomalization
        :return: a normalized column
        """
        return (series - series.min()) / (series.max() - series.min())

    def statistic_info(self, x):
        """
        Argus:
        ------
        x:pandas.Series
            manipulate as whole column
        """

        ser = pd.Series(
            [x.count(), x.mean(), x.std(), x.min(), x.quantile(0.25), x.quantile(0.5), x.quantile(0.75), x.max()],
            index=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])

        return ser

    def display_desribe(self, cleaned_balance_df):
        """

        :return:
        """
        # mimic df.desribe()
        # according to double-check, "Assets Netting & Other Adjustments" this column has been dropped in first step
        # because most of values are zero
        display_list = ["Current Assets - Other - Total",
                        "Current Assets - Total",
                        "Other Long-term Assets"]
        display_df = cleaned_balance_df[display_list]
        # pd.set_option("display.max_rows", None, "display.max_columns", None)
        print("*" * 30, "5.5 Simulate describe() function", "*" * 30)
        print(display_df.apply(self.statistic_info))
        print("*" * 40, "END", "*" * 40, '\n'*3)
        print("*" * 30, "5.6 Calculate the correlation matrix", "*" * 30)
        print(display_df.corr)
        print("*" * 40, "END", "*" * 40, '\n'*3)

    def postfix_extract(self, df):
        """
        Only used for cleaned_balance_df
        :param
        :return: split string with ' ' whitespace, this will return a list and extract last one item
        """
        # x:str will be every element in this column
        print("*" * 30, "5.7 Extract Company Postfix", "*" * 30)
        df['CO'] = df['Company Name'].map(lambda x: x.split(' ')[-1])
        df.groupby(['CO'])['CO'].count().plot(kind='bar')
        print("*" * 40, "END", "*" * 40, '\n' * 3)
        return df


    def merge_df(self, df1, df2):
        """

        :param df1:
        :param df2:
        :return:
        """
        merge_list = ['Data Date', 'Global Company Key']
        print("*" * 30, f"5.8 Merge on {merge_list} with two DataFrame", "*" * 30)
        Matched = pd.merge(df1, df2, on=merge_list, how='inner')
        print(f"New Datase have {Matched.shape} size")
        print("*" * 40, "END", "*" * 40, '\n' * 3)

        return Matched

    def rating_numerical(self, x):
        """
        Transform alpha format to numerical format
        :param x:
        :return:
        """
        if x == 'AAA':
            return 0
        elif x == 'AA+':
            return 1
        elif x == 'AA':
            return 2
        elif x == 'AA-':
            return 3
        elif x == 'A+':
            return 4
        elif x == 'A':
            return 5
        elif x == 'A-':
            return 6
        elif x == 'BBB+':
            return 7
        elif x == 'BBB':
            return 8
        elif x == 'BBB-':
            return 9
        elif x == 'BB+':
            return 10
        elif x == 'BB':
            return 11
        else:
            return 12

    def rating_part(self, Matched):
        """

        :return:
        """
        print("*" * 30, f"5.9 Transform Alpha Format to Numerical Format", "*" * 30)
        Matched['Rate'] = Matched['S&P Domestic Long Term Issuer Credit Rating'].map(self.rating_numerical)
        Matched.groupby(['Rate'])['Rate'].count().plot(kind='bar')
        print("*" * 40, "END", "*" * 40, '\n' * 3)

        print("*" * 30, f"5.10 Distribute Frequence", "*" * 30)
        Matched[Matched['CO'] == 'CO'].groupby(['S&P Domestic Long Term Issuer Credit Rating'])['Rate']\
            .count().plot(kind='bar')
        print("*" * 40, "END", "*" * 40, '\n' * 3)


