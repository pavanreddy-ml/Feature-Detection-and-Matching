from tkinter import *
from PIL import ImageTk, Image
from AR import AR
import tkinter
import cv2

ar = AR()
image = cv2.imread('MarkerIcons01.png')
image2 = cv2.imread('m1.jpg')

slider_list = []

# PARAMS
N_FEATURES = 50
BLOCK_SIZE = 2
K_SIZE = 3
K = 0.04
QUALITY_LEVEL = 0.02
MIN_DISTANCE = 20

def update_n_features(x):
    global N_FEATURES
    N_FEATURES = int(x)

    update_image(sliders_reset=False)
    print(N_FEATURES)

def update_block_size(x):
    global BLOCK_SIZE
    BLOCK_SIZE = int(x)

    update_image(sliders_reset=False)
    print(BLOCK_SIZE)

def update_k_size(x):
    global K_SIZE
    K_SIZE = int(x)

    update_image(sliders_reset=False)
    print(K_SIZE)

def update_k(x):
    global K
    K = float(x)

    update_image(sliders_reset=False)
    print(K)

def update_quality_level(x):
    global QUALITY_LEVEL
    QUALITY_LEVEL = float(x)

    update_image(sliders_reset=False)
    print(QUALITY_LEVEL)

def update_min_distance(x):
    global MIN_DISTANCE
    MIN_DISTANCE = int(x)

    update_image(sliders_reset=False)
    print(MIN_DISTANCE)


def update_image(sliders_reset=True):
    global image, algorithm, operation, image, algorithm, operation, image_id, image2, algorithms_menu, N_FEATURES, \
        slider_list, win, label, BLOCK_SIZE, K_SIZE, QUALITY_LEVEL, MIN_DISTANCE, K, s1, s2, s3, s4

    if image_id == 'Marker 1':
        image = cv2.imread('MarkerIcons01.png')
        image2 = cv2.imread('m1.jpg')
    if image_id == 'Marker 2':
        image = cv2.imread('MarkerIcons02.png')
        image2 = cv2.imread('m2.jpg')
    if image_id == 'Marker 3':
        image = cv2.imread('MarkerIcons03.png')
        image2 = cv2.imread('m3.jpg')

    if operation == 'detection':
        if algorithm == 'None':
            for slider in slider_list:
                slider.destroy()
        elif algorithm == 'harris':
            if sliders_reset:
                for slider in slider_list:
                    if slider == 's1':
                        s1.destroy()
                    if slider == 's2':
                        s2.destroy()
                    if slider == 's3':
                        s3.destroy()
                slider_list = []

                s1 = Scale(win, from_=1, to=20, tickinterval=5, orient=HORIZONTAL, command=update_block_size)
                s1.place(x=512 + 128, y=100, in_=win)
                s1_text = tkinter.Label(win, text='Block Size', anchor='nw')
                s1_text.place(x = 512+80, y=100)
                slider_list.append("s1")

                s2 = Scale(win, from_=1, to=10, tickinterval=5, orient=HORIZONTAL, command=update_k_size)
                s2.place(x=512 + 128, y=150, in_=win)
                s2_text = tkinter.Label(win, text='K Size')
                s2_text.place(x=512 + 80, y=150)
                slider_list.append("s2")

                s3 = Scale(win, from_=0.01, to=2, tickinterval=0.5, orient=HORIZONTAL, resolution=0.01, command=update_k)
                s3.place(x=512 + 128, y=200, in_=win)
                s3_text = tkinter.Label(win, text='K')
                s3_text.place(x=512 + 80, y=200)
                slider_list.append("s3")
        elif algorithm == 'shitomasi':
            if sliders_reset:
                for slider in slider_list:
                    if slider == 's1':
                        s1.destroy()
                    if slider == 's2':
                        s2.destroy()
                    if slider == 's3':
                        s3.destroy()
                slider_list = []

                s1 = Scale(win, from_=1, to=500, tickinterval=250, orient=HORIZONTAL, command=update_n_features)
                s1.place(x=512 + 128, y=100, in_=win)
                s1_text = tkinter.Label(win, text='Features', anchor='nw')
                s1_text.place(x = 512+80, y=100)
                slider_list.append("s1")

                s2 = Scale(win, from_=0, to=1, tickinterval=5, orient=HORIZONTAL, resolution=0.01, command=update_quality_level)
                s2.place(x=512 + 128, y=150, in_=win)
                s2_text = tkinter.Label(win, text='Quality Control')
                s2_text.place(x=512 + 80, y=150)
                slider_list.append("s2")

                s3 = Scale(win, from_=10, to=50, tickinterval=10, orient=HORIZONTAL, command=update_min_distance)
                s3.place(x=512 + 128, y=200, in_=win)
                s3_text = tkinter.Label(win, text='Min Distance')
                s3_text.place(x=512 + 80, y=200)
                slider_list.append("s3")

        elif algorithm == 'sift':
            if sliders_reset:
                for slider in slider_list:
                    if slider == 's1':
                        s1.destroy()
                    if slider == 's2':
                        s2.destroy()
                    if slider == 's3':
                        s3.destroy()
                slider_list = []

                s1 = Scale(win, from_=1, to=5000, tickinterval=2500, orient=HORIZONTAL, command=update_n_features)
                s1.place(x=512 + 128, y=100, in_=win)
                s1_text = tkinter.Label(win, text='Features', anchor='nw')
                s1_text.place(x = 512+80, y=100)
                slider_list.append("s1")




        image = ar.get_features(image, algorithm=algorithm, n=N_FEATURES, blockSize=BLOCK_SIZE, ksize=K_SIZE, k=K,
                                qualityLevel=QUALITY_LEVEL, minDistance=MIN_DISTANCE)[0]
    elif operation == 'matching':
        image = ar.match_features(image, image2, det_algorithm=algorithm, n=N_FEATURES)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = ImageTk.PhotoImage(image=Image.fromarray(image))

    label.configure(image=image)
    # if operation == 'detection':
    #     # label.configure(x=128)
    #     label.place(x=128, y=0)
    # elif operation == 'matching':
    #     label.configure(x=128)
    label.image = image


def change_operation(x):
    global image, algorithm, operation, image, algorithm, operation, image_id, image2, algorithms_menu, drop3
    operation = x
    if operation == 'detection':
        algorithms_menu = ['None', 'harris', 'shitomasi', 'sift', 'surf', 'fast', 'orb']
        algorithm = 'None'
        drop3.destroy()
        drop3 = OptionMenu(win, algorithms_dropdown, *algorithms_menu, command=change_algorithm)
        drop3.place(x=512 + 128, y=70, in_=win)
    elif operation == 'matching':
        algorithms_menu = ['orb']
        algorithm = 'orb'
        algorithms_dropdown.set(algorithm)
        drop3.destroy()
        drop3 = OptionMenu(win, algorithms_dropdown, *algorithms_menu, command=change_algorithm)
        drop3.place(x=512 + 128, y=70, in_=win)

    update_image()

    print(operation)

def change_algorithm(x):
    global image, algorithm, operation, image_id, image2
    algorithm = x

    update_image()

    print(algorithm)

def change_image(x):
    global image, image2, algorithm, operation, image_id
    image_id = x

    update_image()

    print(image_id)


win = Tk()
win.geometry("768x256")

image_id = 'Marker 1'
images_menu = ['Marker 1', 'Marker 2', 'Marker 3']
operation_menu = ['detection', 'matching']
algorithms_menu = ['None', 'harris', 'shitomasi', 'sift', 'fast', 'orb']

operation = 'detection'
algorithm = 'harris'

frame = Frame(win, width=768, height=256)
frame.pack()

images_dropdown = StringVar()
images_dropdown.set("Marker 1")
drop1 = OptionMenu(win, images_dropdown, *images_menu, command=change_image)
drop1.place(x=512+128, y=10, in_=win)

operation_dropdown = StringVar()
operation_dropdown.set("detection")
drop2 = OptionMenu(win, operation_dropdown, *operation_menu, command=change_operation)
drop2.place(x=512+128, y=40, in_=win)

algorithms_dropdown = StringVar()
algorithms_dropdown.set("None")
drop3 = OptionMenu(win, algorithms_dropdown, *algorithms_menu, command=change_algorithm)
drop3.place(x=512+128, y=70, in_=win)

frame.place(anchor='nw', relx=0, rely=0)
img = ImageTk.PhotoImage(Image.open("MarkerIcons01.png"))
label = Label(frame, image=img)
label.pack()


win.mainloop()