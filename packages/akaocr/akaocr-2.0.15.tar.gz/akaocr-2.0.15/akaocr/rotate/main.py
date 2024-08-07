# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import traceback
from akaocr.rotate.center import Classifier


class ClsEngine:
    def __init__(self, model_path=None, 
                 conf_thres=0.75, 
                 device='cpu', 
                 num_workers=1) -> None:
        self.text_rotator = Classifier(model_path, conf_thres, device, num_workers)

    def __call__(self, image) -> tuple:
        # Get rotation angle of cropped text image|images

        rot_res = None
        try:
            if isinstance(image, list):
                rot_res = self.text_rotator(image)
            else:    
                rot_res = self.text_rotator([image])
        except Exception:
            print(traceback.format_exc())
            
        return rot_res