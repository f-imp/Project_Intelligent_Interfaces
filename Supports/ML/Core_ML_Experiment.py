import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import numpy as np
from keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import seaborn as sns

sns.set(rc={'figure.figsize': (8, 8)})
import matplotlib.pyplot as plt

from Supports.ML.Auxiliary_ML_Experiment import oversample_dataset, undersample_dataset, generate_graph, \
    get_model_summary


def execute_model_indians(path_X, path_y, model_nn, n_epochs, bs, lr, path_csv_experiment_data=None,
                          path_image_performances=None, path_confmatrix=None, verbosity=False,
                          path_classification_report=None,
                          path_model=None, binary=False, sampling_strategy=-1, eval_sets=None):
    window_size = (path_X.split(".")[0]).split("_")[-1]
    if verbosity:
        print("Loading of the Datasets...")
    X = np.load(path_X)
    y = np.load(path_y)
    name_loss, name_acc, name_labels = "", "", []
    if binary:
        name_loss, name_acc = "binary_crossentropy", "binary_accuracy"
        name_labels = ["Not Engaged", "Engaged"]
        if verbosity:
            print("Convert problem into a binary one")
        y_binary = []
        for x in y:
            if x != 0:
                y_binary.append(1)
            else:
                y_binary.append(0)
        y = np.array(y_binary)
        y = np.reshape(a=y, newshape=(-1, 1))
    else:
        y = np.reshape(a=y, newshape=(-1, 1))
        name_labels = ["Very Low", "Low", "High", "Very High"]
        name_loss, name_acc = "categorical_crossentropy", "categorical_accuracy"

    sampling_name = ""
    if sampling_strategy == 1:
        sampling_name = "Oversampling"
        if verbosity:
            print("Tackling unbalanced dataset OVERSAMPLING lower classes")
        X, y = oversample_dataset(X=X, y=y)
    elif sampling_strategy == 0:
        sampling_name = "Undersampling"
        if verbosity:
            print("Tackling unbalanced dataset UNDERSAMPLING higher classes")
        X, y = undersample_dataset(X=X, y=y)
    else:
        sampling_name = "No Sampling"
        if verbosity:
            print("No sampling!")

    encoder = OneHotEncoder(sparse=False)
    y_encoded = encoder.fit_transform(y)
    if verbosity:
        print("Splitting Datasets into Training/Testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=11031995)
    if verbosity:
        print("Instantiate the model")
    m, name = model_nn((X_train.shape[1], X_train.shape[2]), y_train.shape[1], lr, af=name_acc, lf=name_loss)
    if verbosity:
        print("Training the model:\t{}".format(name))
    early_stop = EarlyStopping(monitor='val_loss', patience=5)
    history = m.fit(x=X_train, y=y_train, batch_size=bs, epochs=n_epochs, verbose=0, validation_split=0.33,
                    shuffle=True, callbacks=[early_stop])

    epochs_done = len(history.history['loss'])
    if path_csv_experiment_data:
        df = pd.DataFrame(history.history)
        df.to_csv(path_csv_experiment_data)
    scores = m.evaluate(x=X_test, y=y_test, batch_size=bs, verbose=0)
    acc, loss = round(scores[1] * 100, 2), scores[0]
    print("\nAccuracy: {}%\nLoss: {}\n".format(acc, loss))

    if path_image_performances is not None:
        generate_graph(
            title_image="Performance for Model: {}\nWindow: {} - Batch_size: {}\nBinary problem: {} - Sampling: {}\n".format(
                name, window_size, bs, binary, sampling_name),
            path_image=path_image_performances,
            data_of_training=history,
            af=name_acc,
            show_image=verbosity,
            save_image=True)
    else:
        generate_graph(
            title_image="Performance for Model: {}\nWindow: {} - Batch_size: {}\nBinary problem: {} - Sampling: {}\n".format(
                name, window_size, bs, binary, sampling_name),
            path_image="",
            data_of_training=history,
            af=name_acc,
            show_image=verbosity,
            save_image=False)

    if path_model is not None:
        m.save(filepath=path_model, include_optimizer=True)
        description = get_model_summary(m)
        out = open(os.path.join("/".join(path_model.split('/')[:-1]), "model_summary.txt"), 'w')
        out.write(description)
        out.close()

    if verbosity:
        print("The model has been saved successfully at the following path: {}".format("/content/" + name + ".h5"))
    if verbosity:
        print(
            "(It has been saved the Architecture, the Optimizer's end point and the Weights to allow you to restore the whole model)")
    predictions = m.predict(x=X_test)
    real_y_test = [encoder.inverse_transform(np.reshape(x, (-1, predictions.shape[1])))[0][0] for x in y_test]
    real_y_test = np.array(real_y_test)
    # print(np.unique(real_y_test, return_counts=True))
    predicted_classes = [np.argmax(pred) for pred in predictions]
    cm = confusion_matrix(y_true=real_y_test, y_pred=predicted_classes, normalize="pred")
    cr = classification_report(real_y_test, predicted_classes, target_names=name_labels, output_dict=True)
    cr_string = classification_report(real_y_test, predicted_classes, target_names=name_labels, output_dict=False)

    metrics_name = ["precision", "recall", "f1-score", "support"]
    new_cr = dict((k, v) for k, v in cr.items() if k in name_labels)
    df_classification_report = pd.DataFrame.from_dict(new_cr)
    df_classification_report.insert(loc=0, column="Metrics", value=metrics_name)

    if path_classification_report is not None:
        out = open(os.path.join("/".join(path_classification_report.split('/')[:-1]), "classification_report.txt"),
                   'w')
        out.write(cr_string)
        out.close()
        df_classification_report.to_csv(path_classification_report, index=False)

    if verbosity:
        sns.heatmap(cm, annot=True, fmt='.2%', cmap='Blues', square=True, vmax=1, vmin=0, xticklabels=name_labels,
                    yticklabels=name_labels)
        plt.title("Heatmap for Model: {}\nWindow: {}\nBatch_size: {}\nBinary problem: {}\nSampling: {}\n\n".format(name,
                                                                                                                   window_size,
                                                                                                                   bs,
                                                                                                                   binary,
                                                                                                                   sampling_name))
        plt.tight_layout()
        plt.show()
        plt.close('all')
    if path_confmatrix is not None:
        np.save(arr=cm, file=path_confmatrix + ".npy")
        cm_plot = sns.heatmap(cm, annot=True, fmt='.2%', cmap='Blues', square=True, vmax=1, vmin=0,
                              xticklabels=name_labels, yticklabels=name_labels)
        plt.title("Heatmap for Model: {}\nWindow: {}\nBatch_size: {}\nBinary problem: {}\nSampling: {}\n\n".format(name,
                                                                                                                   window_size,
                                                                                                                   bs,
                                                                                                                   binary,
                                                                                                                   sampling_name))
        plt.tight_layout()
        cm_plot.get_figure().savefig(path_confmatrix + ".png")
        plt.close('all')
    return acc, loss, epochs_done


def execute_model_daisee(path_X, path_y, model_nn, n_epochs, bs, lr, path_csv_experiment_data=None,
                         path_image_performances=None, path_confmatrix=None, verbosity=False,
                         path_classification_report=None,
                         path_model=None, binary=False, sampling_strategy=-1, eval_sets=None):
    window_size = (path_X.split(".")[0]).split("_")[-1]
    if verbosity:
        print("Loading of the Datasets...")
    X = np.load(path_X)
    y = np.load(path_y)[:, 0][:, 1:2]
    name_loss, name_acc, name_labels = "", "", []
    if binary:
        name_loss, name_acc = "binary_crossentropy", "binary_accuracy"
        name_labels = ["Not Engaged", "Engaged"]
        if verbosity:
            print("Convert problem into a binary one")
        y_binary = []
        for x in y:
            if x[0] != 0:
                y_binary.append(1)
            else:
                y_binary.append(0)
        y = np.array(y_binary)
        y = np.reshape(a=y, newshape=(-1, 1))
    else:
        name_labels = ["Very Low", "Low", "High", "Very High"]
        name_loss, name_acc = "categorical_crossentropy", "categorical_accuracy"

    sampling_name = ""
    if sampling_strategy == 1:
        sampling_name = "Oversampling"
        if verbosity:
            print("Tackling unbalanced dataset OVERSAMPLING lower classes")
        X, y = oversample_dataset(X=X, y=y)
    elif sampling_strategy == 0:
        sampling_name = "Undersampling"
        if verbosity:
            print("Tackling unbalanced dataset UNDERSAMPLING higher classes")
        X, y = undersample_dataset(X=X, y=y)
    else:
        sampling_name = "No Sampling"
        if verbosity:
            print("No sampling!")

    encoder = OneHotEncoder(sparse=False)
    y_encoded = encoder.fit_transform(y)
    if verbosity:
        print("Splitting Datasets into Training/Testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=11031995)
    if verbosity:
        print("Instantiate the model")
    m, name = model_nn((X_train.shape[1], X_train.shape[2]), y_train.shape[1], lr, af=name_acc, lf=name_loss)
    if verbosity:
        print("Training the model:\t{}".format(name))
    early_stop = EarlyStopping(monitor='val_loss', patience=5)
    history = m.fit(x=X_train, y=y_train, batch_size=bs, epochs=n_epochs, verbose=0, validation_split=0.33,
                    shuffle=True, callbacks=[early_stop])

    epochs_done = len(history.history['loss'])
    if path_csv_experiment_data:
        df = pd.DataFrame(history.history)
        df.to_csv(path_csv_experiment_data)
    scores = m.evaluate(x=X_test, y=y_test, batch_size=bs, verbose=0)
    acc, loss = round(scores[1] * 100, 2), scores[0]
    print("\nAccuracy: {}%\nLoss: {}\n".format(acc, loss))

    if path_image_performances is not None:
        generate_graph(
            title_image="Performance for Model: {}\nWindow: {} - Batch_size: {}\nBinary problem: {} - Sampling: {}\n".format(
                name, window_size, bs, binary, sampling_name),
            path_image=path_image_performances,
            data_of_training=history,
            af=name_acc,
            show_image=verbosity,
            save_image=True)
    else:
        generate_graph(
            title_image="Performance for Model: {}\nWindow: {} - Batch_size: {}\nBinary problem: {} - Sampling: {}\n".format(
                name, window_size, bs, binary, sampling_name),
            path_image="",
            data_of_training=history,
            af=name_acc,
            show_image=verbosity,
            save_image=False)

    if path_model is not None:
        m.save(filepath=path_model, include_optimizer=True)
        description = get_model_summary(m)
        out = open(os.path.join("/".join(path_model.split('/')[:-1]), "model_summary.txt"), 'w')
        out.write(description)
        out.close()

    if verbosity:
        print("The model has been saved successfully at the following path: {}".format("/content/" + name + ".h5"))
    if verbosity:
        print(
            "(It has been saved the Architecture, the Optimizer's end point and the Weights to allow you to restore the whole model)")
    predictions = m.predict(x=X_test)
    real_y_test = [encoder.inverse_transform(np.reshape(x, (-1, predictions.shape[1])))[0][0] for x in y_test]
    real_y_test = np.array(real_y_test)
    # print(np.unique(real_y_test, return_counts=True))
    predicted_classes = [np.argmax(pred) for pred in predictions]
    cm = confusion_matrix(y_true=real_y_test, y_pred=predicted_classes, normalize="pred")
    cr = classification_report(real_y_test, predicted_classes, target_names=name_labels, output_dict=True)
    cr_string = classification_report(real_y_test, predicted_classes, target_names=name_labels, output_dict=False)

    metrics_name = ["precision", "recall", "f1-score", "support"]
    new_cr = dict((k, v) for k, v in cr.items() if k in name_labels)
    df_classification_report = pd.DataFrame.from_dict(new_cr)
    df_classification_report.insert(loc=0, column="Metrics", value=metrics_name)

    if path_classification_report is not None:
        out = open(os.path.join("/".join(path_classification_report.split('/')[:-1]), "classification_report.txt"),
                   'w')
        out.write(cr_string)
        out.close()
        df_classification_report.to_csv(path_classification_report, index=False)

    if verbosity:
        sns.heatmap(cm, annot=True, fmt='.2%', cmap='Blues', square=True, vmax=1, vmin=0, xticklabels=name_labels,
                    yticklabels=name_labels)
        plt.title("Heatmap for Model: {}\nWindow: {}\nBatch_size: {}\nBinary problem: {}\nSampling: {}\n\n".format(name,
                                                                                                                   window_size,
                                                                                                                   bs,
                                                                                                                   binary,
                                                                                                                   sampling_name))
        plt.tight_layout()
        plt.show()
        plt.close('all')
    if path_confmatrix is not None:
        np.save(arr=cm, file=path_confmatrix + ".npy")
        cm_plot = sns.heatmap(cm, annot=True, fmt='.2%', cmap='Blues', square=True, vmax=1, vmin=0,
                              xticklabels=name_labels, yticklabels=name_labels)
        plt.title("Heatmap for Model: {}\nWindow: {}\nBatch_size: {}\nBinary problem: {}\nSampling: {}\n\n".format(name,
                                                                                                                   window_size,
                                                                                                                   bs,
                                                                                                                   binary,
                                                                                                                   sampling_name))
        plt.tight_layout()

        cm_plot.get_figure().savefig(path_confmatrix + ".png")
        plt.close('all')
    return acc, loss, epochs_done
