import cv2
from layers import SaveFeature
import numpy as np
from torch.autograd.variable import Variable
import torch

CLASS_NAMES = ['Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration', 'Mass', 'Nodule', 'Pneumonia',
                'Pneumothorax', 'Consolidation', 'Edema', 'Emphysema',
                'Fibrosis', 'Pleural Thickening', 'Hernia']


def to_np(v):
    '''returns an np.array object given an input of np.array, list, tuple, torch variable or tensor.'''
    if isinstance(v, float): return np.array(v)
    if isinstance(v, (np.ndarray, np.generic)): return v
    if isinstance(v, (list,tuple)): return [to_np(o) for o in v]
    if isinstance(v, Variable): v=v.data
    if torch.cuda.is_available():
        if is_half_tensor(v): v=v.float()
    if isinstance(v, torch.FloatTensor): v=v.float()
    return v.cpu().numpy()

class HeatmapGenerator:

    def __init__(self, chexnet):
        self.chexnet = chexnet
        self.sf = SaveFeature(chexnet.backbone)
        self.weight = list(list(self.chexnet.head.children())[-1].parameters())[0]

    def cam(self, pred_y):
        heatmap = self.sf.features[0].permute(1, 2, 0) @ self.weight[pred_y]
        return heatmap


    def from_prob(self, prob, w, h):
        """
        input: prob: np.array (14)
        output: heatmap np.array (h, w, 1)
        """
        pred_y = np.argmax(prob)
        heatmap = self.cam(pred_y)

        # single image
        heatmap = to_np(heatmap)
        heatmap -= heatmap.min()
        heatmap /= heatmap.max()
        heatmap = cv2.resize(heatmap, (w, h))

        return heatmap, np.take(CLASS_NAMES, to_np(pred_y))
