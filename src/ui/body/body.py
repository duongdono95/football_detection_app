
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QGroupBox, QMessageBox, QStackedWidget, QTabWidget
from PySide6.QtCore import Signal, QObject, Qt, QAbstractListModel, QModelIndex

from src.core.constants.constants import VALID_IMAGE_EXTENSIONS
from src.core.states.global_states import path_state
from src.ui.body.components.photo_mode import PhotoMode
from src.ui.body.components.video_mode import VideoMode
from src.utils.functions import extract_path_features

class Body(QGroupBox):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.stack = QStackedWidget()
        
        self.photo_mode = PhotoMode(self)               # Index 0
        self.video_mode = VideoMode(self)               # Index 1
        
        self.stack.addWidget(self.photo_mode)
        self.stack.addWidget(self.video_mode)
        
        self.stack.setCurrentIndex(0)

        layout.addWidget(self.stack, 9)

        path_state.path_updated.connect(self.handle_path_updated)
        
    def switch_screen(self, index):
        self.stack.setCurrentIndex(index)
        
    def handle_path_updated(self, path):
        details = extract_path_features(path)
        if len(path) > 0:
            if details["is_image"]: 
                self.switch_screen(0)
            else:
                self.switch_screen(1)
        
