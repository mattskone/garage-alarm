# Garage Alarm
A Raspberry Pi IoT project to alert me if I left the garage door open.

### Overview
This app is designed to detect when I have left my garage door open and, if detected, alert me.  It runs on a [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) - though a 2B might also work - with the [camera module v2](https://www.raspberrypi.org/products/camera-module-v2/).  It uses [Pillow](https://python-pillow.org/) for image processing, [numpy](http://www.numpy.org/) for image analysis, and [scikit-learn](http://scikit-learn.org/stable/) for classifying images.  Alerting is handled using [IFTTT](https://ifttt.com) applets.

As you explore this project, it will at some point occur to you that there is nothing specific in the code for detecting garage doors being open or closed, per se.  You're correct.  The classifier is trained on one set of images that meet some condition (positive samples), and another set that don't (negative samples).  With no code changes, this same project could be used to detect the presence, or absence, of a package on your doorstep, a bird in a nest, clouds in the sky, or countless other scenarios.

### Installation and Configuration

#### Raspberry Pi

#### Config.py

#### IFTTT

### Training

#### Taking Samples

#### Training the Model

### Running on a Schedule

### License and Contributions
