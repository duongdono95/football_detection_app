from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QGroupBox, QMessageBox
import pickle , os
from pathlib import Path
import json
from pathlib import Path
import warnings

class PathState(QObject):
    path_updated = Signal(str)
    def __init__(self):
        super().__init__()
        self.current_path = ""
        
    def set_path(self, path):
        if path != self.current_path and len(path) > 0:
            self.current_path = path
            self.path_updated.emit(path)
            
    def get_path(self, path):
        return self.current_path
    
    def remove_path(self):
        self.current_path = ""
        