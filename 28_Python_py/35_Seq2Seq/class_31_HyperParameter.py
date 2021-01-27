
class HyperParameter(object):
    def __init__(self):
        """

        """
        # we can change read file path
        self.PATH = "03_data/"

        # whole dataset is too large, we only use a small sample
        self.SAMPLE = 10000
        self.TEST_SAMPLE = 2000


        # max_words decided how many frequence words will present to you.
        # For instance, if we use max_unique words, 12175 for english part, this menas we will not abnondan any words in sentecne
        # if we set MAX_WORDS=1000, this menas, we only reserve most frequence Top 1000 words in each sentence. On this condition,
        # only some most common words will be resvers
        # if we set MAX_WORDS = 10, only stop words will be resever.
        # in the meantime, word_index and index_word will rematin same and full dictionray

        # self.MAX_WORDS_EN = 12175
        self.MAX_WORDS_EN = 5000
        # the max unique wrod is 16419, but we need to set this paramter in to max+1,
        # because keras.Tokenize() function only keep num_words-1 words, so if we want to keep all words
        # we either add 1 in tokenzie() function, or we set this parameters+1
        # Most important is in to_category() function, keras expect an integer vector from 0 to num_calss
        # but Tokenize() function provide word_index start from 1 to num_words-1,
        # so if we set parameters here as max+1, to_category can find 16419(max word)
        # 16420, memeory out....
        self.MAX_WORDS_ES = 5000
        # self.MAX_WORDS_EN = 1000
        # self.MAX_WORDS_ES = 16419
        # self.MAX_WORDS_ES = 10
        # self.MAX_WORDS_ES = 500

        self.MAX_SEQ_LEN_EN = 100
        self.MAX_SEQ_LEN_ES = 100


        self.EMBEDDING_DIM = 50


        self.BATCH_SIZE = 8
        self.EPOCHS = 3

        self.NAME_STR = 'Seq2Seq'
        """
        If we use max_len to cut sentence, it's ok for english part, but for spanish part
        we will cut the <end>
        
        """
