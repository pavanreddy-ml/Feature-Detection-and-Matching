from tkinter import *
from PIL import ImageTk, Image
from AR import AR
import tkinter
import cv2


ar = AR()
image = cv2.imread('MarkerIcons01.png')
image2 = cv2.imread('m1.jpg')


class GUI():
    def __init__(self):
        # TKINTER PARAMS
        self.window_geometry = "800x512"
        self.frame_width = 800
        self.frame_heigth = 512

        self.win = Tk()
        self.win.geometry(self.window_geometry)


        self.marker_id = 'Marker 1'
        self.augmentation_image_id = ''
        self.algorithm = 'orb'
        self.operation = 'matching'

        # DROPDOWN LISTS
        self.images_menu = ['Marker 1', 'Marker 2', 'Marker 3']
        self.augmentation_image_menu = ['Image 1', 'Image 2', 'Image 3']
        self.operation_menu = ['detection', 'matching']
        self.algorithms_menu = ['None', 'harris', 'shitomasi', 'sift', 'fast', 'orb']

        #MANAGEMENT DICTS
        self.dropdown_dict = dict()
        self.slider_dict = dict()

        # COMMON PARAMS
        self.n_features = 50
        self.suppression = 0
        # HARRIS CORNER DETECTION PARAMS
        self.block_size = 2
        self.k_size = 3
        self.k = 0.04
        # SHI-TOMASI PARAMS
        self.quality_level = 0.02
        self.min_distance = 20


        self.init_config()
        self.update_image()

    def update_image(self):
        global image, image2
        image = ar.match_features(image, image2, det_algorithm=self.algorithm, n=self.n_features)
        image = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.frame.place(anchor='nw', relx=0, rely=0)
        label = Label(self.frame, image=image)
        label.pack()


    def dropdown_action(self, value, id):
        if id == 'markers_list':
            self.marker_id = value
        elif id == 'aug_image':
            self.augmentation_image_id = value
        elif id == 'operation':
            self.operation = value
        elif id == 'algorithm':
            self.algorithm = value

        print(self.marker_id, self.augmentation_image_id, self.operation, self.algorithm)
        self.update_environment()
        # self.update_image()




    def update_environment(self):
        pass









    def init_config(self):
        self.frame = Frame(self.win, width=self.frame_width, height=self.frame_heigth)
        self.frame.pack()

        x = 512
        y = 10
        label_offset = 19

        self.dropdown_dict['markers_list'] = self.create_dropdown((x+10, y), 'Marker 1', self.images_menu, 'markers_list')
        self.dropdown_dict['aug_image'] = self.create_dropdown((x+150, y), 'Aug Image', self.augmentation_image_menu, 'aug_image')
        self.dropdown_dict['operation'] = self.create_dropdown((x+10, y+40), 'Detection', self.operation_menu, 'operation')
        self.dropdown_dict['algorithm'] = self.create_dropdown((x+150, y+40), 'None',
                                                               self.algorithms_menu, 'algorithm')


        self.slider_dict['s1'] = self.create_slider((10, 20), (x+75, y+80), 5, None, "Features", (x+65, y+label_offset+80), 0.5)
        self.slider_dict['s2'] = self.create_slider((10, 20), (x + 75, y + 120), 5, None, "K",
                                                    (x + 65, y + label_offset + 120), 0.5)
        self.slider_dict['s3'] = self.create_slider((10, 20), (x + 75, y + 160), 5, None, "K",
                                                    (x + 65, y + label_offset + 160), 0.5)


    def create_dropdown(self, pos, init_val, menu, id):
        images_dropdown = StringVar()
        images_dropdown.set(init_val)
        drop1 = OptionMenu(self.win, images_dropdown, *menu, command=lambda drop1, id=id:self.dropdown_action(drop1, id))
        drop1.place(x=pos[0], y=pos[1], in_=self.win, anchor='nw')
        drop1.configure(width=14)
        return drop1

    def create_slider(self, slider_range, pos, tick_interval, command, label, label_pos, resolution):
        s1 = Scale(self.win, from_=slider_range[0], to=slider_range[1], tickinterval=tick_interval, orient=HORIZONTAL,
                   command=command, activebackground='red', length=200, resolution=resolution)
        s1.place(x=pos[0], y=pos[1], in_=self.win, anchor='nw')
        s1_text = tkinter.Label(self.win, text=label)
        s1_text.place(x=label_pos[0], y=label_pos[1], anchor='ne')
        return s1

    def run(self):
        self.win.mainloop()


__name__ = "__main__"

GUI().run()