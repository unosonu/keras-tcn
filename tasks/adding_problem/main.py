from uuid import uuid4

import keras
from utils import data_generator

from tcn import compiled_tcn

x_train, y_train = data_generator(n=200000, seq_length=600)
x_test, y_test = data_generator(n=40000, seq_length=600)


class PrintSomeValues(keras.callbacks.Callback):

    def on_epoch_begin(self, epoch, logs={}):
        print(f'x_test[0:1] = {x_test[0:1]}.')
        print(f'y_test[0:1] = {y_test[0:1]}.')
        print(f'pred = {self.model.predict(x_test[0:1])}.')


def run_task():
    model = compiled_tcn(return_sequences=False,
                         num_feat=x_train.shape[2],
                         num_classes=0,
                         nb_filters=24,
                         kernel_size=8,
                         dilations=[2 ** i for i in range(9)],
                         nb_stacks=1,
                         max_len=x_train.shape[1],
                         use_skip_connections=True,
                         regression=True,
                         dropout_rate=0)

    print(f'x_train.shape = {x_train.shape}')
    print(f'y_train.shape = {y_train.shape}')

    psv = PrintSomeValues()

    # Using sparse softmax.
    # http://chappers.github.io/web%20micro%20log/2017/01/26/quick-models-in-keras/
    model.summary()

    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=15,
              callbacks=[psv], batch_size=256)

    test_acc = model.evaluate(x=x_test, y=y_test, verbose=0)  # loss.
    with open(f'adding_problem_{str(uuid4())[0:5]}.txt', 'w') as w:
        w.write(str(test_acc) + '\n')


if __name__ == '__main__':
    run_task()
