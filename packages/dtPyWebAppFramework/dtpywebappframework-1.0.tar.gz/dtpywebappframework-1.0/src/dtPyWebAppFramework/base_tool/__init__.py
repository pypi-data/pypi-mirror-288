from dtPyAppFramework.resources import ResourceManager
from dtPyAppFramework.settings import Settings
from ..managers.content_manager import ContentManager
from flask import Response


class AbstractTool(object):

    def __init__(self, flask_wrapper, resource_manager: ResourceManager, app_name, settings: Settings):
        super().__init__()
        self.app_name = app_name
        self.flask_wrapper = flask_wrapper
        self.settings: Settings = settings
        self.content_manager: ContentManager = ContentManager()
        self.resource_manager: ResourceManager = resource_manager
        self.add_custom_endpoints()

    def is_enabled(self):
        raise NotImplementedError

    def add_custom_endpoints(self):
        raise NotImplementedError

    def name(self):
        raise NotImplementedError

    def short_name(self):
        raise NotImplementedError

    def description(self):
        raise NotImplementedError

    def icon(self):
        raise NotImplementedError

    def tool_home_body_content(self):
        raise NotImplementedError

    def disabled_reason(self):
        raise NotImplementedError

    def tool_static_content(self, path):
        raise NotImplementedError

    def tool_home(self):
        return Response(self.content_manager.base_template().replace('{{CONTENT}}', self.tool_home_body_content())
                        .replace('{{APP_NAME}}', self.app_name), 200)

    def tool_disabled(self):
        return Response(self.content_manager.base_template().replace('{{CONTENT}}', self.content_manager.tool_disabled())
                        .replace('{{APP_NAME}}', self.app_name)
                        .replace('{{NAME}}', self.name())
                        .replace('{{REASON}}', self.disabled_reason()), 200)

    def error_message(self, friendly, detail):
        return Response(self.content_manager.base_template().replace('{{CONTENT}}', self.content_manager.error_card())
                        .replace('{{ERROR_FRIENDLY}}', friendly).replace('{{ERROR_DETAILS}}', detail)
                        .replace('{{APP_NAME}}', self.app_name), 500)

    def please_wait(self, task_id, message):
        return Response(self.content_manager.please_wait_template()
                        .replace('{{MESSAGE}}', message)
                        .replace('{{TASK_ID}}', task_id)
                        .replace('{{APP_NAME}}', self.app_name), 200)

    def add_endpoint(self, endpoint, endpoint_name, handler, methods=None):
        self.flask_wrapper.add_endpoint(endpoint=f'/{self.short_name()}{endpoint}',
                                        endpoint_name=f'{endpoint_name}',
                                        handler=handler, methods=methods)
