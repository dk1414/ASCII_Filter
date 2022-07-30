# ASCII_Filter
Webcam filter that draws video to the screen using keyboard characters


[![ASCII Filter Demo](https://imgur.com/Fy4X7Kn.png)](https://www.youtube.com/watch?v=fN0fT94LBX4 "ASCII Filter Demo")


## Description

Main code to run is in the main.py file. The program uses pygame's camera module to get a video feed from the first webcam that it finds.
For each image, the program averages each pixel's color to find its brightness. Then each pixel is mapped to an ASCII character that fits that brightness.
The program can also decrease the resolution. This is done by using a box blur (When I wrote this algorithm I didn't actually know what a box blur was, so my implementaion is the naive version). 



### Installing

* Download zip file and unzip into directory of your choice
* Open the main.py file and run

### Executing program
* Make sure you have a webcam connected to your computer if one is not built-in
* This filter works best on low resolutions, so if possible change your resolution settings before hand
* Once you download all necessary files and run the viewer.py file, the main window should appear
* You should see your webcam image in ASCII form
* Click the buttons to change the resolution
