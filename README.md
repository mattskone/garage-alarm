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

### Training

#### Taking Samples

#### Training the Model

### Running on a Schedule

### License and Contributions
