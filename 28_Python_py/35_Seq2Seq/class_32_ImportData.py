import pandas as pd
from sklearn.model_selection import train_test_split


from class_31_HyperParameter import HyperParameter

class ImportData(HyperParameter):
    """
    Include process moduel

    """
    def __init__(self):
        """

        """
        HyperParameter.__init__(self)

    def import_data(self):
        """

        :return:
        """
        # we use assign root path + file name to read this firl
        en_path = self.PATH + "europarl-v7.es-en.en"
        # this file didn't use potifix, so we need use open() function to read it into list
        # try to use 'utf-8' decode
        with open(en_path, 'r', encoding = 'utf-8') as f:
            # each sentence is seperate by line
            corpus_en_list = f.read().split('\n')

        # read spanish part
        es_path = self.PATH + "europarl-v7.es-en.es"
        with open(es_path, 'r', encoding = 'utf-8') as f:
            # each sentence is seperate by line
            corpus_es_list = f.read().split('\n')

        # build a dictionary first and then concatneate into a dataframe
        data = {'english': corpus_en_list[:-1],
                'spanish': corpus_es_list[:-1]}
        df = pd.DataFrame(data)

        # we have almost 2 million pairs, so I only use 10k as my running sample
        self.df_sample = df.sample(n = self.SAMPLE, random_state = 1024)

        return self.df_sample


    def split_data(self):
        """

        :return:
        """
        X_train, X_test = train_test_split(self.df_sample, test_size = 0.2, random_state = 1024)

        return X_train, X_test
    #
