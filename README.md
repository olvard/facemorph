
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
