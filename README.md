# Augmented Reality Visualizer

This project demonstrates the different steps involved in augmented reality i.e. Feature Detection, Matching and Image Augmentation. This project deals with Marker Based AR which uses a very distinguishable marker to augment an image into a frame. This app allows you to try different algorithms and change their parameters to see how they affect each step of Augmented Reality

## Description

The project has 4 dropdowns. The first is to choose a marker. The second is to choose the image you want to augment. The third is the operation i.e. feature detection, matching or image augmentation. The fourth is the algorithm for the selected operation.
<br/>
![1](https://user-images.githubusercontent.com/86465783/229004425-c8ecf699-a768-4e0a-bf25-553902e6cc6b.jpg)
![2](https://user-images.githubusercontent.com/86465783/229004452-24fb2863-86fc-4e67-8b87-200ace038990.jpg)
<br/>
The three steps of Marker Based AR:
<br/>
* **Feature Detection:** Extract unique features of a marker from the source image(Unedited image of marker) and the target image(current camera frame). Harris Corner Detection, Shi-Tomasi, SIFT, ORB and FAST are the algorithms demonstrated
<br/>

![3](https://user-images.githubusercontent.com/86465783/229004460-7ad97047-1b36-4a44-8723-f594a455edc4.png)

<br/>
* **Feature Matching:** Match the extracted features between the source and target image and calculate the transformation between the two images. Only ORB is used for Feature Matching.
<br/>

![4](https://user-images.githubusercontent.com/86465783/229004473-ebe8d38f-0f65-4e45-ac70-eff8fe9ad932.png)

<br/>
* **Image Augmentation:** Apply the obtained transformation to the Image that is to be augmented and place it on the target image(frame)
<br/>

![5](https://user-images.githubusercontent.com/86465783/229004482-b99cd617-a850-4126-9ad4-ef29e9526602.png)

<br/>
## Live Video
<br/>

https://user-images.githubusercontent.com/86465783/229006071-695fb4a7-5c89-456e-b7e5-04382c2d84fb.mp4

<br/>

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
