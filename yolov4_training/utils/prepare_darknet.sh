#!/bin/bash

# Select the correct cuda version
sudo rm /usr/local/cuda
sudo ln -s /usr/local/cuda-11.0 /usr/local/cuda

# Enable GPU
nvidia-smi

# Clone darknet repo
git clone https://github.com/AlexeyAB/darknet
cd darknet

# Modify make file to enable GPU and OpenCV when building project
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile
sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile

# Build darknet project
make

# Download pretrained weights
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137

# Execute darknet to check if working properly
./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights data/person.jpg
cd ..