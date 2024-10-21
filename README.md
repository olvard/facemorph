# Facemorphing using stylegan2 and linear interpolation in w space

## Notebooks

### notebook.ipynb

Basic facemorph of two wild images using projection into W.

### align_faces.ipynb

Face alignment batch script for aligning images like the FFHQ dataset.

### batch_notebook.ipynb

Generate mulitple facemorph strips.

### multi_morph_notebook.ipynb

Morph several images into one and display the process as a pyramid. This uses a brack style intepolation until one projection remains.

## Util functions

Functions to call for generating facemorphs and aligning wild images.

## UI

### app.py

Simple ui for doing facemorph between two faces.

## Get started

Clone the repo and inside it clone the stylegan2-ada-pytorch repo

### create environment:

    conda create -n "facemorphing" python=3.8.5

    conda activate facemorphing

    conda install click requests tqdm ninja imageio-ffmpeg==0.4.3

    conda install imageio matplotlib

    conda install numpy=1.24

Install pytorch using https://pytorch.org/get-started/locally/

Download 256 resolution pretrained model:
https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/transfer-learning-source-nets/ffhq-res256-mirror-paper256-noaug.pkl
