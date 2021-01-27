# make picture
import matplotlib.pyplot as plt
# draw picture
import seaborn as sns
import numpy as np

class EDA(object):

    def eda_length(self, raw_list):
        sentence_len = [len(x) for x in raw_list]
        sentence_len_arr = np.array(sentence_len)
        # change the type to numpy array and get 95%/90%/85%th percentile of the data value
        print(f"100%th percentile of sentence lenght is {np.percentile(sentence_len_arr, 100)}")
        print(f"95%th percentile of sentence lenght is {np.percentile(sentence_len_arr, 95)}")
        print(f"90%th percentile of sentence lenght is {np.percentile(sentence_len_arr, 90)}")
        print(f"85%th percentile of sentence lenght is {np.percentile(sentence_len_arr, 85)}")
        print(f"80%th percentile of sentence lenght is {np.percentile(sentence_len_arr, 80)}")
        print(f"70%th percentile of sentence lenght is {np.percentile(sentence_len_arr, 70)}")
        print(f"50%th percentile of sentence lenght is {np.percentile(sentence_len_arr, 50)}")
        # get sorted
        sentence_len.sort()
        plt.plot(np.arange(len(sentence_len)), sentence_len)
        plt.title("Sentence Length Distribution")
        plt.xlabel("Sentence Amount")
        plt.ylabel("Sentence Length")
        plt.show()
        print(
            f"For MAX_SEQ_LEN, 1000 words in one sentce will reasonable to preseve 90% sentence and delete outlier value")

        return None