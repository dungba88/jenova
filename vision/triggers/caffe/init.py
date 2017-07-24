"""Trigger implementation for initializing caffe"""

import logging

class InitCaffe(object):
    """Trigger to initialize caffe"""

    def run(self, execution_context, app_context):
        """run the action"""
        import caffe

        # init CPU/GPU mode
        cpu_mode = app_context.get_config('caffe.cpu_mode')
        if cpu_mode:
            caffe.set_mode_cpu()
        else:
            caffe.set_mode_gpu()
            caffe.set_device(0)

        # load test model
        test_model_file = "models/" + app_context.get_config('caffe.test_model')
        trained_data_file = "cache/data/" + app_context.get_config('caffe.trained_data')
        test_net = caffe.Net(test_model_file, trained_data_file, caffe.TEST)
        app_context.params['test_net'] = test_net

        logging.getLogger(__name__).info('Loaded neural network: ' + trained_data_file)
