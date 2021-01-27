from tensorflow.keras.utils import to_categorical


from class_31_HyperParameter import HyperParameter


class ToCategory(HyperParameter):
    """

    """
    def __init__(self):
        """

        """
        # HyperParameter.__init__(sefl)
        super(ToCategory, self).__init__()

    def to_category(self, padded):
        """
        Argus:
        -----

        :param padded:
        :return:
        """
        padded_cat = to_categorical(padded, num_classes = self.MAX_WORDS_ES)
        print(padded_cat.shape)

        return padded_cat


