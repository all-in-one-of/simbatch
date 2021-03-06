
class Interactions:
    current_os = -1
    logger = None

    def __init__(self, current_os, logger, comfun):
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun

    def print_info(self):
        self.logger.raw("This is interaction with 3dsmax")

    # common interactions
    def schema_item_double_click(self, param):
        self.max_open_scene(param)

    def task_item_double_click(self, param):
        self.max_open_scene(param)

    def open_setup(self, param):
        self.max_open_scene(param)

    def save_setup(self, param):
        self.save_current_scene_as(param)

    def save_setup_as_next_version(self, param):
        self.save_current_scene_as(param)

    # max interactions
    def max_open_scene(self, file):
        pass
        
    def max_import_ani(self, objects, dir):
        pass
        
    def max_import_cam(self, objects, file_or_dir):
        pass
        
    def max_import_obj(self, objects, file_or_dir):
        pass
    
    def max_simulate(self, ts, te, objects_names, cache_dir):
        pass   
        
    def max_render(self, ts, te, out_file=""):
        pass

    def max_save_scene(self, file):
        pass

    def save_current_scene_as(self, file):
        pass
