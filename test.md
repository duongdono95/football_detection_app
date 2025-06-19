# Soccer Player Detection in Match Videos

## 1. Brief:

The main objective of this project is to develop an intelligent desktop application that automatically detects objects on soccer field in recorded match videos using deep learning techniques. Built on the YOLOv5 architecture, the system provides accurate, real-time detection (above 90% accuracy), marking plobjectsayers with bounding boxes. 

## 2. Run Project:

Follow these steps to set up and run the project locally:

- **Create virtual environment:**
 
  ```bash conda
  conda env create -f environment.yml

  ```or local env - python 3.11.6
  pip3 -m venv venv

- **Activate virtual environment:**

  conda activate football

  ```or local env - python 3.11.6
  macos: source venv/bin/activate
  window: venv\Scripts\activate.bat

  ```or local env - python 3.11.6
  pip install -r requirements.txt


  # Packages will be installed automatically when the environment is created via the .yml file. If needed, you can manually reinstall with:
  conda env update --file environment.yml --prune


- **run the GUI application:**
  python app.py

- **To test model inference:**
  jupyter notebook test.ipynb
  or access to test.ipynb to run the project

## 3. Project Structure:

SoccerPlayerDetection/
├── .gitignore
├── app.py # GUI launcher
├── requirement.txt # Project dependencies
├── readme.md # Project overview and guide
│
├── src/
│ ├── style.css # GUI styling
│ └── ... # GUI components (modularized)
| │
| ├── models/ # Trained model weights and files
│ └── yolov5_weights.pt
│
├── test_data/ # Test images and videos
│
│
└── output/ # Processed file
│
└── app.py/ # Run Application
│
└── environment.yml  # Processed file
│
└── test.ipynb  # Test Inference file

## Libraries:

Deep Learning & CV: PyTorch, OpenCV, YOLOv5

Data Handling: NumPy, Pandas

GUI: PySide6 / PyQt

Visualization: Matplotlib, OpenCV

Others: OS, Glob, Pickle

## Requirements:

PyTorch version: 2.3.0+cu121

Cuda version: 12.8

NVIDIA-SMI: 570.133.07
