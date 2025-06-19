import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt

from src.ui.body.body import Body
from src.ui.footer.footer import Footer
from src.ui.header.header import Header


""" --------------------- Fixed ------------------------ """
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Football Detector")

        # Full screen or maximized window
        screen = self.app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(rect)

        # Central widget wrapper
        wrapper = QWidget()
        self.setCentralWidget(wrapper)

        # Layout for centering content
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Fixed-size content area
        content = QWidget()
        content.setMaximumWidth(1200)

        # Internal layout inside content
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        """ --------------------- Editable ------------------------ """
        header = Header(self)
        body = Body(self)
        
        content_layout.addWidget(header)
        content_layout.addWidget(body)
        """ ------------------------------------------------------ """
        
        """ --------------------- Fixed ------------------------ """
        # Add content to wrapper layout
        wrapper_layout.addWidget(content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_path = os.path.join(os.path.dirname(__file__), "src", "styles", "styles.css")
    with open(style_path, "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
