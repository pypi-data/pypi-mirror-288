# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import os 
os.environ["FLAGS_allocator_strategy"] = 'auto_growth'

import traceback
from akaocr.rotate.center import Rotator


class RotateEngine():
    def __init__(self, model_path=None, conf_thres=0.75, device='cpu', num_workers=4) -> None:
        self.text_rotator = Rotator(model_path, conf_thres, device, num_workers)

    def __call__(self, image) -> tuple:

        rot_res = None
        try:
            if isinstance(image, list):
                rot_res = self.text_rotator(image)
            else:    
                rot_res = self.text_rotator([image])
        except Exception:
            print(traceback.format_exc())
            
        return rot_res
