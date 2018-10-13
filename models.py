from keras.layers import Input, Dense
from keras.models import Model

from keras.models import load_model


def raw_model():
    input_all = Input(shape=(233,), name="input")

    x = Dense(512, activation='relu')(input_all)

    x = Dense(1024, activation='relu')(x)

    x = Dense(512)(x)

    out = Dense(4)(x)

    model = Model(inputs=[input_all], outputs=out)
    model.compile(optimizer='rmsprop', loss='mse')
    return model


def preflop_model():

    # ranks, is_sb, starting stack/500
    input_n = Input(shape=(16,), name="input")

    x = Dense(16, activation='relu')(input_n)
    x = Dense(32, activation='relu')(x)
    x = Dense(16, activation='relu')(x)
    out = Dense(2)(x)
    model = Model(inputs=[input_n], outputs=out)
    model.compile(optimizer='adam', loss='mse')
    return model


def save_model(model, name):
    model.save(name)


def load(name):
    return load_model(name)
