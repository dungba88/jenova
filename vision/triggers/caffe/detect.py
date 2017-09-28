"""Trigger implementation for initializing caffe"""

class DetectObject(object):
    """Trigger to detect object"""

    def run(self, execution_context, app_context):
        """run the action"""
        from vision_utils.image import imageio
        from vision_utils.object_detection import detect

        classes = app_context.get_config('detect.classes')

        test_net = app_context.params['test_net']
        if test_net is None:
            raise ValueError('Test Net is not initialized')

        img_base64 = execution_context.event.get('image')
        if img_base64 is None:
            raise ValueError('Image data is not defined')

        import time
        start = time.time()
        # try to detect objects
        img = imageio.read_base64(str(img_base64))
        detection_results = detect.detect_classes(test_net, img, {
            'conf_thresh': 0.8,
            'nms_thresh': 0.3
        })

        distance_meter = app_context.get_config('detect.distance_meter')
        metric_mappings = distance_meter['real_metric_mappings']
        focal_length = distance_meter['focal_length']

        # convert class indexes to names
        for detection in detection_results:
            detection['class'] = classes[detection['class']]
            if detection['class'] in metric_mappings:
                populate_distances(metric_mappings[detection['class']], focal_length, detection['boxes'])

        result = {
            'detections': detection_results,
            'time': time.time() - start
        }
        execution_context.finish(result)

def populate_distances(metric_mapping, focal_length, boxes):
    """calculate distance to target heuristically"""
    for box in boxes:
        box_width = box['coord'][2] - box['coord'][0]
        box_height = box['coord'][3] - box['coord'][1]
        box['distance'] = calculate_distance(metric_mapping, focal_length, box_width, box_height)

def calculate_distance(metric_mapping, focal_length, box_width, box_height):
    """calculate distance for a single box"""
    use_width = box_width < box_height
    if use_width:
        return metric_mapping['w'] / box_width * focal_length
    return metric_mapping['h'] / box_height * focal_length
