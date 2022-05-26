# Assigment 

## Intro
Taking into account the global situation with the pandemic and COVID-19, create an IoT system that detects if a person is wearing a medical mask using the CSI Camera

## Steps
### Create your own dataset
1. Create a label file: (1) none, (2) no_mask, (3) with_mask
2. Create your dataset 


<img alt="hello!" title="No Person" src="../figures/none.jpg" width="400">

<img title="No Mask" src="../figures/nomask.jpg" width="400">

<img title="With Mask" src="../figures/withmask.jpg" width="400">

### Re-training 
* Re-training the ResNet-18 Model with your input Dataset 
     * Note that apart from training, you should converting the Model to ONNX

### Inference
* Invoke the inference with your model create by yourself. Use the CSI camera to create an IoT system to identify an access control (person worn a mask)

[Click Here to download](../Week6/figures/mask-2022-05-26_11.50.00.mp4) the demo video of IoT System

