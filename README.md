# Augmented Reality Visualizer

This project demonstrates the different steps involved in augmented reality i.e. Feature Detection, Matching and Image Augmentation. This project deals with Marker Based AR which uses a very distinguishable marker to augment an image into a frame. This app allows you to try different algorithms and change their parameters to see how they affect each step of Augmented Reality

## Description

The project has 4 dropdowns. The first is to choose a marker. The second is to choose the image you want to augment. The third is the operation i.e. feature detection, matching or image augmentation. The fourth is the algorithm for the selected operation.

The three steps of Marker Based AR:
* **Feature Detection:** Extract unique features of a marker from the source image(Unedited image of marker) and the target image(current camera frame). Harris Corner Detection, Shi-Tomasi, SIFT, ORB and FAST are the algorithms demonstrated

* **Feature Matching:** Match the extracted features between the source and target image and calculate the transformation between the two images. Only ORB is used for Feature Matching.

* **Image Augmentation:** Apply the obtained transformation to the Image that is to be augmented and place it on the target image(frame)

## Getting Started

### Dependencies

* opencv-contrib-python 4.5.5.62
* tkinter
* pillow 9.4.0
* threading

### Installing

* Install the mentioned libraries. Use **opencv-contrib-python** to use SIFT. SIFT is unavailable in opencv-python 

### Executing program

```
Run the GUI.py File
```

## Version History

* 0.1
    * Initial Release. 
    * Contains only ORB for Matching and Augmentation