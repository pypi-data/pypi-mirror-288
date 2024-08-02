"""
Validate that prerequisites are installed.
"""
import platform

import invoke
from loguru import logger
from .prerequisite_utils import install_nightvision


class Prerequisites:
    def __init__(self, check_only: bool = False, force: bool = False):
        self.openapi_to_postman_installed: bool = False
        self.newman_installed: bool = False
        self.nightvision_installed: bool = False
        self.check_only = check_only
        self.force = force

    def validate_openapi_to_postman(self):
        """
        Validate that openapi-to-postman is installed.
        """
        logger.info("Validating that openapi-to-postman is installed...")
        try:
            invoke.run("openapi2postmanv2 --version", hide=True)
        except invoke.exceptions.UnexpectedExit:
            self.openapi_to_postman_installed = False
            logger.warning("openapi2postmanv2 is not installed.")

    def validate_newman(self):
        """
        Validate that newman is installed.
        """
        logger.info("Validating that newman is installed...")
        try:
            invoke.run("newman --version", hide=True)
        except invoke.exceptions.UnexpectedExit:
            self.newman_installed = False
            logger.warning("newman is not installed.")

    def validate_nightvision(self):
        """
        Validate that nightvision is installed.
        """
        logger.info("Validating that nightvision is installed...")
        try:
            invoke.run("nightvision --version", hide=True)
        except invoke.exceptions.UnexpectedExit:
            self.nightvision_installed = False
            logger.warning("nightvision is not installed.")

    @staticmethod
    def install_newman():
        """
        Install newman.
        """
        try:
            invoke.run("npm install -g 'newman@^6.0.0' 'newman-reporter-csv@^1.3.0'", hide=True)
            logger.info("newman installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install newman")
            print(f"Error: {exc.result.stderr}")

    @staticmethod
    def install_openapi_to_postman():
        """
        Install openapi-to-postman.
        """
        try:
            invoke.run("npm install -g openapi-to-postmanv2@^4.18.0", hide=True)
            logger.info("openapi-to-postmanv2 installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install openapi-to-postman.")
            print(f"Error: {exc.result.stderr}")

    @staticmethod
    def install_nightvision():
        """
        Install nightvision.
        """
        install_nightvision()

    @staticmethod
    def uninstall_openapi_to_postman():
        """
        Uninstall openapi-to-postman.
        """
        try:
            invoke.run("npm uninstall -g openapi-to-postmanv2", hide=True)
        except invoke.exceptions.UnexpectedExit:
            logger.critical("Failed to uninstall openapi-to-postman.")

    @staticmethod
    def uninstall_newman():
        """
        Uninstall newman.
        """
        try:
            invoke.run("npm uninstall -g newman", hide=True)
        except invoke.exceptions.UnexpectedExit:
            logger.critical("Failed to uninstall newman.")

    def validate(self):
        """
        Validate prerequisites.
        """
        self.validate_openapi_to_postman()
        self.validate_newman()

    def install(self):
        """
        Install prerequisites.
        """
        if not self.newman_installed or self.force:
            self.install_newman()
        if not self.openapi_to_postman_installed or self.force:
            self.install_openapi_to_postman()

    def uninstall(self):
        """
        Uninstall prerequisites.
        """
        self.uninstall_newman()
        self.uninstall_openapi_to_postman()
