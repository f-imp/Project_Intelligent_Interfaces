import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing import sequence

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import load_model


def load_model_dataframe(path_df):
    df = pd.read_csv(path_df)
    if "Synonyms" not in df.columns:
        synonyms = []
        for i in range(df.shape[0]):
            name = "Model_" + str(i + 1)
            synonyms.append(name)
        df["Synonyms"] = pd.Series(synonyms)

    df.to_csv(path_df, index=False)
    return df


def from_excel_to_csv(path_excel_file, name_sheet, path_output_csv):
    read_file = pd.read_excel(path_excel_file, sheet_name=name_sheet)
    read_file.to_csv(path_output_csv, index=None, header=True)
    return


def create_or_load_dataframe_testset(name_excel_file):
    path_csv = os.path.join(os.getcwd(), name_excel_file.split(".")[0] + ".csv")
    print(path_csv)
    if not os.path.isfile(path_csv):

        from_excel_to_csv(path_excel_file=os.path.join(os.getcwd(), name_excel_file),
                          name_sheet="Form Responses 1",
                          path_output_csv=path_csv)

        df_engagement_groundtruth = pd.read_csv(path_csv)
        df_engagement_groundtruth = df_engagement_groundtruth[['ID partecipante',
                                                               'Quale lezione hai appena seguito?',
                                                               'Average of engagement\'s values',
                                                               'Average of engagement\'s_values_(neural)']]

        df_engagement_groundtruth.columns = ["ID", "Type", "Avg_Engagement", "Avg_Engagement_Neural"]

        compliant_data_format = {"ID_Video": [], "Avg_Engagement": [], "Avg_Engagement_Neural": []}
        for i in range(df_engagement_groundtruth.shape[0]):
            row = df_engagement_groundtruth.values[i:i + 1, :][0]
            record_type = row[1]
            new_id = "Test_" + str(row[0]) + "_"
            if record_type == 'Video-lezione Arduino':
                new_id += "video_arduino"
            elif record_type == 'Video-lezione TED':
                new_id += "video_ted"
            else:
                new_id += "slide_arduino"
            compliant_data_format["ID_Video"].append(new_id)
            compliant_data_format["Avg_Engagement"].append(row[2])
            compliant_data_format["Avg_Engagement_Neural"].append(row[3])
        df = pd.DataFrame.from_dict(compliant_data_format)
        df.to_csv(path_csv, index=False)
        print("Dataframe Created!")
    else:
        print("Dataframe ALREADY CREATED!")
        df = pd.read_csv(path_csv)
    return path_csv, df


def create_dict(cols, df):
    d = {}
    print(cols)
    for each_col in cols:
        d[each_col] = []
    for i in range(df.shape[0]):
        name = df["Synonyms"].values[i]
        d[name] = []
    return d


def create_window(data, window):
    data_windowed = []
    for i in range(data.shape[0] - window + 1):
        data_windowed.append(data[i:i + window, :])
    data_windowed = np.array(data_windowed)
    return data_windowed


def perform_classification(X, model_path):
    X = X.to_numpy()[:, 3:-1]
    mm_scaler = MinMaxScaler(feature_range=(0, 1))
    X = mm_scaler.fit_transform(X=X)
    m = load_model(model_path)
    first_layer = m.layers[0].input_shape
    last_layer = m.layers[-1].output_shape
    n_rows, n_labels = first_layer[1], last_layer[1]
    X_windowed = create_window(data=X, window=n_rows)

    no_samples = X_windowed.shape[0]
    predictions = []
    for i in range(no_samples):
        single_window = X_windowed[i:i + 1, :, :]
        single_prediction = m.predict(single_window)[0]
        idx = np.argmax(single_prediction)
        if n_labels == 2:
            if idx == 0:
                predictions.append(0.0)
            else:
                predictions.append(1.0)
        elif n_labels == 4:
            if idx == 0:
                predictions.append(0.0)
            elif idx == 1:
                predictions.append(0.33)
            elif idx == 2:
                predictions.append(0.66)
            else:
                predictions.append(1.0)
    predictions = np.array(predictions)
    return predictions


def get_engagements_level(path_data, path_models, root):
    df_example = pd.read_csv(os.path.join(root, path_data))
    df_models = load_model_dataframe(os.path.join(root, path_models))
    engagements_levels = dict()
    for i in range(df_models.shape[0]):
        data_model = df_models.values[i]
        domain, no_labels, simbolic_name = data_model[0], data_model[1], data_model[3]
        path_model = os.path.join(root, "2_EngagementClassification", data_model[2], "model.h5")
        print("Execution of {}".format(simbolic_name))
        preds = perform_classification(X=df_example, model_path=path_model)
        avg_preds = round(np.mean(a=preds), 6)
        engagements_levels[simbolic_name] = pd.Series(round(avg_preds * 100, 2))
    df_engagements_levels = pd.DataFrame.from_dict(engagements_levels,
                                                   orient='index',
                                                   columns=["Engagement Prediction"])
    return df_engagements_levels
