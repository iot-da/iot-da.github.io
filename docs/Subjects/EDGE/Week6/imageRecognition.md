# Re-training on the Cat/Dog Dataset
* **Note:** information extracted from [NVIDIA laboratories](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-cat-dog.md) 

The model that we'll be re-training is a simple model that recognizes two classes:  cat or dog.

<img src="https://github.com/dusty-nv/jetson-inference/raw/python/docs/images/pytorch-cat-dog.jpg" width="700">

Provided below is an 800MB dataset that includes 5000 training images, 1000 validation images, and 200 test images, each evenly split between the cat and dog classes.  The set of training images is used for transfer learning, while the validation set is used to evaluate classification accuracy during training, and the test images are to be used by us after training completes.  The network is never directly trained on the validation and test sets, only the training set.

The images from the dataset are made up of many different breeds of dogs and cats, including large felines like tigers and mountain lions since the amount of cat images available was a bit lower than dogs.  Some of the images also picture humans, which the detector is essentially trained to ignore as background and focus on the cat vs. dog content.

To get started, first make sure that you have [PyTorch installed](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-transfer-learning.md#installing-pytorch) on your Jetson, then download the dataset below and kick off the training script.  After that, we'll test the re-trained model in TensorRT on some static images and a live camera feed. 

## Downloading the Data

During this tutorial, we'll store the datasets on the host device under `jetson-inference/python/training/classification/data`, which is one of the directories that is automatically mounted into the container.  This way the dataset won't be lost when you shutdown the container.

``` bash
nano@jetson-nano:~$ cd jetson-inference/python/training/classification/data
nano@jetson-nano:~/jetson-inference/python/training/classification/data$ wget https://nvidia.box.com/shared/static/o577zd8yp3lmxf5zhm38svrbrv45am3y.gz -O cat_dog.tar.gz
nano@jetson-nano:~/jetson-inference/python/training/classification/data$ tar xvzf cat_dog.tar.gz
```

Mirrors of the dataset are available here:

* <a href="https://drive.google.com/file/d/16E3yFvVS2DouwgIl4TPFJvMlhGpnYWKF/view?usp=sharing">https://drive.google.com/file/d/16E3yFvVS2DouwgIl4TPFJvMlhGpnYWKF/view?usp=sharing</a>
* <a href="https://nvidia.box.com/s/o577zd8yp3lmxf5zhm38svrbrv45am3y">https://nvidia.box.com/s/o577zd8yp3lmxf5zhm38svrbrv45am3y</a>

## Re-training ResNet-18 Model

The PyTorch training scripts are located in the repo under <a href="https://github.com/dusty-nv/jetson-inference/tree/master/python/training/classification">`jetson-inference/python/training/classification/`</a>.  These scripts aren't specific to any one dataset, so we'll use the same PyTorch code with each of the example datasets from this tutorial.  By default it's set to train a ResNet-18 model, but you can change that with the `--arch` flag.

To launch the training, run the following commands:

``` bash
nano@jetson-nano:~/jetson-inference$ sudo init 3
nano@jetson-nano:~/jetson-inference$ docker/run.sh
root@jetson-nano:/jetson-inference# cd python/training/classification
root@jetson-nano:/jetson-inference/python/training/classification# python3 train.py --batch-size=2 --workers=1  --model-dir=models/cat_dog data/cat_dog
Use GPU: 0 for training
=> dataset classes:  2 ['cat', 'dog']
=> using pre-trained model 'resnet18'
Downloading: "https://download.pytorch.org/models/resnet18-f37072fd.pth" to /root/.cache/torch/hub/checkpoints/resnet18-f37072fd.pth
100.0%
=> reshaped ResNet fully-connected layer with: Linear(in_features=512, out_features=2, bias=True)
```

> **note:** if you run out of memory or your process is "killed" during training, try [Mounting SWAP](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-transfer-learning.md#mounting-swap) and [Disabling the Desktop GUI](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-transfer-learning.md#disabling-the-desktop-gui). <br/>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; to save memory, you can also reduce the `--batch-size` (default 8) and `--workers` (default 2)
  
As training begins, you should see text appear from the console like the following:

``` bash
Use GPU: 0 for training
=> dataset classes:  2 ['cat', 'dog']
=> using pre-trained model 'resnet18'
=> reshaped ResNet fully-connected layer with: Linear(in_features=512, out_features=2, bias=True)
Epoch: [0][   0/2500]  Time 95.370 (95.370)  Data  4.801 ( 4.801)  Loss 6.3362e-01 (6.3362e-01)  Acc@1  50.00 ( 50.00)  Acc@5 100.00 (100.00)
Epoch: [0][  10/2500]  Time  0.225 ( 9.306)  Data  0.000 ( 0.709)  Loss 0.0000e+00 (1.6583e+01)  Acc@1 100.00 ( 50.00)  Acc@5 100.00 (100.00)
Epoch: [0][  20/2500]  Time  0.222 ( 4.981)  Data  0.000 ( 0.377)  Loss 2.5114e+02 (6.3377e+01)  Acc@1  50.00 ( 57.14)  Acc@5 100.00 (100.00)
Epoch: [0][  30/2500]  Time  0.223 ( 3.446)  Data  0.000 ( 0.260)  Loss 1.0363e+01 (5.5885e+01)  Acc@1  50.00 ( 58.06)  Acc@5 100.00 (100.00)
Epoch: [0][  40/2500]  Time  0.226 ( 2.660)  Data  0.000 ( 0.199)  Loss 2.2514e+00 (4.3716e+01)  Acc@1   0.00 ( 52.44)  Acc@5 100.00 (100.00)

```

To stop training at any time, you can press `Ctrl+C`.  You can also restart the training again later using the `--resume` and `--epoch-start` flags, so you don't need to wait for training to complete before testing out the model.  

Run `python3 train.py --help` for more information about each option that's available for you to use, including other networks that you can try with the `--arch` flag.

### Training Metrics

The statistics output above during the training process correspond to the following info:

* Epoch:  an epoch is one complete training pass over the dataset
	* `Epoch: [N]` means you are currently on epoch 0, 1, 2, ect.
	* The default is to run for 35 epochs (you can change this with the `--epochs=N` flag)
* `[N/625]` is the current image batch from the epoch that you are on
	* Training images are processed in mini-batches to improve performance
	* The default batch size is 8 images, which can be set with the `--batch=N` flag
	* Multiply the numbers in brackets by the batch size (e.g. batch `[100/625]` -> image `[800/5000]`)
* Time:  processing time of the current image batch (in seconds)
* Data:  disk loading time of the current image batch (in seconds)
* Loss:  the accumulated errors that the model made (expected vs. predicted)
* `Acc@1`:  the Top-1 classification accuracy over the batch
	* Top-1, meaning that the model predicted exactly the correct class
* `Acc@5`:  the Top-5 classification accuracy over the batch
	* Top-5, meaning that the correct class was one of the Top 5 outputs the model predicted
	* Since this Cat/Dog example only has 2 classes (Cat and Dog), Top-5 is always 100%
	* Other datasets from the tutorial have more than 5 classes, where Top-5 is valid 

You can keep an eye on these statistics during training to gauge how well the model is trained, and if you want to keep going or stop and test.  As mentioned above, you can restart training again later if you desire.

### Model Accuracy

On this dataset of 5000 images, training ResNet-18 takes approximately ~7-8 minutes per epoch on Jetson Nano, or around 4 hours to train the model to 35 epochs and 80% classification accuracy.  Below is a graph for analyzing the training progression of epochs versus model accuracy:

<p align="center"><img src="https://github.com/dusty-nv/jetson-inference/raw/python/docs/images/pytorch-cat-dog-training.jpg" width="700"></p>

At around epoch 30, the ResNet-18 model reaches 80% accuracy, and at epoch 65 it converges on 82.5% accuracy.  With additional training time, you could further improve the accuracy by increasing the size of the dataset or by trying more complex models.

By default the training script is set to run for 35 epochs, but if you don't wish to wait that long to test out your model, you can exit training early and proceed to the next step (optionally re-starting the training again later from where you left off).  You can also download this completed model that was trained for a full 100 epochs from here:

* <a href="https://nvidia.box.com/s/zlvb4y43djygotpjn6azjhwu0r3j0yxc">https://nvidia.box.com/s/zlvb4y43djygotpjn6azjhwu0r3j0yxc</a>

Note that the models are saved under `jetson-inference/python/training/classification/models/cat_dog/`, including a checkpoint from the latest epoch and the best-performing model that has the highest classification accuracy.  This `classification/models` directory is automatically mounted into the container, so your trained models will persist after the container is shutdown.

## Converting the Model to ONNX

To run our re-trained ResNet-18 model with TensorRT for testing and realtime inference, first we need to convert the PyTorch model into <a href="https://onnx.ai/">ONNX format</a> format so that TensorRT can load it.  ONNX is an open model format that supports many of the popular ML frameworks, including PyTorch, TensorFlow, TensorRT, and others, so it simplifies transferring models between tools.

PyTorch comes with built-in support for exporting PyTorch models to ONNX, so run the following command to convert our Cat/Dog model with the provided `onnx_export.py` script:

``` bash
root@jetson-nano:/jetson-inference/python/training/classification# python3 onnx_export.py --model-dir=models/cat_dog
Namespace(input='model_best.pth.tar', model_dir='models/cat_dog', no_softmax=False, output='')
running on device cuda:0
loading checkpoint:  models/cat_dog/model_best.pth.tar
using model:  resnet18
....
exporting model to ONNX...
....
model exported to:  models/cat_dog/resnet18.onnx
....
```

This will create a model called `resnet18.onnx` under `jetson-inference/python/training/classification/models/cat_dog/`

## Processing Images with TensorRT

To classify some static test images, we'll use the extended command-line parameters to `imagenet` to load our customized ResNet-18 model that we re-trained above.  To run these commands, the working directory of your terminal should still be located in:  `jetson-inference/python/training/classification/`

```bash
root@jetson-nano:/jetson-inference/build/aarch64/bin# NET=/jetson-inference/python/training/classification/models/cat_dog
root@jetson-nano:/jetson-inference/build/aarch64/bin# DATASET=/jetson-inference/python/training/classification/data/cat_dog

# C++
root@jetson-nano:/jetson-inference/build/aarch64/bin# imagenet --model=$NET/resnet18.onnx --input_blob=input_0 --output_blob=output_0 --labels=$DATASET/labels.txt $DATASET/test/cat/01.jpg images/test/my_cat.jpg

# Python
root@jetson-nano:/jetson-inference/build/aarch64/bin# imagenet.py --model=$NET/resnet18.onnx --input_blob=input_0 --output_blob=output_0 --labels=$DATASET/labels.txt $DATASET/test/cat/01.jpg images/test/my_cat.jpg
```

<img src="https://github.com/dusty-nv/jetson-inference/raw/python/docs/images/pytorch-cat.jpg">


### Processing all the Test Images

There are 200 test images included with the dataset between the cat and dog classes, or you can download your own pictures to try.  You can process them all like this:

``` bash
mkdir $DATASET/test_output_cat $DATASET/test_output_dog

imagenet --model=$NET/resnet18.onnx --input_blob=input_0 --output_blob=output_0 --labels=$DATASET/../labels.txt \
           $DATASET/test/cat $DATASET/test_output_cat

imagenet --model=$NET/resnet18.onnx --input_blob=input_0 --output_blob=output_0 --labels=$DATASET/../labels.txt \
           $DATASET/test/dog $DATASET/test_output_dog
```

In this instance, all the images will be read from the dataset's `test/` directory, and saved to the `test_output/` directory.  

For more info about loading/saving sequences of images, see the [Camera Streaming and Multimedia](../Week1/setup_Jetson-Nano/#camera-setup).

Next, we'll try running our re-trained model on a live camera feed.

# Collecting your own Classification Datasets

In order to collect your own datasets for training customized models to classify objects or scenes of your choosing, we've created an easy-to-use tool called `camera-capture` (NOTE: /jetson-inference/build/aarch64/bin/camera-capture) for capturing and labeling images on your Jetson from live video:

<img src="https://github.com/dusty-nv/jetson-inference/raw/python/docs/images/pytorch-collection.jpg" >

The tool will create datasets with the following directory structure on disk:

```
‣ train/
	• class-A/
	• class-B/
	• ...
‣ val/
	• class-A/
	• class-B/
	• ...
‣ test/
	• class-A/
	• class-B/
	• ...
```

where `class-A`, `class-B`, ect. will be subdirectories containing the data for each object class that you've defined in a class label file.  The names of these class subdirectories will match the class label names that we'll create below.  These subdirectories will automatically be populated by the tool for the `train`, `val`, and `test` sets from the classes listed in the label file, and a sequence of JPEG images will be saved under each.

Note that above is the organization structure expected by the PyTorch training script that we've been using.  If you inspect the Cat/Dog and PlantCLEF datasets, they're also organized in the same way.

## Creating the Label File
Under `jetson-inference/python/training/classification/data`, create an empty directory for storing your dataset and a text file that will define the class labels (usually called `labels.txt`).  The label file contains one class label per line, and is alphabetized (this is important so the ordering of the classes in the label file matches the ordering of the corresponding subdirectories on disk).

Here's an example `labels.txt` file with 3 classes:

``` bash
class-A
class-B
class-C
```

And here's the corresponding directory structure that the tool will create:

``` bash
‣ train/
	• class-A/
	• class-B/
	• class-C/
‣ val/
	• class-A/
	• class-B/
	• class-C/
‣ test/
	• class-A/
	• class-B/
	• class-C/
```

## Assignment 
* If you have finished all the steps mentioned before, you are ready to perform the task

!!! note "Homework"
	Create your own dataset with the **camera-capture** tool, for example a database with three objects: 
               * No person
               * Yourself
               * Yourself with a medical mask wearn
	Taking into account the global situation with the pandemic and COVID-19, create an IoT system that detects if a person is wearing a medical mask using an image classifier based on ResNet18 whose training can be carried out using a dataset created by yourself
**Please send a message to the professor as soon as you finished**

