
from class_31_HyperParameter import HyperParameter
from class_32_ImportData import ImportData
from class_33_PreProcess import PreProcess
from class_35_EDA import EDA
from class_36_Tokenize import Tokenize
from class_37_categoory import ToCategory
from class_51_models import Seq2Seq
from class_52_compile_fit import CompileFit
from class_61_analysis import Analysis


def main():
    """
    Pipeline:
    1.Import Data
    :return:
    """
    #************1.Import Data****************
    import_class = ImportData()
    df = import_class.import_data()
    df_train, df_test = import_class.split_data()


    #****************2.Preprocess*************
    pre_class = PreProcess()
    corpus_train_en_list, corpus_train_es_in, corpus_train_es_out = pre_class.transform(df_train)
    corpus_test_en_list, corpus_test_es_in, corpus_test_es_out = pre_class.transform(df_test)

    #****************EDA******************
    # eda_class = EDA()
    # eda_class.eda_length(corpus_en_list)

    #*************tokenize*****************
    token_class = Tokenize()
    _, _, _, train_en_padded, train_en_token = token_class.tokenize(corpus_train_en_list,
                                                                    corpus_train_es_in,
                                                                    corpus_train_es_out,
                                                                    language='en')

    _, _, _, train_es_in_padded, train_es_in_token = token_class.tokenize(corpus_train_en_list,
                                                                          corpus_train_es_in,
                                                                          corpus_train_es_out,
                                                                          language='es_in')

    _, _, _, train_es_out_padded, train_es_out_token = token_class.tokenize(corpus_train_en_list,
                                                                     corpus_train_es_in,
                                                                     corpus_train_es_out,
                                                                     language='es_out')

    _, _, _, test_en_padded, test_en_token = token_class.tokenize(corpus_test_en_list,
                                                                  corpus_test_es_in,
                                                                  corpus_test_es_out,
                                                                  language='en',
                                                                  token = train_en_token)

    _, _, _, test_es_in_padded, test_es_in_token = token_class.tokenize(corpus_test_en_list,
                                                                  corpus_test_es_in,
                                                                  corpus_test_es_out,
                                                                  language='es_in',
                                                                  token = train_es_in_token)

    _, _, _, test_es_out_padded, test_es_out_token = token_class.tokenize(corpus_test_en_list,
                                                                  corpus_test_es_in,
                                                                  corpus_test_es_out,
                                                                  language='es_out',
                                                                  token = train_es_out_token)

    #******************category************************
    cat_class = ToCategory()
    train_es_out_padded_cat = cat_class.to_category(train_es_out_padded)
    test_es_out_padded_cat = cat_class.to_category(test_es_out_padded)
    #
    model_class = Seq2Seq()
    seq_model = model_class.seq_atten()

    compile_class = CompileFit()
    history, hist_dict = compile_class.complie_fit(
        seq_model, train_en_padded, train_es_in_padded, train_es_out_padded_cat
    )

    #***************Analysis***************
    plt_class = Analysis()
    plt_class.plot_history(history)



    return (df, df_train, df_test,
            corpus_train_en_list, corpus_train_es_in, corpus_train_es_out,
           train_en_padded, train_es_in_padded, train_es_out_padded,
            history)


if __name__=="__main__":
    (df, df_train, df_test,
     corpus_train_en_list, corpus_train_es_in, corpus_train_es_out,
     train_en_padded, train_es_in_padded, train_es_out_padded,
     history) = main()
    print("OVER")