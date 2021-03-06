import os
import warnings

import cv2
import numpy as np
import pandas as pd
import torch
from PIL import Image
from Supports.State_of_art import face_detect
from Supports.State_of_art.FER.models import VGG, Variable, F
from Supports.State_of_art.FER.transforms import transforms
from skimage.transform import resize

from Supports.FER.Core_FER import report_experiment, report_details, create_hist, create_timeline, set_fps

warnings.simplefilter("ignore")
np.seterr(divide='ignore', invalid='ignore')


def extract_metrics(csv_path, start_column, end_column, metrics_dict, path_histogram):
    dataframe = pd.read_csv(csv_path, delimiter=',', header=0)
    header = list(dataframe.columns)
    data = dataframe.values
    cardinality = np.shape(data)[0]
    interval = np.arange(0, cardinality, 1).reshape(cardinality, 1)
    # print(interval)
    # print("\n---\n")
    interval = [value for each_sublist in interval for value in each_sublist]
    # print(interval)
    name = []
    pearson_2bar = []
    for i in range(end_column - start_column):
        name_column = header[start_column + i:start_column + i + 1]
        name_column = name_column[0]
        # print("Column name -> \n" + name_column)
        name.append(name_column)
        column_taken = data[:, start_column + i:start_column + i + 1]
        column2array = np.array(column_taken)
        # print("\nColumn2 Array -> \n", column2array)
        column2flattenlist = [value for each_sublist in column2array for value in each_sublist]
        # print("\nColumn2 Flatten -> \n", column2flattenlist)
        metrics_dict[name_column + "_max"] = float(format(np.max(column2array), '.3f'))
        metrics_dict[name_column + "_min"] = float(format(np.min(column2array), '.3f'))
        metrics_dict[name_column + "_avg"] = float(format(np.mean(column2array), '.3f'))
        metrics_dict[name_column + "_std_dev"] = float(format(np.std(column2array), '.3f'))
        pearson_matrix = np.corrcoef(interval, column2flattenlist)
        # print("\nPearson Matrix -> \n" + str(pearson_matrix))
        if np.math.isnan(pearson_matrix[0][1]):
            metrics_dict[name_column + "_pearson"] = float(format(0, '.3f'))
            pearson_2bar.append(float(format(0, '.3f')))
        else:
            metrics_dict[name_column + "_pearson"] = float(format(np.round(pearson_matrix[0][1], 2), '.3f'))
            pearson_2bar.append(float(format(np.round(pearson_matrix[0][1], 2), '.3f')))
        # print("Pearson 2 Bar -> ", pearson_2bar)
    create_hist(name, pearson_2bar, path_histogram)
    return metrics_dict


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def execute_recognition(face, report_exp, emotions, report_det=None):
    cut_size = 44

    transform_test = transforms.Compose([
        transforms.TenCrop(cut_size),
        transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
    ])

    gray = rgb2gray(face)
    gray = resize(gray, (48, 48), mode='symmetric').astype(np.uint8)
    # plt.imshow(gray)
    img = gray[:, :, np.newaxis]

    img = np.concatenate((img, img, img), axis=2)
    img = Image.fromarray(img)
    inputs = transform_test(img)

    net = VGG('VGG19')
    checkpoint = torch.load(
        os.path.join(os.path.abspath(os.getcwd()), "Supports/State_of_art/FER/FER2013_VGG19/PrivateTest_model.t7"),
        map_location=torch.device('cpu'))
    net.load_state_dict(checkpoint['net'])
    # net.cuda()
    net.eval()

    ncrops, c, h, w = np.shape(inputs)

    inputs = inputs.view(-1, c, h, w)
    # inputs = inputs.cuda()
    inputs = Variable(inputs, volatile=True)
    outputs = net(inputs)

    outputs_avg = outputs.view(ncrops, -1).mean(0)  # avg over crops

    score = F.softmax(outputs_avg)
    _, predicted = torch.max(outputs_avg.data, 0)

    threshold = 0.01
    for i in range(len(emotions)):
        value_predicted = round(score.data.cpu().numpy()[i], 3)
        if value_predicted >= threshold and report_det is not None:
            report_det[emotions[i]] += 1
            if str(emotions[i]) == "Angry" or str(emotions[i]) == "Sad" or str(emotions[i]) == "Disgust" or str(
                    emotions[i]) == "Fear":
                report_det['Negative'] += 1
            else:
                report_det['Positive'] += 1

            report_exp[str(emotions[i])].append(format(value_predicted, '.3f'))
        else:
            report_exp[str(emotions[i])].append(format(0, '.3f'))

    e = str(emotions[int(predicted.cpu().numpy())])
    report_exp['high_emotion'].append(e)
    return


def runner(path_video, percentage, path_result):
    list_emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    experiment = report_experiment(list_emotions)

    folder_frames = "frames/"
    folder_faces = "faces/"
    os.makedirs(path_result + "/" + folder_frames, exist_ok=True)
    os.makedirs(path_result + "/" + folder_faces, exist_ok=True)
    # --------- read video -----------------------------------------
    video = os.path.basename(os.path.normpath(path_video))
    name_video = str(video.split('.')[0])
    v = cv2.VideoCapture(path_video)

    # --------- statistics video -----------------------------------
    format_video = str(video.split('.')[1])
    fps = set_fps(format_video, v)

    step_f2f = fps * percentage
    cont = 1
    cont_analyzed = 0
    info = report_details(name_video=video, fps=fps, sampling=percentage, emotions=list_emotions)

    exist_frame, image = v.read()
    while exist_frame:
        if cont == step_f2f:
            cont = 1
        if cont == 1:
            cont_analyzed += 1

            name_frame = "frame_" + str(cont_analyzed)
            path_image = path_result + "/" + folder_frames + name_frame + ".jpg"
            cv2.imwrite(path_image, image)

            name_face = "face_" + str(cont_analyzed)
            path_face = path_result + "/" + folder_faces + name_face + ".jpg"

            image = face_detect.load_image_file(path_image, mode='L')
            face_locations = face_detect.face_locations(image, model='cnn')
            experiment['path_frame'].append(path_image)
            fl = []
            if len(face_locations) == 1:
                for i in range(len(face_locations[0])):
                    fl.append(int((face_locations[0])[i]))

                face_locations = np.array(face_locations)
                face_locations = face_locations[0]
                image2extractface = cv2.imread(path_image)
                experiment['position_face'].append(fl)
                extract_face = image2extractface[face_locations[0]:face_locations[2],
                               face_locations[3]:face_locations[1]]
                cv2.imwrite(path_face, extract_face)
                execute_recognition(extract_face, experiment, report_det=info, emotions=list_emotions)
            else:
                experiment['position_face'].append([0, 0, 0, 0])
                black_image = np.full(shape=(64, 64, 3), fill_value=0)
                cv2.imwrite(path_face, black_image)
                for i in range(len(list_emotions)):
                    experiment[list_emotions[i]].append(format(0.0, '.3f'))
                experiment['high_emotion'].append("face_not_detected")
        cont += 1
        exist_frame, image = v.read()
    # print(cont)
    path_report = path_result + "/" + "report_experiment.csv"
    pd.DataFrame(data=experiment).to_csv(path_report)

    info = extract_metrics(path_report, 3, 10, info, path_result)
    pd.DataFrame(data=info, index=[0]).to_csv(path_result + "/" + "statistics.csv")

    create_timeline(path_file=path_report, emotions=list_emotions, path_result=path_result)

    return
