from calendar import c
import sys, os
from re import L, M
from turtle import width
from typing import Literal, List
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QGroupBox
import torch, cv2
from src.core.constants.types import DetectedObjectType, JerseyObjectType
from src.core.constants.constants import DIGIT_MODEL_PATH, FOOTBALL_MODEL_PATH, ROOT_PATH, SRC_PATH
from src.utils.functions import extract_path_features, process_image, show_message
import numpy as np

from src.ui.body.components.video_mode import VideoMode
class ModelState(QObject):
    football_result_updated = Signal(list)
    progress_bar_updated = Signal(int)
    def __init__(self):
        super().__init__()
        self.load_models()
        
        # removable objects
        self.detected_objects: List[DetectedObjectType] = []
        self._id_counter = 0
    
    def get_unique_id(self) -> int:
        self._id_counter += 1
        return self._id_counter
    
    def reset_unique_id_counter(self):
        self._id_counter = 0
    
    def load_models(self):
        try:
            self.digit_detector = torch.hub.load('ultralytics/yolov5', 'custom', path=DIGIT_MODEL_PATH)
            print(f"✅ Digit model loaded from: {DIGIT_MODEL_PATH}")
        except Exception as e:
            print(f"❌ Failed to load digit model: {DIGIT_MODEL_PATH}\nError: {e}")
            sys.exit(1)
        try:
            self.football_detector = torch.hub.load('ultralytics/yolov5', 'custom', path=FOOTBALL_MODEL_PATH)
            print(f"✅ Football model loaded from: {FOOTBALL_MODEL_PATH}")
        except Exception as e:
            print(f"❌ Failed to load football model: {FOOTBALL_MODEL_PATH}\nError: {e}")
            sys.exit(1)

    def trigger_process_image_request(self, image_path):
        try:
            self.reset_unique_id_counter()
            path_details = extract_path_features(image_path)
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            detected_objects, rgb = process_image(rgb, self.football_detector, self.digit_detector, self.get_unique_id)
            
            self.detected_objects = detected_objects
            
            save_path = os.path.join(ROOT_PATH, "output", f"processed_{path_details['file_name']}.{path_details['extension']}")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            success = cv2.imwrite(save_path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            if not success:
                error_msg = f"❌ Failed to save image to: {save_path}"
                print(error_msg)
                show_message(error_msg, "Error", parent=None)
            return success
        except Exception as e:
            show_message(f"Processing Image failed:\n{str(e)}", "Error", None)
    

    def trigger_process_video_request(self, video_path):
        self.reset_unique_id_counter()
        
        path_details = extract_path_features(video_path)
        file_name = path_details["file_id"]
        output_path = os.path.join(ROOT_PATH ,"output", f"processed_{file_name}.mp4")

        try: 
            cap = cv2.VideoCapture(video_path)
            # Get original video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            current_frame = 0
            with torch.no_grad():
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        break
                    
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                    detected_objects, rgb = process_image(rgb, self.football_detector, self.digit_detector, self.get_unique_id)
                    out.write(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
                    
                    current_frame += 1
                    progress = int((current_frame / total_frames) * 100)
                    

                    self.progress_bar_updated.emit(progress)

                    # Clean up to avoid CUDA OOM
                    del detected_objects
                    del rgb
                    torch.cuda.empty_cache()

            # Release everything
            cap.release()
            out.release()
            cv2.destroyAllWindows() 
            self.progress_bar_updated.emit(100)
            show_message(f"Processed video has been saved to: \n{output_path}", "Success", parent=None)
        except Exception as e:
            show_message(f"Processing failed:\n{str(e)}", "Error")
