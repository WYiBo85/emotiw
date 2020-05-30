# -*- coding: utf-8 -*-
"""preprocess-all-modes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R-fl6VLDuneQMMovEAemB3odW4VNkuCJ

## Video Sentiment Analysis in the Wild
### Ensembling Notebook | CS231n

This notebook preprocesses input videos to extract faces, frames, poses, and audio before running pre-trained models for each modality to predict group sentiment (positive, negative, or neutral).
"""

import subprocess

# Clone the code base
subprocess.check_output("git clone 'https://github.com/kevincong95/cs231n-emotiw.git'" , shell=True)


# Install required packages
subprocess.check_output("pip install -r  '/content/cs231n-emotiw/requirements.txt'" , shell=True)

"""#### Navigate to the repo we downloaded
We will run all our commands from this repo
"""

import os
os.chdir('/content/cs231n-emotiw')

"""#### Pose Pre-Requisites
Pose extraction uses the [CMU OpenPose library](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to extract body keypoints. We have pre-compiled this library for use in Colab but some system files still need to be installed.
"""

subprocess.check_output("apt-get -qq install -y libatlas-base-dev libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev opencl-headers ocl-icd-opencl-dev libviennacl-dev" , shell=True)
subprocess.check_output("wget https://storage.googleapis.com/cs231n-emotiw/openpose/openpose.tar.gz", shell=True)
subprocess.check_output("tar -xzf openpose.tar.gz", shell=True)

"""#### Retrieve the files

The code block below demonstrates how to retrieve the files from GCS. However, feel free to skip this step if the files are already on the local disk or you have Google Drive mounted.
"""

subprocess.check_output("wget https://storage.googleapis.com/cs231n-emotiw/data/train-tiny.zip", shell=True)
subprocess.check_output("wget https://storage.googleapis.com/cs231n-emotiw/data/val-tiny.zip" , shell=True)
subprocess.check_output("wget https://storage.googleapis.com/cs231n-emotiw/data/test-tiny.zip" , shell=True)
subprocess.check_output("wget https://storage.googleapis.com/cs231n-emotiw/data/Train_labels.txt" , shell=True)
subprocess.check_output("wget https://storage.googleapis.com/cs231n-emotiw/data/Val_labels.txt" , shell=True)

"""#### Pre-Processing

Here, we will instantiate each of the preprocessors and process all of the input video files.

NOTE: Change the input parameters as needed.

WARNING: This may take several hours to complete, depending on the number of files.

In general, pre-processing will extract the following:
- Video frames
- Pose keypoints
- Faces from each video frame
- Audio waveform and audio features
"""

from src.preprocessors.scene_preprocessor import VideoPreprocessor
from src.preprocessors.face_preprocessor import FacePreprocessor
from src.preprocessors.pose_preprocessor import PosePreprocessor
from src.preprocessors.audio_preprocessor import AudioPreprocessor

video_preprocessor = VideoPreprocessor(
    video_folder= "train-tiny.zip", 
    label_file= "Train_labels.txt", 
    output_folder="train-tiny-local", 
    output_file= "train-tiny-local.zip"
)

face_preprocessor = FacePreprocessor(
    video_folder="train-tiny.zip",
    output_folder="train-tiny-faces", 
    output_file="train-tiny-faces.zip"
)

pose_preprocessor = PosePreprocessor(
    video_frame_folder="val-tiny.zip",
    output_folder="val-tiny-pose", 
    output_file="val-tiny-pose.zip"
)

audio_preprocessor = AudioPreprocessor(
    output_folder="train-tiny-audio", 
    output_file= "train-tiny-audio.zip" ,
    video_folder= "train-tiny.zip",
    label_path = "Train_labels.txt"
)

preprocessors_list = [video_preprocessor, face_preprocessor, pose_preprocessor, audio_preprocessor] 

for preprocessor in preprocessors_list:
    preprocessor.preprocess()