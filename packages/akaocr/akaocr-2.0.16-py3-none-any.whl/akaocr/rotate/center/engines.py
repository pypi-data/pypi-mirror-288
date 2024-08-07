# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import numpy as np
import onnxruntime as ort
import math
import os, cv2
import math


class Classifier:
    def __init__(self, model_path=None, conf_thres=0.75, device='cpu', num_workers=4):
        # Initialize some parameters
        
        self.cls_image_shape = [3, 48, 192]
        self.cls_batch_num = 32
        self.cls_thresh = conf_thres
        self.postprocess_op = ClsPostProcess(label_list=['0', '180'])
        self.predictor, self.input_tensor, self.output_tensors = create_predictor(model_path, device, num_workers)

    @staticmethod
    def resize_image(image, img_c, img_h, img_w):
        # Resize image without distortion

        h = image.shape[0]; w = image.shape[1]
        ratio = w / float(h)
        if math.ceil(img_h * ratio) > img_w:
            resized_w = img_w
        else:
            resized_w = int(math.ceil(img_h * ratio))
        resized_image = cv2.resize(image, (resized_w, img_h))
        resized_image = resized_image.astype('float32')
        resized_image = resized_image.transpose((2, 0, 1)) / 255
        resized_image -= 0.5
        resized_image /= 0.5
        padding_im = np.zeros((img_c, img_h, img_w), dtype=np.float32)
        padding_im[:, :, 0:resized_w] = resized_image

        return padding_im

    def __call__(self, img_list):
        # calculate the aspect ratio of all text bars
        img_num = len(img_list)
        width_list = np.array([img.shape[1] / float(img.shape[0]) for img in img_list])

        # sorting can speed up the classification process
        indices = np.argsort(width_list)
        cls_res = [['', 0.0]] * img_num
        batch_num = self.cls_batch_num

        for beg_img_no in range(0, img_num, batch_num):
            end_img_no = min(img_num, beg_img_no + batch_num)
            norm_img_batch = []

            # create a batch of images
            for ino in range(beg_img_no, end_img_no):
                norm_img = self.resize_image(img_list[indices[ino]], *self.cls_image_shape)
                norm_img_batch.append(norm_img[np.newaxis, :])

            norm_img_batch = np.concatenate(norm_img_batch)
            norm_img_batch = norm_img_batch.copy()

            # infer with batch
            input_dict = {self.input_tensor.name: norm_img_batch}
            outputs = self.predictor.run(self.output_tensors, input_dict)
            preds = outputs[0]

            cls_result = self.postprocess_op(preds)
            for rno in range(len(cls_result)):
                cls_res[indices[beg_img_no + rno]] = cls_result[rno]

        return cls_res


class ClsPostProcess:
    # Convert between text-label and text-index

    def __init__(self, label_list=None, key=None, **kwargs):
        super(ClsPostProcess, self).__init__()
        self.label_list = label_list
        self.key = key

    def __call__(self, preds, label=None, *args, **kwargs):
        if self.key is not None:
            preds = preds[self.key]

        label_list = self.label_list
        if label_list is None:
            label_list = {idx: idx for idx in range(preds.shape[-1])}

        pred_idxs = preds.argmax(axis=1)
        decode_out = [(label_list[idx], preds[i, idx])
                      for i, idx in enumerate(pred_idxs)]
        if label is None:
            return decode_out
        label = [(label_list[idx], 1.0) for idx in label]
        
        return decode_out, label


def prepare_inference_session(device='cpu', num_workers=2):
    # Create session options

    so = ort.SessionOptions()
    so.intra_op_num_threads = num_workers
    so.inter_op_num_threads = 2
    so.execution_mode = ort.ExecutionMode.ORT_PARALLEL
    
    if device == 'gpu':
        # configure GPU settings
        providers = [
            'CUDAExecutionProvider', 'CPUExecutionProvider'
        ]
    else:
        # configure CPU settings
        so.enable_cpu_mem_arena = True
        providers = ['CPUExecutionProvider']

    return so, providers


def create_predictor(model_path=None, device='cpu', num_workers=2):
    # Create a predictor for ONNX model inference.

    so, providers = prepare_inference_session(device, num_workers)

    # use default model path if none provided or if the provided path does not exist
    if not model_path or not os.path.exists(model_path):
        work_dir = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(work_dir, "../data/model.onnx")

    # create the ONNX Runtime inference session
    sess = ort.InferenceSession(model_path, sess_options=so, providers=providers)

    return sess, sess.get_inputs()[0], None