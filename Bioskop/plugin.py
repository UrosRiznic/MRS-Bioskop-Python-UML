from plugin_framework.plugin import Plugin
from .widgets.hale_list import HaleListWidget

class Main(Plugin):

    def __init__(self, spec):

        super().__init__(spec)

    def get_widget(self, parent=None):
        return HaleListWidget(parent), None, None
