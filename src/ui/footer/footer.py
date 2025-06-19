from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QGroupBox, QMessageBox
from PySide6.QtCore import Signal, QObject, Qt, QAbstractListModel, QModelIndex
class Footer(QGroupBox):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        label = QLabel("Footer")
        

        layout.addWidget(label)