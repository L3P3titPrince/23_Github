import pandas as pd

from class_31_eda import EdaData
from class_32_energy import Energy

def main():
    """
    Beacause running cleaning process will wast a lot of time, so i directly read file from cleaned data
    that i processed before
    This function draw the whole procee of each step
    :param object:
    :return:
    """
    #*************Part One*******************
    eda_class = EdaData()
    credit_df = eda_class.eda_data()
    cleaned_credit_df = eda_class.clean_data()
    # cleaned_credit_df = pd.read_csv('03_data/cleaned_purchase_2014.csv')

    #**********Part Two****************
    energy_class = Energy()
    balance_sheet_df, rating_df = energy_class.import_data()
    # drop nan column, replace NaN value with mean
    cleaned_balance_df = energy_class.clean_data(balance_sheet_df)
    cleaned_rating_df = energy_class.clean_data(rating_df)

    # normalize, becase rating_df only have data and company no is numerical, so we only process balacne_sheet
    # we don't process these not calcuation nuermical column, like date, year, month, company number
    # initial a exclude_list to deduct these columns from normalization queue
    exclude_list = ['Global Company Key', 'Data Date', 'Fiscal Year', 'Fiscal Quarter', 'Fiscal Year-end Month']
    norm_df = energy_class.normalize(cleaned_balance_df, exclude_list)

    energy_class.display_desribe(cleaned_balance_df)

    cleaned_balance_df = energy_class.postfix_extract(cleaned_balance_df)

    Matched = energy_class.merge_df(cleaned_balance_df, cleaned_rating_df)

    energy_class.rating_part(Matched)

    return (cleaned_credit_df, balance_sheet_df, rating_df, cleaned_balance_df, cleaned_rating_df,
            norm_df, Matched)

if __name__=="__main__":
    """
    """
    (cleaned_credit_df, balance_sheet_df, rating_df, cleaned_balance_df, cleaned_rating_df,
     norm_df, Matched)  = main()