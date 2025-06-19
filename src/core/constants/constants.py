from pathlib import Path
import os

SRC_PATH = Path(__file__).resolve().parents[2]
ROOT_PATH = Path(__file__).resolve().parents[3]

DEFAULT_TEST_FOLDER_PATH = os.path.join(ROOT_PATH, "test_data")
DIGIT_MODEL_PATH = os.path.join(SRC_PATH, "models", "digit_model_test.pt")
FOOTBALL_MODEL_PATH = os.path.join(SRC_PATH, "models", "football_yolo5s_all_classes.pt")

VALID_VIDEO_EXTENSIONS = [".mov", ".mp4"]
VALID_IMAGE_EXTENSIONS= [".jpg", ".png"]

VALID_FILE_EXTENSIONS = set(VALID_VIDEO_EXTENSIONS + VALID_IMAGE_EXTENSIONS)
VALID_FILE_EXTENSION_STRINGS = " ".join(f"*{ext}" for ext in VALID_FILE_EXTENSIONS)

# 0: field
# 1: bystander
# 2: ball
# 3: team_a
# 4: team_b