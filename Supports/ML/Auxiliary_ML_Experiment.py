import io

import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import matplotlib.pyplot as plt


def formatted_output_unique_values(tuple_unique, set_name):
    labels = tuple_unique[0]
    numbers = tuple_unique[1]
    print("\n{} set".format(set_name))
    for x, y in zip(labels, numbers):
        print("Label {} --> #{}".format(x, y))
    return


def create_data_window(data, set_label, window):
    X, y = [], []
    for i in range(np.shape(data)[0]):
        sample_data = data[i]
        label = set_label[i]
        for j in range(np.shape(sample_data)[0] - window + 1):
            sample_window = sample_data[j:j + window, :]
            X.append(sample_window)
            y.append(label)
    X, y = np.array(X), np.array(y)
    return X, y


def oversample_dataset(X, y):
    dim2, dim3 = X.shape[1], X.shape[2]
    new_X = [x.flatten() for x in X]
    new_X = np.array(new_X)
    sample_method = SMOTE(random_state=110395, sampling_strategy='auto')
    X_res, y_res = sample_method.fit_resample(new_X, y)
    X_res = np.reshape(a=X_res, newshape=(X_res.shape[0], dim2, dim3))
    y_res = np.reshape(a=y_res, newshape=(-1, 1))
    return X_res, y_res


def undersample_dataset(X, y):
    dim2, dim3 = X.shape[1], X.shape[2]
    new_X = [x.flatten() for x in X]
    new_X = np.array(new_X)
    sample_method = RandomUnderSampler(random_state=110395, sampling_strategy='auto')
    X_res, y_res = sample_method.fit_resample(new_X, y)
    X_res = np.reshape(a=X_res, newshape=(X_res.shape[0], dim2, dim3))
    y_res = np.reshape(a=y_res, newshape=(-1, 1))
    return X_res, y_res


def generate_graph(title_image, path_image, data_of_training, af, show_image=False, save_image=False):
    figure = plt.figure(figsize=(18, 4), edgecolor='b', facecolor='w')
    plt.suptitle(title_image)
    ax1 = figure.add_subplot(121)
    ax1.title.set_text("Accuracy")
    ax1.plot(data_of_training.history[af])
    ax1.plot(data_of_training.history["val_" + af])
    ax1.set_ylabel('Accuracy')
    ax1.set_ylim(bottom=0.0, top=1.0)
    ax1.set_xlabel('Epochs')
    ax1.legend(['Train', 'Validation'], loc='best')

    ax2 = figure.add_subplot(122)
    ax2.title.set_text("Loss")
    ax2.plot(data_of_training.history['loss'])
    ax2.plot(data_of_training.history['val_loss'])

    ax2.set_ylabel('Loss (categorical_crossentropy)')
    ax2.set_xlabel('Epochs')
    ax2.set_ylim(bottom=0.0)
    ax2.legend(['Train', 'Validation'], loc='best')

    if save_image:
        plt.savefig(path_image)

    if show_image:
        plt.show()

    plt.close(fig=figure)
    return


def get_model_summary(model):
    stream = io.StringIO()
    model.summary(print_fn=lambda x: stream.write(x + '\n'))
    summary_string = stream.getvalue()
    stream.close()
    return summary_string
