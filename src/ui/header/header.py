from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QGroupBox, QMessageBox
from PySide6.QtCore import Signal, QObject, Qt, QAbstractListModel, QModelIndex
from pathlib import Path
import os
from src.core.constants.constants import DEFAULT_TEST_FOLDER_PATH, VALID_FILE_EXTENSION_STRINGS
from src.core.states import global_states
from src.utils.functions import extract_path_features, show_message


class Header(QGroupBox):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        selected_image_title = QLabel("Selected Image: ")
        self.selected_image_name = QLabel("N/A")
        
        button = QPushButton("Select Path")
        button.clicked.connect(self.select_image_file) # type: ignore
        
        content = QWidget()
        conent_layout = QHBoxLayout(content)
        conent_layout.addWidget(selected_image_title, 1)
        conent_layout.addWidget(self.selected_image_name, 4)
        
        global_states.path_state.path_updated.connect(self.update_path)
        
        layout.addWidget(content, 4)
        layout.addWidget(button, 1)
        
    def select_image_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an Image",
            DEFAULT_TEST_FOLDER_PATH,
            VALID_FILE_EXTENSION_STRINGS
        )
        
        if file_path:
            global_states.path_state.set_path(file_path)
        else:
            show_message("No Path selected or can't read the file.", "Error", self)
            self.selected_image_name.setText("N/A")

    def update_path(self, path):
        details = extract_path_features(path)
        self.selected_image_name.setText(str(details["shortcut"]))
        