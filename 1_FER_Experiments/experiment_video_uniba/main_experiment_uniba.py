'''
This python file aims to extract frames and performs a facial emotion recognition over the face for each frame read

The structure of folder is the following:
data (root)
    |--- Test_4
            |--- baseline
            |--- slide-arduino
                    |--- video.mp4
            |--- video-ted
                    |--- video.mp4
    ...
    |--- Test_51
            |--- baseline
            |--- slide-arduino
                    |--- video.mp4
            |--- video-arduino
                    |--- video.mp4
            |--- video-ted
                    |--- video.mp4
    ...
    |--- Test_74

NB: Not all test's folders contains all of three subfolders (slide-arduino, video-arduino, video-ted)
Each video is related to a number of test and has been recorded under a set of settings (not always all of three ways)
'''
import os
from Supports.FER.Auxiliary_FER import runner

# Change this path with the path of folder in which are saved the video
path_of_data_folder = "/Volumes/fimp/LM-CScience/INTINT/IntelligentInterfaces_FER/Prj_ELEARNING/data"

# Create folder to save final results
current_folder = os.path.abspath(os.getcwd()) + "/"
name_folder_results = "Results_Experiment_FER_Uniba/"
final_folder = current_folder + name_folder_results
os.makedirs(final_folder, exist_ok=False)

video_original_path = []
new_name = []
for current_path, subfolders, subfiles in os.walk(top=path_of_data_folder):
    for each_sub_file in subfiles:
        if each_sub_file.endswith('.mp4'):
            path = current_path + "/" + each_sub_file
            path_splitted = path.split("/")
            new_parts = path_splitted[len(path_splitted) - 3:-1]
            new_filename = "_".join(new_parts)
            new_filename = new_filename.replace("-", "_")
            video_original_path.append(path)
            new_name.append(new_filename)

sampling_in_seconds = 10
for i, (original_path, final_path) in enumerate(zip(video_original_path, new_name)):
    folder_result_single_experiment = final_folder + final_path
    os.makedirs(folder_result_single_experiment, exist_ok=False)
    print(
        "\nExecution of FER over Video {}/{}\n\tPath of Video: {}\n\tSampling: every {} second[s]\n\tThis step could require some minutes ...".format(
            str(i + 1),
            str(len(video_original_path)),
            original_path,
            sampling_in_seconds))
    runner(path_video=original_path,
           percentage=sampling_in_seconds,
           path_result=folder_result_single_experiment)
