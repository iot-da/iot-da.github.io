# Understanding Source Code

## Source Code

For reference, below is the source code to [`detectnet.py`](https://github.com/dusty-nv/jetson-inference/blob/master/python/examples/detectnet.py):

``` python
import jetson.inference
import jetson.utils

import argparse
import sys

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# process frames until the user exits
while True:
	# capture the next image
	img = input.Capture()

	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)

	# print the detections
	print("detected {:d} objects in image".format(len(detections)))

	for detection in detections:
		print(detection)

	# render the image
	output.Render(img)

	# update the title bar
	output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

	# print out performance info
	net.PrintProfilerTimes()

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break
```

# Coding Your Own Object Detection Program

In this step of the tutorial, we'll walk through the creation of the previous example for realtime object detection on a live camera feed in only 10 lines of Python code.  The program will load the detection network with the [`detectNet`](https://rawgit.com/dusty-nv/jetson-inference/dev/docs/html/python/jetson.inference.html#detectNet) object, capture video frames and process them, and then render the detected objects to the display.

For your convenience and reference, the completed source is available in the [`python/examples/my-detection.py`](https://github.com/dusty-nv/jetson-inference/blob/master/python/examples/my-detection.py) file of the repo, but the guide below will act like they reside in the user's home directory or in an arbitrary directory of your choosing.  

Here's a quick preview of the Python code we'll be walking through:

``` python
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
```

There's also a video screencast of this coding tutorial available on YouTube:

<a href="https://www.youtube.com/watch?v=obt60r8ZeB0&list=PL5B692fm6--uQRRDTPsJDp4o0xbzkoyf8&index=12" target="_blank"><img src=https://github.com/dusty-nv/jetson-inference/raw/master/docs/images/thumbnail_detectnet.jpg width="750"></a>
## Source Code

### Importing Modules

At the top of the source file, we'll import the Python modules that we're going to use in the script.  Add `import` statements to load the [`jetson.inference`](https://rawgit.com/dusty-nv/jetson-inference/python/docs/html/python/jetson.inference.html) and [`jetson.utils`](https://rawgit.com/dusty-nv/jetson-inference/python/docs/html/python/jetson.utils.html) modules used for object detection and camera capture.

``` python
import jetson.inference
import jetson.utils
```
### Loading the Detection Model

Next use the following line to create a [`detectNet`](https://rawgit.com/dusty-nv/jetson-inference/python/docs/html/python/jetson.inference.html#detectNet) object instance that loads the [91-class](../data/networks/ssd_coco_labels.txt) SSD-Mobilenet-v2 model:

``` python
# load the object detection model
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
```

Note that you can change the model string to one of the values from [this table](detectnet-console-2.md#pre-trained-detection-models-available) to load a different detection model.  We also set the detection threshold here to the default of `0.5` for illustrative purposes - you can tweak it later if needed.

### Opening the Camera Stream

To connect to the camera device for streaming, we'll create an instance of the [`videoSource`](https://rawgit.com/dusty-nv/jetson-inference/pytorch/docs/html/python/jetson.utils.html#videoSource) object:

``` python
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
```

The string passed to `videoSource()` can actually be any valid resource URI, whether it be a camera, video file, or network stream.  
#### Display Loop

Next, we'll create a video output interface with the [`videoOutput`](https://rawgit.com/dusty-nv/jetson-inference/pytorch/docs/html/python/jetson.utils.html#videoOutput) object and create a main loop that will run until the user exits:

``` python
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	# main loop will go here
```

#### Camera Capture

The first thing that happens in the main loop is to capture the next video frame from the camera.  `camera.Capture()` will wait until the next frame has been sent from the camera and loaded into GPU memory.

``` python
	img = camera.Capture()
```

The returned image will be a [`jetson.utils.cudaImage`](aux-image.md#image-capsules-in-python) object that contains attributes like width, height, and pixel format:

```python
<jetson.utils.cudaImage>
  .ptr      # memory address (not typically used)
  .size     # size in bytes
  .shape    # (height,width,channels) tuple
  .width    # width in pixels
  .height   # height in pixels
  .channels # number of color channels
  .format   # format string
  .mapped   # true if ZeroCopy
```


#### Detecting Objects

Next the detection network processes the image with the `net.Detect()` function.  It takes in the image from `camera.Capture()` and returns a list of detections:

``` python
	detections = net.Detect(img)
```

This function will also automatically overlay the detection results on top of the input image.

If you want, you can add a `print(detections)` statement here, and the coordinates, confidence, and class info will be printed out to the terminal for each detection result.  Also see the [`detectNet`](https://rawgit.com/dusty-nv/jetson-inference/python/docs/html/python/jetson.inference.html#detectNet) documentation for info about the different members of the `Detection` structures that are returned for accessing them directly in a custom application.

#### Rendering

Finally we'll visualize the results with OpenGL and update the title of the window to display the current peformance:

``` python
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
```

The `Render()` function will automatically flip the backbuffer and present the image on-screen.

#### Source Listing

That's it!  For completness, here's the full source of the Python script that we just created:

``` python
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
```

Note that this version assumes you are using a MIPI CSI camera.


## Running the Program

To run the application we just coded, simply launch it from a terminal with the Python interpreter:

``` bash
$ python3 my-detection.py
```

To tweak the results, you can try changing the model that's loaded along with the detection threshold.  Have fun!

