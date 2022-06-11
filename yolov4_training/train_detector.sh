#!/bin/bash

# Download and compile darknet
sh utils/prepare_darknet.sh

# Create setup files
python3 utils/training_setup.py

# Enter Darknet
cd darknet

# Darknet
./darknet detector train data/obj.data cfg/yolov4-obj.cfg yolov4.conv.137 -dont_show -map
