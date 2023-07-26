import os

import confuse


class Config(confuse.LazyConfig):
    def __init__(self, name=None):
        super().__init__('mucus', __name__)
        if name is not None:
            filename = os.path.join(self.config_dir(), name)
            if not filename.endswith('.yaml'):
                filename += '.yaml'
            self.set_file(filename)
