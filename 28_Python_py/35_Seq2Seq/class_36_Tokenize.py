from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from class_31_HyperParameter import HyperParameter

class Tokenize(HyperParameter):
    """

    """

    def __init__(self):
        """

        """
        HyperParameter.__init__(self)


    def tokenize(self, corpus_en_list, corpus_es_in, corpus_es_out, language ,token=None):
        """
        Argus:
        -----
        language:str
            we use this to control which paramters we use

        token:
            When we provide token we train_tokenize, we means use train_tokenzie to fit test dataset
        :return:
        """
        if language == 'en':
            MAX_WORDS = self.MAX_WORDS_EN
            corpus = corpus_en_list
            MAX_SEQ_LEN = self.MAX_SEQ_LEN_EN
        elif language == 'es_in':
            MAX_WORDS = self.MAX_WORDS_ES
            corpus = corpus_es_in
            MAX_SEQ_LEN = self.MAX_SEQ_LEN_ES
        elif language == 'es_out':
            MAX_WORDS = self.MAX_WORDS_ES
            corpus = corpus_es_out
            MAX_SEQ_LEN = self.MAX_SEQ_LEN_ES
        else:
            print("language input error")

        # this is test part
        if token!=None:
            # because we don't have <OOV> requirement
            # (each words need to be represent in translate task), so we don't assign <OOV>
            print(f"MAX_WORDS is {MAX_WORDS}")
            # This function only keep the most common num_words-1 words to be kept.
            # So, if we want to keep all words, we need to plus 1 in here
            # tokenizer = Tokenizer(filters='', num_words = MAX_WORDS, oov_token="<OOV>")
            # use training tokenizer
            tokenizer = token
            tokenizer.fit_on_texts(corpus)
            seq = tokenizer.texts_to_sequences(corpus)
            print(f"MAX_SEQ_LEN is {MAX_SEQ_LEN}")
            padded = pad_sequences(seq, maxlen=MAX_SEQ_LEN, padding='post')
            word_index, index_word = tokenizer.word_index, tokenizer.index_word

        # this is train part
        else:
            # because we don't have <OOV> requirement
            # (each words need to be represent in translate task), so we don't assign <OOV>
            print(f"MAX_WORDS is {MAX_WORDS}")
            # This function only keep the most common num_words-1 words to be kept.
            # So, if we want to keep all words, we need to plus 1 in here
            tokenizer = Tokenizer(filters='', num_words = MAX_WORDS, oov_token="<OOV>")
            tokenizer.fit_on_texts(corpus)
            seq = tokenizer.texts_to_sequences(corpus)
            print(f"MAX_SEQ_LEN is {MAX_SEQ_LEN}")
            padded = pad_sequences(seq, maxlen=MAX_SEQ_LEN, padding='post')
            word_index, index_word = tokenizer.word_index, tokenizer.index_word


        return word_index, index_word, seq, padded, tokenizer



    def sequence_to_text(self, padded, index_word):
        """
        Use this function to convert padded sequnce back to text according to word_index
        """
        # create a empty list
        word_list = []
        for idx, i in enumerate(padded):
            # for every word in self.question_padded[0]=sentence, put it into a list
            words = np.array([index_word.get(word) for word in i])
            # insert into list
            word_list.append(words)
        # create a dictionary to build DataFrame
        dic = {"sequence_to_text": word_list}
        word_df = pd.DataFrame(dic)
        return word_df


