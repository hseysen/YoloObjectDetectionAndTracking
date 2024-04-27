# YOLOv5 Object Detection and Tracking in PyTorch
## About
Welcome to the YOLOv5 Object Detection and Tracking repository! This repository contains the code written in the "[PyTorch: How to DETECT and TRACK objects in a video using YOLOv5](https://www.youtube.com/watch?v=jNc4JdX8FHA)" video on my [YouTube channel](https://www.youtube.com/channel/UC9V66IyJFFmsYmN6QDT63xw).

## Get Started
First, clone the repository:
```bash
git clone https://github.com/hseysen/YoloObjectDetectionAndTracking.git
```

Next, create a virtual environment and install the requirements:
```bash
cd YoloObjectDetectionAndTracking
python -m venv venv/
source venv/Scripts/activate
python -m pip install -r requirements.txt
```

Additionally, install the relevant PyTorch version depending on your operating system by visiting [this](https://pytorch.org/get-started/locally/) link.

Downloading the [input video](https://www.youtube.com/watch?v=IjBazObNYMg) provided in the channel (you can use something like [SaveFrom](https://en.savefrom.net/)), or use a video of your own. Make sure that the video is put inside a folder called `videos`, as shown in the tutorial.

## Run the code
You can simply run the `main.py` file in the repository:
```bash
python main.py
```

## Contributing
You can contribute by submitting any bugs you have faced. Although the tracking algorithm in this repository is not the most efficient one, it is outside the scope of this project to improve the algorithm's efficiency.