from tensorflow.keras.layers import Embedding, Lambda, Dot, Activation, Concatenate, Dropout, Input, LSTM, Dense
from tensorflow.keras import Model
from tensorflow.keras import backend as K

# draw the structure of this model
from tensorflow.keras.utils import model_to_dot, plot_model
# dispaly structure and saved picture
from IPython.display import Image, display


from class_31_HyperParameter import HyperParameter

class Seq2Seq(HyperParameter):
    """

    """

    def __init__(self):
        """

        """
        HyperParameter.__init__(self)

    def seq_atten(self):
        """

        :return:
        """
        self.encoder_input_1 = Input(shape=(self.MAX_SEQ_LEN_EN,), name='encoder_input_layer')
        # if we didn't assign input_shape, Embedding layer will use input_length as input_shape
        # which means it will fit Input layers and input_shape will be padded with english part sentence length
        # enghlish sentence maximize we set as 100, but actually it should longer than that, as least 300
        # Typically, input_dim show be max
        encoder_embed_2 = Embedding(input_dim=self.MAX_WORDS_EN,
                                    output_dim=self.EMBEDDING_DIM,
                                    input_length=self.MAX_SEQ_LEN_EN,
                                    name='encoder_embedding_layer')(self.encoder_input_1)
        # this layer can be imporoved and replaced
        # LSTM is read each word, so input is individual word vector
        encoder_lstm_3 = LSTM(units=self.EMBEDDING_DIM,
                              return_sequences=True,
                              return_state=True,
                              dropout=0.2,
                              name='encoder_lstm_3')
        encoder_outputs, state_h, state_c = encoder_lstm_3(encoder_embed_2)
        self.encoder_states = [state_h, state_c]

        # Set up the decoder, using `encoder_states` as initial state.
        # the shape of decoder_inputs is set to None so it can translate
        # with a single word input, not necessary a sentence input
        self.decoder_inputs_4 = Input(shape=(None,), name='decoder_input_4')
        # deocder didn't have input_length, it seems no sentence length limitation
        self.decoder_embedding_5 = Embedding(input_dim=self.MAX_WORDS_ES,
                                        output_dim=self.EMBEDDING_DIM,
                                        name='decoder_embedding_5')(self.decoder_inputs_4)
        self.decoder_lstm_6 = LSTM(units=self.EMBEDDING_DIM,
                              return_sequences=True,
                              return_state=True,
                              dropout=0.2,
                              name='decoder_lstm_6')
        decoder_output, _, _ = self.decoder_lstm_6(self.decoder_embedding_5, initial_state=self.encoder_states)

        # Transform encoder outputs to a space which can be aligned with decoder output
        encoder_outputs_transformed = Dense(units=self.EMBEDDING_DIM,
                                            activation=None,
                                            use_bias=False)(encoder_outputs)

        # calculate alignment between decoder and encoder
        attention = Dot(axes=[2, 2])([decoder_output, encoder_outputs_transformed])
        attention = Activation('tanh')(attention)

        # Normalize alignment score
        attention = Activation('softmax')(attention)

        # weighted sum
        context = Dot(axes=[2, 1])([attention, encoder_outputs])

        # Concatenate context with decoder output
        decoder_combined_context = Concatenate(axis=-1)([context, decoder_output])

        self.decoder_dense = Dense(units=self.MAX_WORDS_ES, activation='softmax')(decoder_combined_context)
        # decoder_dense = Dense(units = self.MAX_WORDS_ES, activation = 'softmax')
        # decoder_final_output = decoder_dense(decoder_combined_context)

        model = Model(inputs=[self.encoder_input_1, self.decoder_inputs_4],
                      outputs=self.decoder_dense)

        model.summary()

        dot_img_file = '04_images/10_Seq2Seq_attention.png'
        plot_model(model, to_file=dot_img_file, show_shapes=True)
        display(Image(filename='04_images/10_Seq2Seq_attention.png'))

        return model

    def predict(self):
        """

        :return:
        """
        # encoder_input_1 = Input(shape=(self.MAX_SEQ_LEN_EN,), name='encoder_input_layer')
        # # if we didn't assign input_shape, Embedding layer will use input_length as input_shape
        # # which means it will fit Input layers and input_shape will be padded with english part sentence length
        # # enghlish sentence maximize we set as 100, but actually it should longer than that, as least 300
        # # Typically, input_dim show be max
        # encoder_embed_2 = Embedding(input_dim=self.MAX_WORDS_EN,
        #                             output_dim=self.EMBEDDING_DIM,
        #                             input_length=self.MAX_SEQ_LEN_EN,
        #                             name='encoder_embedding_layer')(encoder_input_1)
        # # this layer can be imporoved and replaced
        # # LSTM is read each word, so input is individual word vector
        # encoder_lstm_3 = LSTM(units=self.EMBEDDING_DIM,
        #                       return_sequences=True,
        #                       return_state=True,
        #                       dropout=0.2,
        #                       name='encoder_lstm_3')
        # encoder_outputs, state_h, state_c = encoder_lstm_3(encoder_embed_2)
        # encoder_states = [state_h, state_c]

        # encoder and decoder models in inference
        # encoder_inputs comes from english input layer
        # encoder_states also come from output of encoder_LSTM
        encoder_model = Model(inputs = self.encoder_input_1,
                              outputs = self.encoder_states)

        decoder_state_input_h = Input(shape = (self.EMBEDDING_DIM,), name = "decoder_h")
        decoder_state_input_c = Input(shape=(self.EMBEDDING_DIM,), name="decoder_c")
        decoder_state_inputs = [decoder_state_input_h, decoder_state_input_c]

        # decoder_embedding comes from france decoder part, which have
        decoder_embed = self.decoder_embedding_5(self.decoder_inputs_4)
        decoder_outputs, state_h, state_c = self.decoder_lstm_6(decoder_embed,
                                                                initial_state = decoder_state_inputs)

        deocder_states = [state_h, state_c]
        decoder_outputs = self.decoder_dense(deocder_states)

        decoder_model = Model(inputs = [self.decoder_inputs_4] + decoder_state_inputs,
                              outpus = [decoder_outputs]  + deocder_states)

        decoder_model.summary()

        dot_img_file = '04_images/11_encoder_model.png'
        plot_model(decoder_model, to_file=dot_img_file, show_shapes=True)
        display(Image(filename='04_images/11_encoder_model.png'))

        dot_img_file = '04_images/12_decoder_model.png'
        plot_model(decoder_model, to_file=dot_img_file, show_shapes=True)
        display(Image(filename='04_images/12_decoder_model.png'))

        return encoder_model, decoder_model

    def decode_sequence(input_seq):  # input_seq is a English sentence

        # Encode the input as state vectors.
        states_value = encoder_model.predict(input_seq)

        # Generate empty target sequence of length 1. (i.e. we translate word by word)
        target_seq = np.zeros((1, 1))

        # Populate the start symbol of target sequence with the start character.
        target_seq[0, 0] = fr_tokenizer.word_index["<start>"]

        # Generate word by word using the encode state and the last
        # generated word

        decoded_sentence = []

        while True:

            output_tokens, h, c = decoder_model.predict(
                [target_seq] + states_value)

            # Get the most likely word
            sampled_token_index = np.argmax(output_tokens[0, 0, :])

            # Look up the word by id
            sampled_word = reverse_fr_word_index[sampled_token_index]

            decoded_sentence.append(sampled_word)

            # Exit condition: either hit max length
            # or find stop character.
            if (sampled_word == '<end>' or len(decoded_sentence) == max_fr_len):
                break

            # Update the target sequence with newly generated word.
            target_seq[0, 0] = sampled_token_index

            # Update states
            states_value = [h, c]

        return ' '.join(decoded_sentence)