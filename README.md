# Garage Alarm
A Raspberry Pi IoT project to alert me if I left the garage door open.

### Overview
This app is designed to detect when I have left my garage door open and, if detected, alert me.  It runs on a [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) - though a 2B might also work - with the [camera module v2](https://www.raspberrypi.org/products/camera-module-v2/).  It uses [Pillow](https://python-pillow.org/) for image processing, [numpy](http://www.numpy.org/) for image analysis, and [scikit-learn](http://scikit-learn.org/stable/) for classifying images.  Alerting is handled using [IFTTT](https://ifttt.com) applets.

As you explore this project, it will at some point occur to you that there is nothing specific in the code for detecting garage doors being open or closed, per se.  You're correct.  The classifier is trained on one set of images that meet some condition (positive samples), and another set that don't (negative samples).  With no code changes, this same project could be used to detect the presence, or absence, of a package on your doorstep, a bird in a nest, clouds in the sky, or countless other scenarios.

### Installation and Configuration

#### Raspberry Pi
1. Assemble the Pi with the camera, and be sure you can `SSH` to it and/or access it via a remote desktop or terminal client.
2. `git clone` this repository to a directory on the Pi.
3. Run `pip install -r requirements.txt` to install the dependencies.

#### IFTTT
The Pi sends alerts by POSTing to a specified URL.  While this could be any URL you choose, of course, I set mine up to trigger IFTTT applets using the [Maker channel](https://internal-api.ifttt.com/maker).  Follow [these instructions](http://www.makeuseof.com/tag/ifttt-connect-anything-maker-channel/) (or similar) to create an applet trigger.  Make a note of the trigger URL:

`https://maker.ifttt.com/trigger/{event}/with/key/{key}`

The `event` name is yours to choose, but the name you use will need to match in the `config.py` file and any IFTTT applets you create.  The `key` value is created when you connect the Maker IFTTT channel.

Finally, use IFTTT to create applet(s) that respond to your Maker trigger.  I have two set up: one sends me an SMS message, and the other changes the color of one of my [Philips Hue](http://meethue.com) smarthome lights.  Again, the event name you use in your applet trigger will need to match what you specify in the `config.py` file.

#### Config.py
Here's what the various settings in `config.py` are for.
- `ALERT_URL` should match the URL specified in the Maker IFTTT channel, with placeholders for the `event` and `key` values.  You shouldn't need to change this.
- The `ALERT_NAME` must match the event name you chose when you set up your IFTTT applet(s).
- The `ALERT_KEY` is the key provided by the [Maker IFTTT channel](https://internal-api.ifttt.com/maker).
- `INSTALL_DIR` is the absolute path on your Pi to the project root directory where you cloned this repository.
- The remaining `_DIR` directories are relative to the `INSTALL_DIR` and should not need to be changed.  They hold the image files created in the process of training and running the app.  After training (see below), these directories can be safely emptied at any time.
- `MODEL_FILE_NAME` should not need to be changed unless you would like to train multiple models (see Training below).
- `MIN_` and `MAX_` settings represent bounds on how the app will try to achieve the best brightness of captured images in order to have the best chance of correctly analyzing each image.  If the app is having trouble classifying some images, and you suspect it's becuase some images are turning out too bright or dark, try adjusting `BRIGHTNESS` accordingly.  The acceptible value range is 0-255.  The `SHUTTER_SPEED` values should not exceed the minimum and maximum values specified in the camera documentation.
- `SHUTTER_SPEED_STEP` specifies how much the shutter speed changes with each trial image as the app tries to find the best camera settings to achieve acceptable brightness.  It should not need to be changed.

### Training
Before this app can alert on an open garage door, it needs to be trained what open and closed garage doors look like.

#### Taking Samples
Use `samples.py` to capture images that represent positive (garage door open) and negative (garage door closed) examples, as follows:

`$ python ./samples.py --positive`

`$ python ./samples.py --negative`

Sample images will be stored in the corresponding directories specified in the `config.py` file.  Be sure to capture samples with various combinations of objects and brightness in the image.  For a garage door alarm, for example, take samples with a car present and absent, with overhead lights on and off, and during daylight and at night.

How many samples are enough?  That depends on many factors, and may require some trial-and-error.  My garage alarm works well with about two dozen samples each (positive and negative).  More samples will generally lead to better performance, but the size of the resulting `model.pkl` file may become a limiting factor.

#### Training the Model
After capturing your samples, train your model as follows:

`$ python ./models.py`

Depending on the number of samples, training may take several minutes.  The training process produces a `model.pkl` file (or whatever file name is specified in `config.py`) which the app will use to classify new trial images as either positive or negative.

For those with an interest in machine learning, this app trains a [Support Vector Machine (SVM)](https://en.wikipedia.org/wiki/Support_vector_machine) classifier with a linear kernel function.  If you'd like to experiment with different types of classifiers or classifier parameters, you'll find that code in the `models.py` file.  Refer to the [scikit-learn](http://scikit-learn.org/stable/) documentation for available options. 

### Logging
The app logs its activities to an `app.log` file in the project root directory.

### Running on a Schedule
`cron` is an easy way to run the app on a regular schedule.  For this purpose, I have provided the `setcron.sh` script, but `cron` jobs can be created manually quite easily.

### License and Contributions
Use of this code is governed by the MIT license.  This app is a work in progress, and it may fail for any number of reasons, causing your house to catch fire or, worse, your cat to go bald.  I welcome pull requests that improve performance and/or help prevent such disasters.
