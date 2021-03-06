import time
import tkinter as tk
import warnings
from ast import literal_eval
from tkinter import ttk, filedialog, messagebox

import cv2
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Supports.FER.Auxiliary_FER import runner

warnings.simplefilter("ignore")
np.seterr(divide='ignore', invalid='ignore')


def browse_button():
    filename = filedialog.askopenfile()
    if filename is None:
        video.set(None)
    else:
        video.set(filename.name)
    return


def ask_dir():
    directory = filedialog.askdirectory()
    destination.set(directory)
    return


def start_analysis():
    if video.get() is '' or video.get() == 'None' or destination.get() is '':
        messagebox.showerror(title="Error", message="Specify an input and/or a destination")
    else:
        runner(path_video=video.get(), percentage=int(spinbox.get()), path_result=destination.get())
        messagebox.showinfo(title="Analysis completed",
                            message="Now you can show what has been created pressing 'Show Result' button on the main page or browsing the folder that you specified before.\nThank you!")
    return


def change_image(label_for_image, list_images, list_locations, cont, last, d):
    cont2 = cont
    if cont2 == 0:
        time.sleep(4)
    # print("Immagine letta:\t\t" + (list_images[ciao])[0])
    img = cv2.imread((list_images[cont2])[0])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = cv2.rectangle(img, ((list_locations[cont2])[1], (list_locations[cont2])[0]),
                        ((list_locations[cont2])[3], (list_locations[cont2])[2]),
                        (0, 0, 255), 5)
    img = ImageTk.PhotoImage(Image.fromarray(img).resize((500, 250)))
    label_for_image.config(image=img)
    label_for_image.image = img
    cont2 = cont
    cont2 = cont2 + 1
    if cont2 < last:
        label_for_image.after(d,
                              lambda: change_image(label_for_image, list_images, list_locations, cont2, last, d))
    else:
        return


def show_result():
    result_window = tk.Toplevel(main_window)
    result_window.title('Result Window')
    c = 0
    # --------------------------------------------------------------------------------------
    # --                                  read data from csv                              --
    # --------------------------------------------------------------------------------------
    df = pd.read_csv(
        destination.get() + "/" + "report_experiment.csv",
        delimiter=',',
        header=0)
    data = df.values
    num_cycles = np.shape(data)[0]
    # print("Num:\t" + str(num_cycles))
    images = data[:, 1:2]
    locations = data[:, 2:3]
    #  --------------------------------------------------------------------------------------
    loc = []
    for i in range(num_cycles):
        loc.append(literal_eval(locations[i][0]))
    #  --------------------------------------------------------------------------------------
    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
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

    fig, ax = plt.subplots(1, 1, figsize=(18, 6), dpi=100)
    plt.setp(ax, xticks=np.arange(0, num_cycles + 1, step_x).tolist(),
             yticks=np.arange(-0.1, 1.1, 0.1).tolist())
    plt.grid()
    ax.set_xlim(0, num_cycles + 1)
    ax.set_ylim(-0.1, 1.1)
    plt.tight_layout(1.0)
    frames_ax = np.arange(1, num_cycles + 1, 1)

    d = dict()
    for i in range(num_emotions):
        line_emotion, = ax.plot(0, 0, color=color_list[i], label=emotions[i], linewidth=line_tick)
        d[emotions[i]] = [[], [], line_emotion, data[:, i + 3:i + 4]]

    def animation_frame1(i):
        list_lines = []
        # -------
        for key, value in d.items():
            value[0].append(frames_ax[i])
            value[1].append((value[3])[i])
            value[2].set_xdata(value[0])
            value[2].set_ydata(value[1])
            list_lines.append(value[2])
        return list_lines,

    #  --------------------------------------------------------------------------------------

    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width * 0.8, chartBox.height])
    ax.legend(loc='upper center', bbox_to_anchor=(1.1, 0.6), shadow=True, ncol=1)

    result_window.after(200, result_window.update())
    canvas1 = FigureCanvasTkAgg(fig, master=result_window)
    canvas1.get_tk_widget().grid(column=0, row=2)
    animation1 = anim.FuncAnimation(fig, func=animation_frame1, frames=np.arange(0, num_cycles, 1),
                                    interval=10,
                                    repeat=False)

    img = cv2.imread((images[1])[0])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.rectangle(img, ((loc[0])[1], (loc[0])[0]), ((loc[0])[3], (loc[0])[2]),
                        (0, 0, 255), 5)
    starter = ImageTk.PhotoImage(Image.fromarray(img).resize((500, 250)))
    image2show = tk.Label(result_window, image=starter)
    image2show.grid(column=0, row=0)
    image2show.after(10, lambda: change_image(image2show, images, loc, c, num_cycles, 10))
    result_window.attributes("-fullscreen", True)
    result_window.mainloop()


main_window = tk.Tk()
main_window.title(string="Intelligent Interfaces - A.A. 2019/20 - FER on Video - Federico Impellizzeri")
video = tk.StringVar()
video.set('')
destination = tk.StringVar()
destination.set('')
# -----------------
menu = tk.Menu(main_window)
main_window.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label='Menu', menu=filemenu)
filemenu.add_command(label='About')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=main_window.quit)
# -----------------
label_video = ttk.Label(main_window, text="Choose a video", anchor='center')
label_video.pack(fill='x')
# -----------------
load_video = ttk.Button(main_window, text="Load a video", command=browse_button, state='active')
load_video.place()
load_video.pack(fill='x')
# -----------------
name_video = ttk.Label(main_window, anchor='center', textvariable=video)
name_video.pack(fill='x')
# -----------------
label_destination = ttk.Label(main_window, text="Choose a folder to save results", anchor='center')
label_destination.pack(fill='x')
# -----------------
load_video = ttk.Button(main_window, text="Choose a directory", command=ask_dir, state='active')
load_video.place()
load_video.pack(side='top', fill='x')
# -----------------
name_dir = ttk.Label(main_window, anchor='center', textvariable=destination)
name_dir.pack(fill='x')

# -----------------
label_spinbox = ttk.Label(main_window, text="Choose sampling frequency (in seconds)", anchor='center')
label_spinbox.pack(fill='x')
# -----------------
spinbox = tk.Spinbox(main_window, from_=1, to=60, justify='right')
spinbox.pack(fill='x')
# -----------------

separator = tk.Frame(height=2, bd=1, relief='sunken')
separator.pack(fill='x', padx=5, pady=5)
# -----------------
go = ttk.Button(main_window, text="Perform Analysis", command=start_analysis, state='active')
go.place()
go.pack(fill='x')
output = ttk.Button(main_window, text="Show Results", command=show_result,
                    state='active')
output.place()
output.pack(fill='x')
# -----------------
main_window.minsize(300, 150)
main_window.resizable(False, False)
main_window.lift()
main_window.mainloop()
