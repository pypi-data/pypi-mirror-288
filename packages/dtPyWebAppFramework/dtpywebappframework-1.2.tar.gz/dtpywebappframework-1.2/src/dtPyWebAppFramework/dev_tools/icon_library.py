from ..base_tool import AbstractTool
import os


class Tool(AbstractTool):

    def add_custom_endpoints(self):
        self.resource_manager.add_resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources"))

    def is_enabled(self):
        return True

    def name(self):
        return "Icons Library"

    def short_name(self):
        return "icon_library"

    def description(self):
        return "Shows the icons which can be used to represent apps you host via this framework."

    def icon(self):
        return 'image-gallery'

    def disabled_reason(self):
        return "-"

    def tool_home_body_content(self):
        with open(self.resource_manager.get_resource_path('icon_library.html'), mode='r') as body:
            return body.read()

    def tool_static_content(self, path):
        raise NotImplementedError
