'''
This python file aims to extract frames and performs a facial emotion recognition over the face for each frame read

The structure of folder is the following:
DataSet (root)
    |--- Test
          |--- 500044
                 |--- 5000441001
                            |--- 5000441001.avi
                 |--- 5000441002
                            |--- 5000441002.avi
                 ...
                 |--- 5000441072
                            |--- 5000441072.avi
                 |--- 5000442001
                            |--- 5000442001.avi
                 ...
                 |--- 5000442078
                            |--- 5000442078.avi
    |--- Train
          |---
    |--- Validation
          |---
'''
import os
from Supports.FER.Auxiliary_FER import runner

# Change this path with the path of folder in which are saved the video
path_of_data_folder = "/Volumes/fimp/LM-CScience/dataset/DAiSEE/DataSet"

# Create folder to save final results
current_folder = os.path.abspath(os.getcwd()) + "/"
name_folder_results = "Results_Experiment_FER_DAiSEE/"
final_folder = current_folder + name_folder_results
os.makedirs(final_folder, exist_ok=True)

nested_subfolders = ["Test", "Train", "Validation"]
no_video = 0
data = {}
for each_folder in nested_subfolders:
    data[each_folder] = [[], []]
    for current_path, subfolders, subfiles in os.walk(top=path_of_data_folder + "/" + each_folder):
        for each_sub_file in subfiles:
            if each_sub_file.endswith('.avi') or each_sub_file.endswith('.mp4'):
                no_video += 1
                original_path = current_path + "/" + each_sub_file
                file_without_extension = each_sub_file.split('.')[0]
                new_path = final_folder + each_folder + "/" + file_without_extension
                data[each_folder][0].append(original_path)
                data[each_folder][1].append(new_path)

cont = 0
sampling_in_seconds = 1
for k, v in data.items():
    first_list = (v[0])
    second_list = (v[1])
    for i, (origin_pathfile, final_pathfile) in enumerate(zip(first_list, second_list)):
        cont += 1
        if not os.path.isdir(final_pathfile):
            os.makedirs(final_pathfile, exist_ok=False)
            print("#Video {}/{}\tName: {}\tType: {}\tSampling Frequency: {}\n".
                  format(cont, no_video, final_pathfile.split("/")[-1], k, sampling_in_seconds))
            runner(path_video=origin_pathfile,
                   percentage=sampling_in_seconds,
                   path_result=final_pathfile)
        else:
            print("Video called {} already analyzed!".format(final_pathfile.split("/")[-1]))
