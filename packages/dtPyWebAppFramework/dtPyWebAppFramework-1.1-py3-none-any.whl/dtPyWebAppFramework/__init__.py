import os
import sys
import yaml
import time
import logging
import webbrowser

from argparse import ArgumentParser
from threading import Thread

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.resources import ResourceManager

from .flask import FlaskAppWrapper
from .managers.content_manager import ContentManager
from .managers.tool_manager import ToolManager

dir_path = os.path.dirname(os.path.realpath(__file__))

# Define module-level variables with version-related information
with open(os.path.join(dir_path, 'version.dat'), 'r') as _version:
    __version__ = _version.read()


# Function to retrieve the version
def version():
    """Returns the version of the module."""
    return __version__


class WebApp(AbstractApp):
    app_module_directory = "./app"
    definition_file = os.path.abspath(f"{app_module_directory}/app_definition.yaml")

    def __init__(self) -> None:
        if not os.path.exists(self.definition_file):
            raise NotImplementedError(f'No Application Definition Found "{self.definition_file}".')

        sys.path.append(os.path.abspath(self.app_module_directory))
        with open(self.definition_file, 'r', encoding='UTF-8') as file:
            self.app_definition = yaml.safe_load(file)

        super().__init__(description=self.app_definition.get('description'),
                         version=self.app_definition.get('version'),
                         short_name=self.app_definition.get('short_name'),
                         full_name=self.app_definition.get('full_name'),
                         console_app=os.environ.get("DEV_MODE", None) is not None)

        self.flask_app: FlaskAppWrapper = None
        self.settings: Settings = None
        self.resource_manager: ResourceManager = None
        self.content_manager: ContentManager = None
        self.tool_manager: ContentManager = None

    def define_args(self, arg_parser: ArgumentParser):
        arg_parser.add_argument('--dev_mode', action='store_true', required=False, help='Run in Dev Mode')

    def _open_home_page(self):
        home_url = f"http://{self.flask_app.web_server_host}:{self.flask_app.web_server_port}/"
        webbrowser.open(home_url, new=0, autoraise=True)
        logging.info(f'Web Toolkit available on: {home_url}')

    def main(self, args):
        self.settings = Settings()
        self.resource_manager = ResourceManager()
        self.flask_app = FlaskAppWrapper(self.app_spec['short_name'], settings=self.settings)
        self.resource_manager.add_resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources"))

        custom_resource_path = os.path.abspath(f"{self.app_module_directory}/resources")
        if os.path.exists(custom_resource_path):
            logging.info(f'Adding custom application resource path: "{custom_resource_path}"')
            self.resource_manager.add_resource_path(custom_resource_path)

        self.tool_manager = ToolManager(resource_manager=self.resource_manager,
                                        settings=self.settings,
                                        app_definition=self.app_definition,
                                        flask_app=self.flask_app, dev_mode=args.dev_mode)
        self.content_manager = ContentManager(resource_manager=self.resource_manager,
                                              settings=self.settings,
                                              app_definition=self.app_definition, flask_app=self.flask_app,
                                              tool_manager=self.tool_manager)

        self.tool_manager.load_tools()

        self.flask_app.add_endpoint(endpoint='/', endpoint_name='home', handler=self.content_manager.home)
        self.flask_app.add_endpoint(endpoint='/exit', endpoint_name='exit', handler=self.exit)
        self.flask_app.add_endpoint(endpoint='/assets/<path:path>', endpoint_name='assets', handler=self.content_manager.assets)
        self.flask_app.start()
        self._open_home_page()

    @staticmethod
    def close_app():
        time.sleep(2)
        logging.info("Closing app at user's request")
        os._exit(0)

    def exit(self):
        thread = Thread(target=self.close_app)
        thread.start()
        return flask.Response(self.content_manager.exit(), 200)


def start():
    WebApp().run()
