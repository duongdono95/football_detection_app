from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout, QSlider, QProgressBar, QApplication
)
from PySide6.QtCore import Qt, QUrl
from PySide6 import QtMultimediaWidgets, QtMultimedia, QtCore

from src.core.constants.constants import VALID_IMAGE_EXTENSIONS, VALID_VIDEO_EXTENSIONS
from src.core.states import global_states
from src.utils.functions import extract_path_features


class VideoMode(QGroupBox):
    def __init__(self, body_level):
        super().__init__()
        self.body_level = body_level
        self.setup_ui()

        # Connect global path update
        global_states.path_state.path_updated.connect(self.handle_path_updated)
        global_states.model_states.progress_bar_updated.connect(self.handle_update_progress_bar)

    def setup_ui(self):
        # === Video Widget ===
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.video_widget.setFixedSize(1000, 500)

        self.video_container = QWidget()
        self.video_container_layout = QVBoxLayout(self.video_container)
        self.video_container_layout.addWidget(self.video_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        # === Controls ===
        self.play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause")
        self.slider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)

        self.play_btn.clicked.connect(lambda: self.media_player.play() if self.media_player else None)
        self.pause_btn.clicked.connect(lambda: self.media_player.pause() if self.media_player else None)
        self.slider.sliderMoved.connect(self.set_position)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.pause_btn)
        controls_layout.addWidget(self.slider)

        self.controls_widget = QWidget()
        self.controls_widget.setLayout(controls_layout)

        # === Process Button ===
        self.process_btn = QPushButton("Process Video")
        self.process_btn.clicked.connect(self.handle_process_video_request)

        self.progress_bar = QProgressBar()

        # === Layout Setup ===
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_container)
        layout.addWidget(self.controls_widget)
        layout.addWidget(self.process_btn)
        layout.addWidget(self.progress_bar)
    
    def clean_up(self):
        if self.media_player:
            self.media_player.stop()
            self.media_player.deleteLater()
            self.media_player = None
            self.controls_widget.setVisible(False)
            
    def update_slider_position(self, position: int):
        self.slider.setValue(position)

    def update_slider_range(self, duration: int):
        self.slider.setRange(0, duration)

    def set_position(self, position: int):
        if self.media_player:
            self.media_player.setPosition(position)
            
            
    def handle_path_updated(self, file_path: str):
        
        path_details = extract_path_features(file_path)
        if path_details["extension"] in VALID_IMAGE_EXTENSIONS:
            self.clean_up()
            return
        
        self.media_player = QtMultimedia.QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)
        self.video_widget.show()

        self.media_player.setSource(QtCore.QUrl.fromLocalFile(file_path))
        self.media_player.positionChanged.connect(self.update_slider_position)
        self.media_player.durationChanged.connect(self.update_slider_range)
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)

        self.media_player.play()

        self.controls_widget.setVisible(True)

    def handle_process_video_request(self):
        path = global_states.path_state.current_path
        if len(path) > 0:
            self.progress_bar.setValue(0)
            global_states.model_states.trigger_process_video_request(path)

    def handle_update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)
        QApplication.processEvents() 
        
    def handle_media_status(self, status):
        if status == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            if self.media_player:
                self.media_player.pause()
