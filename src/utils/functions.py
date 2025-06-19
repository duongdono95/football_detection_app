from pathlib import Path
import os
from PySide6.QtWidgets import QMessageBox
from typing import List, Tuple, TypedDict, Literal, Optional
import cv2
import numpy as np
from src.core.constants.types import DetectedObjectType, JerseyObjectType
from src.core.constants.constants import VALID_IMAGE_EXTENSIONS
from PySide6.QtWidgets import QWidget

class PathDetails(TypedDict):
    path: Path
    shortcut: str
    parent_folder: str
    file_name: str
    file_id: str
    extension: str
    is_image: bool

def extract_path_features(path) -> PathDetails:
        path = Path(path.strip())
        file_name = path.name
        file_id, extension = file_name.split(".")
        patrent_name = path.parent.name
        shortcut_path = str(os.path.join("~",patrent_name, file_name))
        is_image = True if f".{extension}" in VALID_IMAGE_EXTENSIONS else False
        return {
            "path": path,
            "shortcut": shortcut_path,
            "parent_folder": patrent_name,
            "file_name": file_name,
            "file_id": file_id,
            "extension":  extension, 
            "is_image": is_image
        }
        
def detect_objects(model, image: str | np.ndarray, size:int = 1920):
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise ValueError(f"Unable to read image from path: {image}")
    elif not isinstance(image, np.ndarray):
        raise TypeError("Image must be either a file path or a NumPy ndarray")

    results = model(image, size=size) # type: ignore
    detections = results.pandas().xyxy[0].to_dict(orient="records")
    return detections

def show_message(message: str, title:Literal["Success", "Warning", "Error", "Question", "Info"], parent:Optional[QWidget] = None):
        icon_map = {
            "Success": QMessageBox.Icon.Information,
            "Info": QMessageBox.Icon.Information,
            "Warning": QMessageBox.Icon.Warning,
            "Error": QMessageBox.Icon.Critical,
            "Question": QMessageBox.Icon.Question,
        }

        icon = icon_map.get(title, QMessageBox.Icon.Information)
        QMessageBox(icon, title, message, parent=parent).exec()
        
def process_image(rgb: np.ndarray, football_detector, digit_detector, get_unique_id):
    """ ========================== Detect Objects on the field ========================== """
    objects = detect_objects(football_detector, rgb, 1920)
    detected_objects = []
    best_ball_object = None
    best_ball_confidence = 0
    
    # Early exit if no objects were detected
    if len(objects) == 0:
        return detected_objects, rgb
    
    for object in objects:
        xmin, ymin = int(object["xmin"]), int(object["ymin"])
        xmax, ymax = int(object["xmax"]), int(object["ymax"])
        obj_class = object["class"]
        confidence = object["confidence"]    
        """ ========================== Detect Jersey Numbers ========================== """
        if object["class"] in [1, 3, 4]:
            # Filter bad predictions
            if confidence >= 0.8: 
                
                detected_player_object: DetectedObjectType = {
                    "id": get_unique_id(),
                    "class_id": obj_class,
                    "confidence": confidence,
                    "bbox": (xmin, ymin, xmax, ymax),
                    "label": object["name"],
                    "jerseys": None,
                }
                

                # crop players from original image
                cropped_player = rgb[ymin:ymax, xmin:xmax]
                jerseys_raw = detect_objects(digit_detector, cropped_player, 640)

                # Sort jerseys bboxes and assign unique IDs
                sorted_jersey_bboxes:List[JerseyObjectType] = []
                
                for jersey in sorted(jerseys_raw, key=lambda d: d["xmin"]):
                    if jersey["confidence"] > 0.45:
                        base_jersey:JerseyObjectType = {
                        "id": get_unique_id(),
                        "class_id": jersey["class"],
                        "confidence": jersey["confidence"],
                        "bbox": (jersey["xmin"], jersey["ymin"], jersey["xmax"], jersey["ymax"]),
                        "name": jersey["name"],
                        }
                        sorted_jersey_bboxes.append(base_jersey)

                if len(sorted_jersey_bboxes) > 0:
                    jersey_string = "".join(str(int(b["name"])) for b in sorted_jersey_bboxes)
                else:
                    # jersey_string = "?" # "?" if number is not visible
                    jersey_string = "team_a" if object["class"] == 3 else "team_b"
                    
                detected_player_object["jerseys"] = sorted_jersey_bboxes

                # Append current object to Detected Objects
                detected_objects.append(detected_player_object)
                if obj_class == 3: # players in team_a
                    color = (0, 255, 0)
                elif obj_class == 4: # player in team_b
                    color = (0, 0, 255)
                elif obj_class == 1: # By stander
                    color = (255, 255, 0)
                    
                draw_bbox(rgb, color, jersey_string, xmin, ymin, xmax, ymax)

        # elif object["class"] == 0: # Field
        #     color = (255, 0, 255)
        #     draw_bbox(rgb, color, "cone", xmin, ymin, xmax, ymax)
        
        if object["class"] == 2: # Ball
            if confidence > best_ball_confidence: 
                best_ball_confidence = confidence
                best_ball_object = object
                
    if best_ball_object is not None:
        detected_ball_object: DetectedObjectType = {
        "id": get_unique_id(),
        "class_id": 2,
        "confidence": best_ball_object["confidence"],
        "bbox": (best_ball_object["xmin"], best_ball_object["ymin"], best_ball_object["xmax"], best_ball_object["ymax"]),
        "label": "ball",
        "jerseys": None,
        }
        detected_objects.append(detected_ball_object)
        ball_color = (255, 0, 0)
        draw_bbox(rgb, ball_color, "ball", best_ball_object["xmin"], best_ball_object["ymin"], best_ball_object["xmax"], best_ball_object["ymax"])
    
    return detected_objects, rgb
            
def draw_bbox(rgb, color, display_name, xmin, ymin, xmax, ymax):
    """ ========================== render bounding boxes ========================== """
    text_size = 1 if max(rgb.shape) > 1000 else 0.5
    stroke_thickness = 2 if max(rgb.shape) > 1000 else 2
    y_offset = 40 if max(rgb.shape) > 1000 else 25

    # ====== Ellipse shape calculation ======
    bbox_width = xmax - xmin
    center_point = ((xmin + xmax) // 2, ymax)
    axes = (bbox_width // 2, bbox_width // 6)
    angle = 0
    start_angle = -30
    end_angle = 210

    # Ensure types are correct for OpenCV
    center = tuple(int(v) for v in center_point)
    axes = tuple(int(v) for v in axes)
    angle = int(angle)
    start_angle = int(start_angle)
    end_angle = int(end_angle)

    cv2.ellipse(
        rgb,
        center,
        axes,
        angle,
        start_angle,
        end_angle,
        color,
        stroke_thickness
    )

    # ====== Text drawing ======
    (text_width, text_height), _ = cv2.getTextSize(
        display_name,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=text_size,
        thickness=stroke_thickness
    )

    center_x = (xmin + xmax) // 2
    text_x = int(center_x - text_width // 2)
    text_y = int(ymax + y_offset)

    org = (text_x, text_y)
    cv2.putText(
        rgb,
        display_name,
        org,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=text_size,
        color=color,
        thickness=stroke_thickness
    )

    
    