import os
from os.path import exists
from urllib.parse import urlparse

from labelme.widgets import ErrorDialog

import sys

#ultralytics gives error if stdout is None
if sys.stdout is None:
    f = open(os.devnull, 'w')
    sys.stdout = f

class Yolo:
    model_path = ""

    def __init__(self, model_path, track = False):
        self.model_path = model_path
        self.track = track

    @staticmethod
    def getUniqueName(path):
        parent_folder = os.path.basename(os.path.dirname(path))
        file_name = os.path.basename(path)
        return f"{parent_folder}/{file_name}"

    @staticmethod
    def getFileName(path):
        return os.path.basename(path)

    def setModel(self, path):
        self.model_path = path

    def getResults(self, image_paths):
        if not self.model_path.lower().endswith(".pt"):
            msgBox = ErrorDialog("Could not run the model.\nCheck model path in AI -> Object Detection Model.")
            msgBox.show()
            return None
        
        # Lazy load YOLO only when this method is called
        try:
            import importlib
            ultralytics = importlib.import_module('ultralytics')
            YOLO = getattr(ultralytics, 'YOLO')
            model = YOLO(self.model_path)
            if not self.track:
                results = model(image_paths)
            else:
                results = model.track(image_paths, persist=True)
            return results
        except (ImportError, AttributeError) as e:
            msgBox = ErrorDialog(f"Error loading YOLO model: {e}")
            msgBox.show()
            return None




    
