
# 🧠 Project Overview
#### App Interface
![App Interface](https://github.com/duongdono95/football_detection_app/blob/main/src/assets/app_interface.png?raw=true)
#### Test Result
![Test Result](https://github.com/duongdono95/football_detection_app/blob/main/src/assets/result_test.jpg?raw=true)

SoccerVision is an intelligent desktop application designed to detect and track key objects on a soccer field, including players (accuracy ~95%, confidence: above 90%), teams (accuracy ~70%, confidence: ~70%), balls (accuracy: 89%, confidence: above 80%), and jersey numbers (still in training)— from recorded match videos. Leveraging the YOLOv5 deep learning architecture, the system delivers real-time, high-accuracy object detection (90%+ accuracy) and visualizes results using bounding boxes.

This application is built for performance, modularity, and ease of use — ideal for use in sports analytics, broadcast enhancement, or training reviews.

For Model Downloading, please contact me for the Download Links.

# Getting Started:
## Dependencies

#### Python 3.11
#### 🧠 Core AI & Deep Learning
* torch – Deep learning framework powering YOLOv5.

* torchvision – Common image transforms and model utilities.

* torchaudio – (Included with PyTorch install, though not directly used for image tasks.)

* ultralytics – YOLOv5-based object detection framework.

#### 📷 Image & Video Processing
opencv-python – Video frame handling and drawing bounding boxes.

#### 📊 Data & Analysis
* numpy – Efficient numerical operations.

* pandas – Data manipulation and CSV processing.

* scipy – Scientific computation.

* matplotlib, seaborn – Visualization for debugging and analysis.

#### 🖼️ GUI / Desktop App
* PySide6, PySide6_Essentials, PySide6_Addons, shiboken6 – Used to build the desktop interface.

#### 🖼Others
* Please refers to requirements.txt

## 🛠️ Setup & Run Instructions
#### 🔹 macOS / Linux:
* python3 -m venv venv
* source venv/bin/activate

#### 🔹 Windows
* python -m venv venv
* venv\Scripts\activate.bat

#### Installation
* pip install -r requirements.txt

#### ▶️ Run the Application
* python app.py