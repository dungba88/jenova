"""dynamic class loading module"""

def load_class(class_name, *args, **kwargs):
    """Create a trigger from class name"""
    name_parts = class_name.rsplit('.', 1)
    module_name = name_parts[0]
    class_name = name_parts[1]

    loaded_module = __import__(module_name, fromlist=[class_name])
    loaded_class = getattr(loaded_module, class_name)

    return loaded_class(*args, **kwargs)
