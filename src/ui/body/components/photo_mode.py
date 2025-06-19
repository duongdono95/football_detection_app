from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QGroupBox, QMessageBox, QStackedWidget
from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QPixmap
from src.core.constants.constants import VALID_IMAGE_EXTENSIONS
from src.core.states import global_states
from src.utils.functions import extract_path_features, show_message

class PhotoMode(QWidget):
    def __init__(self, body_level):
        super().__init__()
        self.body_level = body_level
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("Photo Viewer")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(50)
        
        self.image_frame = QLabel()
        self.image_frame.setMinimumSize(1000, 500)
        self.image_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_container = QGroupBox()
        self.image_container_layout = QVBoxLayout(self.image_container)
        self.image_container_layout.addWidget(self.image_frame)
        
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self.handle_processing_request) # type: ignore
        layout.addWidget(title)
        layout.addWidget(self.image_container, 5)
        layout.addWidget(self.process_button)
        
        global_states.path_state.path_updated.connect(self.handle_path_updated)
        
    def handle_path_updated(self, path):
        path_details = extract_path_features(path)
        if path_details["is_image"]:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                show_message("Can't read selected file, Please select another Image.", "Error", self)
                return
            target_size = self.image_container.size()
            scaled_pixmap = pixmap.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_frame.setPixmap(scaled_pixmap)
    
    def handle_processing_request(self):
        path = global_states.path_state.current_path
        if len(path) > 0:
            success = global_states.model_states.trigger_process_image_request(path)
            if success:
                show_message("Image has been saved to './output' folder.", "Success", self)
            