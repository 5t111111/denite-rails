# -*- coding: utf-8 -*-

from denite import util
from .base import Base
import re
import glob
import os
import site

path_to_this = os.path.abspath(os.path.dirname(__file__))
site.addsitedir(os.path.join(path_to_this, 'rails'))
site.addsitedir(os.path.join(path_to_this, 'rails', 'Inflector'))

from model import Model
from controller import Controller
from view import View
from helper import Helper


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

    def highlight(self):
        # TODO syntax does not work as expected
        self.vim.command('syntax region deniteSource_railsConstant start=+^+ end=+^.\{-}\s+')
        self.vim.command('highlight link deniteSource_railsConstant Statement')
        self.vim.command('syntax match deniteSource_railsSeparator /::/ containedin=deniteSource_railsConstant')
        self.vim.command('highlight link deniteSource_railsSeparator Identifier')
        self.vim.command('syntax region deniteSource_railsPath start=+(+ end=+)+')
        self.vim.command('highlight link deniteSource_railsPath Statement')

    def gather_candidates(self, context):
        if context['__target'] == 'model':
            return [self._convert(context, model) for model in Model.find_all()]
        if context['__target'] == 'controller':
            return [self._convert(context, controller) for controller in Controller.find_all()]
        if context['__target'] == 'view':
            return [self._convert(context, view) for view in View.find_all()]
        if context['__target'] == 'helper':
            return [self._convert(context, helper) for helper in Helper.find_all()]
        else:
            raise NameError('{0} is not valid denite-rails target'.format(context['__target']))

    def _convert(self, context, obj):
        result_dict = {
                'word': obj.to_word(),
                'action__path': obj.filepath,
                'action__line': 1,
                'action__col': 1
                }
        return result_dict
