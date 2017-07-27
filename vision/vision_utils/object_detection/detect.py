"""Utility for detect object in image"""

from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
import numpy as np

def detect_classes(net, img, cfg):
    """detect all objects in an OpenCV image"""

    scores, boxes = im_detect(net, img)

    num_classes = len(scores[0])

    nms_thresh = cfg['nms_thresh']
    conf_thresh = cfg['conf_thresh']

    result = []

    for cls_ind in range(1, max(num_classes, 1)):
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)] # all boxes coordinates for current class
        cls_scores = scores[:, cls_ind] # all scores for current class
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)

        # use non-maximum suppression to remove overlapping boxes
        dets = suppress_overlap(dets, nms_thresh)

        # only take the boxes with sufficient score
        inds = np.where(dets[:, -1] >= conf_thresh)[0]

        if len(inds) > 0:
            detection_boxes = map_to_detection_boxes(dets, inds)
            result.append({
                'class': cls_ind,
                'boxes': detection_boxes
            })

    return result

def suppress_overlap(dets, nms_thresh):
    """suppress overlapping boxes"""
    keep = nms(dets, nms_thresh)
    return dets[keep, :]

def map_to_detection_boxes(dets, inds):
    """map matrix to detection boxes"""
    detection_boxes = []
    for i in inds:
        coord = dets[i, :4]
        score = dets[i, -1]
        detection_boxes.append({
            'coord': coord.tolist(),
            'score': score.item()
        })
    return detection_boxes
