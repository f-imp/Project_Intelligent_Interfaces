'''
This python file aims to extract frames and performs a facial emotion recognition over the face for each frame read

The structure of folder is the following:
data (root)
    |--- Subject_26_Vid_1.avi
    |--- Subject_26_Vid_x.avi
    |--- Subject_26_Vid_5_1.avi
    |--- Subject_26_Vid_5_2.avi
    ...
    |--- Subject_27_Vid_1.wmv
    ...
    |--- Subject_32_Vid_7.wmv
    ...
    |--- Subject_57_Vid_4.MP4
    ...
'''
import os
from Supports.FER.Auxiliary_FER import runner

# Change this path with the path of folder in which are saved the video
path_of_data_folder = "/Volumes/fimp/LM-CScience/INTINT/IntelligentInterfaces_FER/Prj_Engagement/data"

# Create folder to save final results
current_folder = os.path.abspath(os.getcwd()) + "/"
name_folder_results = "Results_Experiment_FER_Indians/"
final_folder = current_folder + name_folder_results
os.makedirs(final_folder, exist_ok=False)

sampling_in_seconds = 10
for i, each_video in enumerate(os.listdir(path_of_data_folder)):
    if not each_video.startswith(".DS_Store"):
        name = each_video.split(".")[0]
        folder_result_single_experiment = final_folder + name
        os.makedirs(folder_result_single_experiment, exist_ok=False)
        print("\n", each_video, "\t -> \t", each_video.split(".")[0])
        print(
            "Execution of FER over Video {}/{}\n\tSampling: every {} second[s]\n\tThis step could require some minutes ...".format(
                str(i + 1),
                str(len(os.listdir(path_of_data_folder))),
                sampling_in_seconds))
        runner(path_video=path_of_data_folder + "/" + each_video,
               percentage=sampling_in_seconds,
               path_result=folder_result_single_experiment)
