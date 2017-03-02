# -*- coding: utf-8 -*-

from denite import util
from .base import Base

import re
import glob
import os

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'rails_model'
        self.kind = 'file'

    def on_init(self, context):
        args = dict(enumerate(context['args']))
        for arg in args:
            print(arg)

    def gather_candidates(self, context):
        filenames = glob.glob('app/models/**/*.rb', recursive=True)
        return [self._convert(context, filename) for filename in filenames]

    def _convert(self, context, filename):
        result_dict = {
                'word': '{0} ({1})'.format(
                    self.to_constant(filename),
                    filename
                    ),
                'action__path': filename,
                'action__line': 1,
                'action__col': 1
                }

        return result_dict

    def to_constant(self, filename):
        filename = os.path.normpath(filename)
        filename = self.remove_base_directory(filename)
        filename = self.remove_extension(filename)
        path_components = filename.split(os.sep)
        return '::'.join(self.to_upper_camel_case(path_component) for path_component in path_components)

    def remove_base_directory(self, filename):
        return re.sub(r'^app/models/', '', filename)

    def remove_extension(self, filename):
        return os.path.splitext(filename)[0]

    def to_upper_camel_case(self, snake_case_str):
        components = snake_case_str.split('_')
        return "".join(x.title() for x in components)
