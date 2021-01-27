import pandas as pd
import numpy as np
# plot image
import matplotlib.pyplot as plt
from class_31_HyperParameter import HyperParameter

class Analysis(HyperParameter):
    """

    """

    def plot_history(self, history):
        """
        This function is used for plot classification self.history result
        :param self.history:
        :return:
        """
        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch

        # ****loss plost *******************
        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('loss')
        plt.plot(hist['epoch'], hist['loss'],
                 label='Train loss')
        plt.plot(hist['epoch'], hist['val_loss'],
                 label='Val loss')
        plt.ylim([0, 3])
        plt.legend()
        plt.savefig(f'04_images/{self.NAME_STR}_loss.png', dpi=150, format='png')
        # plt.savefig(f'/googledrive/MyDrive/04_images/{self.NAME_STR}_loss.png', dpi=150, format='png')

        # ****************accuracy plot******************
        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.plot(hist['epoch'], hist['accuracy'],
                 label='Train Accuracy')
        plt.plot(hist['epoch'], hist['val_accuracy'],
                 label='Val Accuracy')
        plt.ylim([0, 1])
        plt.legend()
        plt.savefig(f'04_images/{self.NAME_STR}_acc.png', dpi=150, format='png')
        # plt.savefig(f'/googledrive/MyDrive/04_images/{self.NAME_STR}_acc.png', dpi=150, format='png')
        plt.show()
        return hist


