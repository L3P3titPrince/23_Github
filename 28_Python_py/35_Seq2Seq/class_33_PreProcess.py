import unicodedata
import re

from class_31_HyperParameter import HyperParameter

class PreProcess(HyperParameter):
    """

    """
    def __init__(self):
        """

        """
        HyperParameter.__init__(self)

    def unicode_to_ascii(self, s):
        """
        transform unicode to ascii. Because French have special letter
        that English don't have, so we need transform them into same format
        if we want to train or use them.
        We use unicodeatta.normlize to transoform single character by 'NFC',
        if this character is not Nonspcsing_Mark,
        which means most of time character is 'Lu' and 'Ll'
        https://towardsdatascience.com/difference-between-nfd-nfc-nfkd-and-nfkc-explained-with-python-code-e2631f96ae6c

        'Mn' = Nonspacing_Mark = a nonspacing combining mark (zero advance width)
        """
        #     return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
        return ''.join(c for c in unicodedata.normalize('NFC', s) if unicodedata.category(c) != 'Mn')

    def normalize_string(self, s):
        """
        normalize function complete
        """
        s = self.unicode_to_ascii(s)
        #  \1 is the replacement to use in case of a match, so a repeated word will be replaced by a single word.
        s = re.sub(r'([!.?])', r' \1', s)
        # replace any not letter and .!? with whitespace
        s = re.sub(r'[^a-zA-Z.!?]+', r' ', s)
        # replace several white space into one whitespace. because we replace a lot of non-charcters
        # into whitespace, so we may got multi-whitespace, we need substract to one
        s = re.sub(r'\s+', r' ', s)
        return s

    def transform(self, df):
        """
        clean up text, transfrom 'en' column to normalize and restore them as list
        :return:
        """
        # transform and clean ['english'] column
        corpus_en_list = [self.normalize_string(s) for s in df['english']]

        # add special token <start>/<end> to indicate the beginning and end of a sentence
        # <start> = <BOS>, <end> = <EOS>
        # so raw_in like timestep t, and raw_out like timestep t+1
        corpus_es_in = ['<start> ' + self.normalize_string(s) for s in df["spanish"]]
        corpus_es_out = [self.normalize_string(s) + ' <end>' for s in df["spanish"]]

        return corpus_en_list, corpus_es_in, corpus_es_out