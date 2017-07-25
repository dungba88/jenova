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

        # convert class indexes to names
        for detection in detection_results:
            detection['class'] = classes[detection['class']]

        result = {
            'detections': detection_results,
            'time': time.time() - start
        }
        execution_context.finish(result)
