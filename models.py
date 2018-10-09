from keras.layers import Input, Dense
from keras.models import Model


def raw_model():
    input_all = Input(shape=(233,), name="input")

    x = Dense(512, activation='relu')(input_all)

    x = Dense(1024, activation='relu')(x)

    x = Dense(512)(x)

    out = Dense(4)(x)

    model = Model(inputs=[input_all], outputs=out)
    model.compile(optimizer='rmsprop', loss='mse')
    return model
