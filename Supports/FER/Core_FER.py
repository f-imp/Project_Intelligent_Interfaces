import warnings
from sys import platform as sys_pf

import cv2
import numpy as np
import pandas as pd

if sys_pf == 'darwin':
    import matplotlib

    matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

warnings.simplefilter("ignore")
np.seterr(divide='ignore', invalid='ignore')


def report_experiment(emotions):
    d = dict()
    d["path_frame"] = []
    d["position_face"] = []
    for e in emotions:
        d[e] = []
    d['high_emotion'] = []
    return d

def set_fps(format_video, video):
    fps = 0
    if format_video == "MP4" or format_video == "mp4" or format_video == "avi":
        fps = int(video.get(cv2.CAP_PROP_FPS))
    elif format_video == "wmv":
        fps = 15
    elif format_video == "webm":
        fps = 30
    else:
        fps = 25
    return fps

def report_details(name_video, fps, sampling, emotions):
    info = dict()
    info["video_path"] = name_video
    info["fps"] = fps
    info["Sampling_frequency"] = sampling
    for e in emotions:
        info[e] = 0
        info[e + "_max"] = 0.0
        info[e + "_min"] = 0.0
        info[e + "_avg"] = 0.0
        info[e + "_std_dev"] = 0.0
        info[e + "_pearson"] = 0.0
    info['Positive'] = 0
    info['Negative'] = 0
    return info


def create_hist(emotions, values, hp):
    # x-coordinates of left sides of bars
    fig, ax = plt.subplots(1)

    c = []
    for v in values:
        if v >= 0.00:
            c.append('green')
        else:
            c.append('red')
    left = [x + 1 for x in range(len(emotions))]
    # plotting a bar chart

    ax.bar(left, values, tick_label=emotions,
           width=0.8, color=c)

    for i, v in enumerate(values):
        if v < 0.0:
            ax.text(i + 0.8,
                    v - 0.06,
                    v,
                    fontsize=8,
                    fontweight='bold',
                    color='black')
        else:
            ax.text(i + 0.8,
                    v + 0.01,
                    v,
                    fontsize=8,
                    fontweight='bold',
                    color='black')
    plt.margins(0.05, 0.1)
    # naming the x-axis
    plt.xlabel('Emotions')
    # naming the y-axis
    plt.ylabel('Pearson Values')
    plt.yticks(np.arange(-1.0, 1.1, 0.2))
    # plot title
    plt.title('Pearson correlation of emotions over time')
    plt.savefig(hp + "/" + "histogram.png")
    return


def create_timeline(path_file, emotions, path_result):
    df = pd.read_csv(path_file, delimiter=',', header=0)
    data = df.values
    num_cycles = np.shape(data)[0]
    num_emotions = len(emotions)
    color_list = ['red', 'orangered', 'darkorange', 'limegreen', 'darkgreen', 'royalblue', 'navy']

    line_tick = 2.5
    step_x = 1
    threshold_step = 40

    while (num_cycles / step_x) > threshold_step:
        step_x += 1
        if 2 <= step_x <= 4:
            line_tick = 1.5
        elif step_x >= 5:
            line_tick = 1

    fig_2save, ax_2save = plt.subplots(1, 1, figsize=(18, 6), dpi=100)
    plt.setp(ax_2save, xticks=np.arange(0, num_cycles + step_x, step_x).tolist(),
             yticks=np.arange(-0.1, 1.1, 0.1).tolist())
    plt.grid()
    ax_2save.set_xlim(0, num_cycles + 1)
    ax_2save.set_ylim(-0.1, 1.1)
    plt.tight_layout(1.0)
    frames_ax_2save = np.arange(1, num_cycles + 1, 1)

    for i in range(num_emotions):
        line_to_track = ax_2save.plot(frames_ax_2save, data[:, i + 3:i + 4], color=color_list[i],
                                      label=emotions[i],
                                      linewidth=line_tick)

    chartBox2 = ax_2save.get_position()
    ax_2save.set_position([chartBox2.x0, chartBox2.y0, chartBox2.width * 0.8, chartBox2.height])
    ax_2save.legend(loc='upper center', bbox_to_anchor=(1.1, 0.6), shadow=True, ncol=1)
    fig_2save.savefig(path_result + "/timeline_emotion.png")
    return
