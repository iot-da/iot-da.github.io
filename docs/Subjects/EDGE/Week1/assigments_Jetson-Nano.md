# Week1&2&3: Introduction & Setup JetsonNano

## Sumary
* [Setting up Jetson with JetPack](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup)
* [Running the Docker Container](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md)
    * The containers use the [l4t-pytorch](https://ngc.nvidia.com/catalog/containers/nvidia:l4t-pytorch) base container, so support for transfer learning / re-training is already included
* [How to connect CSI Camera](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup) to the Jetson-Nano can be followed 


## Assigments
* All the assigments related to the setup of Jetson-Nano should be sent to professor by email. As a **Subject** write "[IoT-DA Edge] Assignments Weeks1&2&3"

### Assigment 1: Image classification
!!! danger "Assign 1"
    * Image classification using the **imagenet** script with an input example *images/strawberry_0.jpg*


### Assigment 2: Pedestrian detection
!!! danger "Assign 2"
    * Test Pedestrian Detection example running the **detectnet** script with an input example data/images/peds_3.jpg
    * Download test video with the next command and test **detectnet* with pedestrians as output

```shell
root@jetson-nano:/jetson-inference/build/aarch64/bin# wget https://nvidia.box.com/shared/static/veuuimq6pwvd62p9fresqhrrmfqz0e2f.mp4 -O images/pedestrians.mp4
root@jetson-nano:/jetson-inference/build/aarch64/bin# ./detectnet images/pedestrians.mp4 images/test/pedestrians.mp4

```


### Assigment 3: Jupyter Notebook
!!! danger "Assign 3"
    * Create a **Jupyter Notebook** that 
        1. Prints on the screen "Hello World" with the python command **print**. More info about how to use *print* could be found in the [link](https://realpython.com/python-print/)
        2. Given to vectors ```x = [5, 10, -5, 6, 9]``` and ```y = [4, -7, -1, 0.5, 8]``` write a for-loop that compute the dot product of x and y

