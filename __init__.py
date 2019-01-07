"""Content Menu Plugin Init
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from pytsite import reg
    from plugins import menu
    from . import _model

    if reg.get('content_menu.register_default_model', True):
        menu.register_model('content_menu', _model.ContentMenu, __name__ + '@content')

