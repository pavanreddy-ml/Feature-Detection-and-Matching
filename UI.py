from tkinter import *
from PIL import ImageTk, Image
from AR import AR
import tkinter
import cv2

ar = AR()
image = cv2.imread('MarkerIcons01.png')
image2 = cv2.imread('m1.jpg')

# PARAMS
N_FEATURES = 50

def update_n_features(x):
    global N_FEATURES
    N_FEATURES = int(x)

    update_image()
    print(N_FEATURES)


def update_image():
    global image, algorithm, operation, image, algorithm, operation, image_id, image2, algorithms_menu, N_FEATURES

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
        image = ar.get_features(image, algorithm=algorithm, n=N_FEATURES)[0]
    elif operation == 'matching':
        image = ar.match_features(image, image2, det_algorithm=algorithm, n=N_FEATURES)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = ImageTk.PhotoImage(image=Image.fromarray(image))

    label.configure(image=image)
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

s1 = Scale(win, from_=0, to=1000, tickinterval=500, orient=HORIZONTAL, command=update_n_features)
s1.place(x=512+128, y=100, in_=win)





win.mainloop()