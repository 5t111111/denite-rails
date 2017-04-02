# -*- coding: utf-8 -*-

from denite import util
from .base import Base

import os
import site

# Add external modules
path_to_lib = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'modules')
site.addsitedir(path_to_lib)
site.addsitedir(os.path.join(path_to_lib, 'inflection'))
#
# from association import Association # noqa
# from model import Model # noqa
# from controller_file import ControllerFile # noqa
# from view import View # noqa
# from helper import Helper # noqa
# from test_model import TestModel # noqa

from collection import Collection # noqa

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'rails'
        self.kind = 'file'

    def on_init(self, context):
        try:
            context['__target'] = context['args'][0]
        except IndexError:
            raise NameError('target must be provided')

        context['__cbname'] = self.vim.current.buffer.name
        context['__root_path'] = util.path2project(self.vim, self.vim.current.buffer.name)

    def highlight(self):
        # TODO syntax does not work as expected
        self.vim.command('syntax region deniteSource_railsConstant start=+^+ end=+^.\{-}\s+')
        self.vim.command('highlight link deniteSource_railsConstant Statement')
        self.vim.command('syntax match deniteSource_railsSeparator /::/ containedin=deniteSource_railsConstant')
        self.vim.command('highlight link deniteSource_railsSeparator Identifier')
        self.vim.command('syntax region deniteSource_railsPath start=+(+ end=+)+')
        self.vim.command('highlight link deniteSource_railsPath Statement')

        self.vim.command('syntax match deniteSource_railsController /Controller:/')
        self.vim.command('highlight link deniteSource_railsController Function')
        self.vim.command('syntax match deniteSource_railsModel /Model:/')
        self.vim.command('highlight link deniteSource_railsModel String')
        self.vim.command('syntax match deniteSource_railsHelper /Helper:/')
        self.vim.command('highlight link deniteSource_railsHelper Type')
        self.vim.command('syntax match deniteSource_railsView /View:/')
        self.vim.command('highlight link deniteSource_railsView Statement')
        self.vim.command('syntax match deniteSource_railsTest /Test:/')
        self.vim.command('highlight link deniteSource_railsTest Number')

    def gather_candidates(self, context):
        # if context['__target'] == 'dwim':
        #     return [self._convert(context, association) for association in Collection(context)]
        # if context['__target'] == 'model':
        #     return [self._convert(context, model) for model in Model.find_all(context['__root_path'])]
        # if context['__target'] == 'controller':
        #     return [self._convert(context, controller) for controller in Controller.find_all(context['__root_path'])]
        # if context['__target'] == 'view':
        #     return [self._convert(context, view) for view in View.find_all(context['__root_path'])]
        # if context['__target'] == 'helper':
        #     return [self._convert(context, helper) for helper in Helper.find_all(context['__root_path'])]
        # if context['__target'] == 'test':
        #     return [self._convert(context, test_model) for test_model in TestModel.find_all(context['__root_path'])]
        # else:
        #     raise NameError('{0} is not valid denite-rails target'.format(context['__target']))
        return [self._convert(context, element) for element in Collection(context).find_files()]

    def _convert(self, context, obj):
        result_dict = {
                'word': obj.to_word(context['__root_path']),
                'action__path': obj.filepath,
                'action__line': 1,
                'action__col': 1
                }
        return result_dict
