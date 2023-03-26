from tkinter import *
from PIL import ImageTk, Image
from AR import AR
import tkinter
import cv2
from Settings import slider_settings, dropdown_settings

ar = AR()


class GUI:
    def __init__(self):
        # TKINTER PARAMS
        self.window_geometry = "800x512"
        self.frame_width = 800
        self.frame_heigth = 512

        self.win = Tk()
        self.win.geometry(self.window_geometry)

        self.marker_id = 'Marker 1'
        self.augmentation_image_id = ''
        self.algorithm = 'None'
        self.operation = 'detection'

        # IMAGES
        self.marker = cv2.imread('MarkerIcons01.png')
        self.marker_to_match = cv2.imread('m1.jpg')
        self.aug_image = cv2.imread('MarkerIcons01.png')

        # DROPDOWN LISTS
        self.images_menu = ['Marker 1', 'Marker 2', 'Marker 3']
        self.augmentation_image_menu = ['Image 1', 'Image 2', 'Image 3']
        self.operation_menu = ['detection', 'matching']
        self.algorithms_menu = ['None', 'harris', 'shitomasi', 'sift', 'fast', 'orb']

        # MANAGEMENT DICTS
        self.dropdown_dict = dict()
        self.slider_dict = dict()
        self.params = dict()

        # COMMON PARAMS
        self.params["Features"] = 50
        # HARRIS CORNER DETECTION PARAMS
        self.params["Block Size"] = 2
        self.params["Kernel Size"] = 3
        self.params["K"] = 0.04
        # SHI-TOMASI PARAMS
        self.params["Quality Control"] = 0.02
        self.params["Min Distance"] = 20
        # SIFT PARAMS
        self.params["Contrast Threshold"] = 0.04
        self.params["Octave Layers"] = 3
        # FAST PARAMS
        self.params["Threshold"] = 10
        self.params["Non Max Suppression"] = 0
        # ORB PARAMS
        self.params["Scale Factor"] = 1.2
        self.params["Levels"] = 8
        self.params["Edge Threshold"] = 31

        self.init_config()
        self.update_image()

    def update_image(self):
        if self.operation == 'detection':
            image = ar.get_features(self.marker, algorithm=self.algorithm, params=self.params)[0]
            image = ImageTk.PhotoImage(Image.fromarray(cv2.resize(image, (512, 512))))
        elif self.operation == 'matching':
            image = ar.match_features(self.marker, self.marker_to_match, self.params)
            image = ImageTk.PhotoImage(Image.fromarray(image))

        label = Label(image=image)
        label.image = image
        label.place(relx=0, rely=0, anchor='nw')
        pass

    def dropdown_action(self, value, id):
        if id == 'markers_list':
            self.marker_id = value
        elif id == 'aug_image':
            self.augmentation_image_id = value
        elif id == 'operation':
            self.operation = value
        elif id == 'algorithm':
            self.algorithm = value

        self.update_environment()
        self.update_image()

    def slider_action(self, value, id):
        if type(self.params[id]) == float:
            self.params[id] = float(value)
        if type(self.params[id]) == int:
            self.params[id] = int(value)

        print(id, ' updated to: ', self.params[id])
        self.update_image()

    def update_environment(self):
        x = 512
        y = 10
        label_offset = 19

        if self.marker_id == 'Marker 1':
            self.marker = cv2.imread('MarkerIcons01.png')
            self.marker_to_match = cv2.imread('m1.jpg')
        elif self.marker_id == 'Marker 2':
            self.marker = cv2.imread('MarkerIcons02.png')
            self.marker_to_match = cv2.imread('m2.jpg')
        elif self.marker_id == 'Marker 3':
            self.marker = cv2.imread('MarkerIcons03.png')
            self.marker_to_match = cv2.imread('m2.jpg')

        if self.augmentation_image_id == 'Image 1':
            self.aug_image = cv2.imread('MarkerIcons01.png')
        if self.augmentation_image_id == 'Image 2':
            self.aug_image = cv2.imread('MarkerIcons02.png')
        if self.augmentation_image_id == 'Image 3':
            self.aug_image = cv2.imread('MarkerIcons03.png')

        if self.operation == 'detection':
            self.algorithms_menu = ['None', 'harris', 'shitomasi', 'sift', 'fast', 'orb']
        elif self.operation == 'matching':
            self.algorithms_menu = ['orb']

        if self.algorithm not in self.algorithms_menu:
            self.algorithm = self.algorithms_menu[0]
        self.dropdown_dict['algorithm'].destroy()
        self.dropdown_dict['algorithm'] = self.create_dropdown(dropdown_settings['algorithm'], self.algorithm,
                                                               self.algorithms_menu, 'algorithm')

        if self.algorithm == 'None':
            for i in self.slider_dict:
                self.slider_dict[i][0].destroy()
                self.slider_dict[i][1].destroy()
        else:
            for i in self.slider_dict:
                self.slider_dict[i][0].destroy()
                self.slider_dict[i][1].destroy()
            for i in slider_settings[self.algorithm].keys():
                self.slider_dict[i] = self.create_slider(slider_settings[self.algorithm][i])

    def init_config(self):
        self.dropdown_dict['markers_list'] = self.create_dropdown(dropdown_settings['markers_list'], 'Marker 1',
                                                                  self.images_menu, 'markers_list')
        self.dropdown_dict['aug_image'] = self.create_dropdown(dropdown_settings['aug_image'], 'Aug Image',
                                                               self.augmentation_image_menu, 'aug_image')
        self.dropdown_dict['operation'] = self.create_dropdown(dropdown_settings['operation'], 'detection',
                                                               self.operation_menu, 'operation')
        self.dropdown_dict['algorithm'] = self.create_dropdown(dropdown_settings['algorithm'], 'None',
                                                               self.algorithms_menu, 'algorithm')

    def create_dropdown(self, settings, init_val, menu, id):
        images_dropdown = StringVar()
        images_dropdown.set(init_val)
        drop1 = OptionMenu(self.win, images_dropdown, *menu,
                           command=lambda drop1, id=id: self.dropdown_action(drop1, id))
        drop1.place(x=settings['pos'][0], y=settings['pos'][1], in_=self.win, anchor='nw')
        drop1.configure(width=14)
        return drop1

    def create_slider(self, settings):
        s1 = Scale(self.win,
                   from_=settings['range'][0],
                   to=settings['range'][1],
                   tickinterval=settings['tick_interval'],
                   orient=HORIZONTAL,
                   command=lambda drop1, id=settings['label']: self.slider_action(drop1, id),
                   activebackground='red',
                   length=200,
                   resolution=settings['resolution'])
        s1.place(x=settings['pos'][0], y=settings['pos'][1], in_=self.win, anchor='nw')
        s1_text = tkinter.Label(self.win, text=settings['label'])
        s1_text.place(x=settings['label_pos'][0], y=settings['label_pos'][1], anchor='ne')
        return [s1, s1_text]

    def run(self):
        self.win.mainloop()


__name__ = "__main__"

GUI().run()
