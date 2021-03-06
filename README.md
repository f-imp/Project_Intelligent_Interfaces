# Engagement Classification exploiting Facial Emotion's Temporal Sequences
<b>Professor:</b> De Carolis Nadja Berardina<br>
<b>Supervisor:</b> Dott. Macchiarulo Nicola

## Description
This software aims to build a machine learning model ables to classify the people engagement's level while they are watching a video, 
starting from the level of face's emotions catched through by a Facial Emotion Recognition (FER) System.<br>

## External Sources

1. Facial Emotion Recognition (FER) System - [link](https://github.com/WuJie1010/Facial-Expression-Recognition.Pytorch)<br>
2. Face Detection System - [link](https://github.com/ageitgey/face_recognition)<br>
3. Dataset 1 - Indians People - [link](https://drive.google.com/drive/folders/1mBBZ_uzM7g8_SATRo7c7YnEPouAP6jCH)<br>
4. Dataset 2 - DAISEE - [link](https://iith.ac.in/~daisee-dataset/)

## Dependencies
* Python 3.7 (or greater)
* Matplotlib
* Numpy
* Pandas
* Seaborn

### Face Detection & FER Systems
* PyTorch >= 0.2.0
* OpenCV
* PIL
* Tkinter
* dlib
* face\_recognition\_model

### Perform Classification
* sklearn
* imblearn
* Keras

## Instructions

### Project Tree

```bash
Project_Intelligent_Interfaces
├── 1_FER_Experiments
│   ├── examples
│   │   ├── FER_Gasperini
│   │   ├── FER_WithoutFace
│   │   ├── gasperini.mp4
│   │   └── without_face.mp4
│   ├── experiment_video_DAiSEE
│   │   ├── Labels
│   │   ├── Results_Experiment_FER_DAiSEE     <--(*)
│   │   └── main_experiment_DAiSEE.py
│   ├── experiment_video_indians
│   │   ├── Results_Experiment_FER_Indians    <--(*)
│   │   ├── labels.csv
│   │   ├── labels.xlsx
│   │   └── main_experiment_indians.py
│   └── experiment_video_uniba
│       ├── Results_Experiment_FER_Uniba      <--(*)
│       └── main_experiment_uniba.py
├── 2_EngagementClassification
│   ├── Daisee
│   │   ├── 1_Exploration_Data.ipynb
│   │   ├── 2_Generate_Dataset.ipynb
│   │   ├── 3_Execute_Model.ipynb
│   │   ├── 4_Analyze_Results.ipynb
│   │   ├── Datasets_Generated
│   │   ├── FER_Daisee_Results                <--(*)
│   │   ├── FER_Daisee_Results_Analysis
│   │   └── New_matching_folder
│   ├── Indians
│   │   ├── 1_Exploration_Data.ipynb
│   │   ├── 2_Generate_Dataset.ipynb
│   │   ├── 3_Execute_Model.ipynb
│   │   ├── 4_Analyze_Results.ipynb
│   │   ├── Datasets_Generated
│   │   ├── FER_Indians_Results               <--(*)
│   │   └── FER_Indians_Results_Analysis
│   └── best_models.csv
├── 3_TestModels
│   ├── Examples
│   │   └── Classification.ipynb
│   └── Uniba
│       ├── 1_Perform_Classification.ipynb
│       ├── 2_Result_Analysis.ipynb
│       ├── Completed_data_new.csv
│       ├── Completed_data_new.xlsx
│       ├── Results_Analysis
│       └── results_uniba.csv
├── GUI_FER.py
├── README.md
├── Supports
│   ├── FER
│   │   ├── Auxiliary_FER.py
│   │   └── Core_FER.py
│   ├── ML
│   │   ├── Auxiliary_ML_Experiment.py
│   │   ├── Core_ML_Experiment.py
│   │   └── Models.py
│   ├── State_of_art
│   │   ├── FER
│   │   │   ├── FER2013_VGG19
│   │   │   │   └── PrivateTest_model.t7      <--(*)
│   │   │   ├── models
│   │   │   └── transforms
│   │   └── face_detect
│   └── TEST
│       └── Auxiliary.py
└── env
```
**NB:** All those folders in which there is this symbol " <--(*) " are too much 
bigger to be upload on GitHub and so they are going to be available (for the download)
at the following links: <br> 
<li> Results_Experiment_FER_DAiSEE <br> https://drive.google.com/file/d/1ZUOa5Oh880SqaTlsIf3yhtY1SXl8H2ru/view?usp=sharing </li>
<li> Results_Experiment_FER_Indians <br> https://drive.google.com/file/d/1HIrGpikjr_0IURNza7ExtLCu2XhBHYh3/view?usp=sharing </li>
<li> Results_Experiment_FER_Uniba <br> https://drive.google.com/file/d/19unEdAe2jBfdRI-Vw3dUUUWSJAHmfmlo/view?usp=sharing </li>
<li> FER_Daisee_Results - Best Models<br> https://drive.google.com/file/d/1By2Wi0fDa-29rLhdCNplUJBg4RBGebzs/view?usp=sharing </li>
<li> FER_Indians_Results - Best Models<br> https://drive.google.com/file/d/1zfm94JBbBW78TgwmTPnWwAzDEgH6VQbh/view?usp=sharing </li>
<li> PrivateTest_model.t7: See the Repository of FER_System </li>

**NB (2):** In *Fer_Daisee_Results* and in *Fer_Indians_Results* are available only the best models


### Perform Facial Emotion Recognition 

This task can be achieved using the GUI_FER.py file, using the command 'Run' available in your IDE or 
invoking the execution through by the command line with the following code:

```bash
python3 GUI_FER.py
```
<b>NB:</b> The following command exploits the environment (global/local) related to the folder on your device, so please check that all the dependencies have been installed/updated.

The main function is called ***runner*** and is located at the path ***/Supports/FER/Auxiliary_FER.py*** and has the following signature:
```python
runner(path_video, percentage, path_result)
```
Where the **path\_video** is the absolute path file, the **percentage** is the number of second among consecutive frames and **path\_result** is the path in which will be saved all the results.<br>
This function produces:
* **frames (folder)**: in which have been saved all frames (as jpg images)
* **faces (folder)**: in which have been saved all faces, extracted from frames (as jpg images), and useful to perform the emotion recognition
* **histogram.png**: an image of the Pearson Correlation among emotions
* **report\_experiment.csv**: a dataset in which have been saved all the emotion' levels, for each analyzed frame.
* **statistics.csv**: a dataset with a set of statistics for each emotion *[count, max, min, avg, std\_dev, pearson]* 
* **timeline\_emotion**: a timeline to inspect the trend of each emotion

| **Histogram**      |
|--------------------|
| <img src="https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/1_FER_Experiments/examples/FER_Gasperini/histogram.png">|

| **Timeline**      | 
|-------------------|
| <img src="https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/1_FER_Experiments/examples/FER_Gasperini/timeline_emotion.png">|

### Perform Classification

#### 1. Generate Datasets

In order to exploit emotions levels of each frame into a ML model, it must be built a dataset sliced at every timestep to allow the model to learn the evolution
of a set of consecutive temporal sequences; to do this, it has been used the following function:
```python
def create_data_window(data, set_label, window):
    X, y = [], []
    for i in range(np.shape(data)[0]):
        sample_data = data[i]
        label = set_label[i]
        for j in range(np.shape(sample_data)[0] - window +1):
            sample_window = sample_data[j:j + window, :]
            X.append(sample_window)
            y.append(label)
    X, y = np.array(X), np.array(y)
    return X, y
```
This function takes as input:
* **data**: a bidimensional numpy array **shape(*n\_rows*, *n\_cols*)**
* **set\_label**: a numpy array with all labels (one-to-one correspondence with *data*)**shape(*n\_rows*, 1)**
* **window**: an integer *x*, constrained as follow: 0<*x*<*n\_rows*

It produces a new dataset (both *X* and *y*) of size (*n\_rows*, *window*, *n\_cols*).
##### Original Dataset
| **Values** | 3   | 4   | 9   | 15  | 25  | 7   |
|------------|-----|-----|-----|-----|-----|-----|
| **Labels** | 'a' | 'b' | 'a' | 'c' | 'd' | 'e' |

##### Windowed Dataset (window=3)

###### 1<sup>st</sup> SLICE
| **Values** | 3   | 4   | 9   |
|------------|-----|-----|-----|
| **Labels** | 'a' | 'b' | 'a' |

###### 2<sup>nd</sup> SLICE
| **Values** | 4   | 9   | 15  |
|------------|-----|-----|-----|
| **Labels** | 'b' | 'a' | 'c' |

###### 3<sup>rd</sup> SLICE

| **Values** | 9   | 15  | 25  |
|------------|-----|-----|-----|
| **Labels** | 'a' | 'c' | 'd' |

###### 4<sup>th</sup> SLICE

| **Values** | 15  | 25  | 7   |
|------------|-----|-----|-----|
| **Labels** | 'c' | 'd' | 'e' |


#### 2. Build ML Models

There are 6 different Models available at *'/Supports/ML/Models.py'* and each of them try to exploit a different feature like:
* Easy and Deep LSTM Model with *return sequences*
* Convolutional Networks
* Easy and Deep LSTM 

### 3. Training and Test Models
The tuning phase involved several parameters, like:
* **Batch\_size**
* **Different window\_size** of the dataset
* **Tackle Unbalanced dataset**: exploiting *original*, *undersampling* and *oversampling*
* **Classification Mode**: return binary or multiclass predictions

#### 3.1 Indians Dataset
These are the best configurations (*NB:* binary and multiclass):

| **Classification Style** | **Binary**                           | **Multiclass**                       |
|--------------------------| -------------------------------------| -------------------------------------|
| **Model**                | Convolutional Network                | Convolutional Network                |
| **Path function**        | */Supports/ML/Models/Model\_2()*     | */Supports/ML/Models/Model\_2()*     |
| **Synonymous**           | Model\_1                             | Model\_2                             |
| **Window-size**          |  9                                   |  9                                   |
| **Tackle Unbalanced**    | Oversampling                         | Oversampling                         |
| **Batch-Size**           | 32                                   | 64                                   |
| **Learning Rate**        | 1e-03                                | 1e-03                                |

These are the performances graphs and confusion matrices of the best models to perform a binary (left) and a multiclass (right) 
prediction over '*Indians*' Dataset:

| **Performances of Binary Model** |
|----------------------------------|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Indians/FER_Indians_Results/FER_Indians_Results_Padded_11/FER_Indians_Results_Window_9/Convolutional_Network_Window_9_Binary_Oversampling_32_1e-03/performance.png)|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Indians/FER_Indians_Results/FER_Indians_Results_Padded_11/FER_Indians_Results_Window_9/Convolutional_Network_Window_9_Binary_Oversampling_32_1e-03/confusion_matrix.png)|

| **Performances of Multiclass Model** |
|--------------------------------------|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Indians/FER_Indians_Results/FER_Indians_Results_Padded_11/FER_Indians_Results_Window_9/Convolutional_Network_Window_9_Multiclass_Oversampling_64_1e-03/performance.png)|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Indians/FER_Indians_Results/FER_Indians_Results_Padded_11/FER_Indians_Results_Window_9/Convolutional_Network_Window_9_Multiclass_Oversampling_64_1e-03/confusion_matrix.png)|


#### 3.2 DAISEE Dataset
These are the best configurations (*NB:* binary and multiclass):

| **Classification Style** | **Binary**                                 | **Multiclass**                            |
|--------------------------| -------------------------------------------| ------------------------------------------|
| **Model**                | LSTM with return sequences                 | LSTM with return sequences                |
| **Path function**        | */Supports/ML/Models/Model\_6()*           | */Supports/ML/Models/Model\_6()*          |
| **Synonymous**           | Model\_3                                   | Model\_4                                  |
| **Window-size**          | 9                                          | 9                                         |
| **Tackle Unbalanced**    | Oversampling                               | Oversampling                              |
| **Batch-Size**           | 128                                        | 128                                       |
| **Learning Rate**        | 1e-03                                      | 1e-03                                     |

These are the performances graphs and confusion matrices of the best models to perform a binary (left) and a multiclass (right) 
prediction over '*DAISEE*' Dataset:

| **Performances of Binary Model** |
|----------------------------------|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Daisee/FER_Daisee_Results/FER_Daisee_Results_Window_9/LSTM_with_return_sequences4_Window_9_Binary_Oversampling_128_1e-03/performance.png)|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Daisee/FER_Daisee_Results/FER_Daisee_Results_Window_9/LSTM_with_return_sequences4_Window_9_Binary_Oversampling_128_1e-03/confusion_matrix.png)|

| **Performances of Multiclass Model** |
|--------------------------------------|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Daisee/FER_Daisee_Results/FER_Daisee_Results_Window_9/LSTM_with_return_sequences4_Window_9_Multiclass_Oversampling_128_1e-03/performance.png)|
|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/2_EngagementClassification/Daisee/FER_Daisee_Results/FER_Daisee_Results_Window_9/LSTM_with_return_sequences4_Window_9_Multiclass_Oversampling_128_1e-03/confusion_matrix.png)|

### 4. Test Best Models over '*Uniba*' Dataset
In this dataset, used for the test phase, is not reported the label for each frame neither at least for each video; it's only available an average value of the engagement shown by person in the video.<br>
Hence, the testing phase required to average values of the frame-by-frame predictions in order to have a continuos value [0,1] which is comparable with the given ground truth.<br><br>

This is the **Mean Squared Error** among the given average values and resulting averaged predictions.<br>

|![alt text](https://github.com/f-imp/Project_Intelligent_Interfaces/blob/master/3_TestModels/Uniba/Results_Analysis/MSE_Engagement.png)|
|------|

Multiclass was likely to be better than binary, since for the domain purposes it must be computed an average value which is more consistent if the model
is able to catch more granular informations (hence, expanded the final range from {0,1} into {0, 0.33, 0.66, 1}).<br>
**NB:** To understand what is the model referred to, check the rows 'Synonymous' in the previous tables.

