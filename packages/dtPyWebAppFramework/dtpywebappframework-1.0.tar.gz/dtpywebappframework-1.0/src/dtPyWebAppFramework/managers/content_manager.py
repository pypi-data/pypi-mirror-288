from dtPyAppFramework.decorators import singleton
from dtPyAppFramework.resources import ResourceManager
from dtPyAppFramework.settings import Settings

from flask import send_from_directory, Response

import logging
import os


@singleton()
class ContentManager:

    def __init__(self, resource_manager: ResourceManager, settings: Settings, app_definition: dict,
                 flask_app, tool_manager):
        self.resource_manager = resource_manager
        self.settings = settings
        self.app_definition: dict = app_definition
        self.flask_app = flask_app
        self.tool_manager = tool_manager

    def _base_replacements(self, content: str):
        return (((content.replace("{{APP_NAME}}", f"{self.app_definition.get('full_name')}, "
                                                  f"Version: {self.app_definition.get('version')}")
                  .replace("{{FRAMEWORK_COPYRIGHT}}", "© Framework Copyright 2023-2024 Digital-Thought - All Rights Reserved")
                  .replace("{{TOOLS_COPYRIGHT}}", f"© Tool Copyright {self.app_definition.get('copyright', '')}"))
                 .replace("{{BANNER_BACKGROUND}}", self.app_definition.get('banner_background_color', "#060d39")))
                .replace("{{LOGO}}", self.app_definition.get('logo', "/assets/images/logo.png"))
                .replace("{{BANNER_FONT_COLOR}}", self.app_definition.get('banner_font_color', "#ffffff")))

    def base_template(self):
        with open(self.resource_manager.get_resource_path('base_template.html'), mode='r') as base_template:
            return self._base_replacements(base_template.read())

    def please_wait_template(self):
        with open(self.resource_manager.get_resource_path('please_wait_template.html'), mode='r') as base_template:
            return self._base_replacements(base_template.read())

    def error_card(self):
        with open(self.resource_manager.get_resource_path('error_card.html'), mode='r') as base_template:
            return self._base_replacements(base_template.read())

    def tool_disabled(self):
        with open(self.resource_manager.get_resource_path('tool_disabled.html'), mode='r') as base_template:
            return self._base_replacements(base_template.read())

    def home(self):
        resource_path = self.resource_manager.get_resource_path("home.html")
        logging.info(f"Rendering: {resource_path}")
        with open(f'{resource_path}', mode='r') as html:
            content = self._base_replacements(html.read())

            tool_card = []
            for tool in self.tool_manager.tools:
                if tool.is_enabled():
                    card_resource_path = self.resource_manager.get_resource_path("card.html")
                else:
                    card_resource_path = self.resource_manager.get_resource_path("disabled_card.html")
                with open(f'{card_resource_path}', mode='r') as card:
                    card_content = card.read().replace('{{NAME}}', tool.name()) \
                        .replace('{{DESCRIPTION}}', tool.description()) \
                        .replace('{{ICON}}', f'mobi-mbri-{tool.icon()}') \
                        .replace('{{TOOL_HREF}}', f'/{tool.short_name()}')

                    tool_card.append(card_content)

            card_content = '<div class="row">'
            count = 0
            for card in tool_card:
                card_content = card_content + card
                count += 1

                if count == 3:
                    card_content = card_content + '</div>'
                    count = 0
            card_content = card_content + '</div>'
            content = content.replace('{{CARDS}}', card_content)

            return Response(content, 200)

    def assets(self, path):
        for resource_path in self.resource_manager.resource_paths:
            if os.path.exists(os.path.join(resource_path, "assets", path)):
                logging.info(f"Rendering: {resource_path}/assets/{path}")
                return send_from_directory(f'{resource_path}/assets', path)

    def exit(self):
        resource_path = self.resource_manager.get_resource_path("exit.html")
        logging.info(f"Rendering: {resource_path}")
        with open(f'{resource_path}', mode='r') as html:
            return self._base_replacements(html.read())
