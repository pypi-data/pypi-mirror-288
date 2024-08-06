from dtPyAppFramework.decorators import singleton
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.resources import ResourceManager
from ..base_tool import AbstractTool

import logging
import os
import importlib


@singleton()
class ToolManager:

    def __init__(self, resource_manager: ResourceManager, settings: Settings, app_definition: dict, flask_app, dev_mode=False):
        self.settings = settings
        self.resource_manager = resource_manager
        self.app_definition: dict = app_definition
        self.tools: list = []
        self.flask_app = flask_app
        self.dev_mode = dev_mode

    def _init_tool(self, module):
        tool: AbstractTool = module.Tool(self.flask_app, self.resource_manager,
                                         f"{self.app_definition.get('full_name')}, Version: {self.app_definition.get('version')}",
                                         self.settings)
        handler = tool.tool_disabled
        if tool.is_enabled():
            handler = tool.tool_home

        self.flask_app.add_endpoint(endpoint=f'/{tool.short_name()}', endpoint_name=tool.short_name(), handler=handler)
        self.flask_app.add_endpoint(endpoint=f'/{tool.short_name()}/static/<path:path>',
                                    endpoint_name=f'{tool.short_name()}_statics',
                                    handler=tool.tool_static_content)

        self.tools.append(tool)

    def load_tools(self):
        logging.info('Loading Tools into Context')
        if self.dev_mode:
            from ..dev_tools import icon_library
            self._init_tool(icon_library)
        else:
            for tool_module in self.app_definition.get('tools'):
                logging.info(f'Loading Tool: {tool_module}')
                try:
                    module = importlib.import_module(tool_module)
                    self._init_tool(module)

                except Exception as ex:
                    logging.exception(f'Error loading Tool "{tool_module}". {str(ex)}')
