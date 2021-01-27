from tensorflow.keras import losses
from tensorflow.keras import metrics
from class_31_HyperParameter import HyperParameter

class CompileFit(HyperParameter):
    """

    """
    def __init__(self):
        """

        """
        super(CompileFit, self).__init__()

    def complie_fit(self, model, en_padded, es_in_padded, es_out_padded_cat):
        """

        :return:
        """
        model.compile(optimizer = 'rmsprop',
                      loss = 'categorical_crossentropy',
                      metrics=['categorical_accuracy']
                      # loss = losses.SparseCategoricalCrossentropy()
                      # metrics = metrics.sparse_categorical_accuracy()
                      )
        history = model.fit(x = [en_padded, es_in_padded],
                            y = es_out_padded_cat,
                            batch_size = self.BATCH_SIZE,
                            epochs = self.EPOCHS,
                            verbose = 1,
                            validation_split = 0.2)

        history_dict = [x for x in history.history]

        return history, history_dict