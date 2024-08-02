import platform
import invoke
from loguru import logger


def install_nightvision():
    """Install NightVision CLI."""
    # MacOS (Intel)
    if platform.system() == "Darwin" and platform.machine() == "x86_64":
        try:
            invoke.run(
                "curl -L https://downloads.nightvision.net/binaries/latest/nightvision_latest_darwin_amd64.tar.gz | tar -xz; mv nightvision /usr/local/bin/",
                hide=True)
            logger.info("nightvision installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install nightvision.")
            print(f"Error: {exc.result.stderr}")
    # MacOS (Apple Silicon)
    elif platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            invoke.run(
                "curl -L https://downloads.nightvision.net/binaries/latest/nightvision_latest_darwin_arm64.tar.gz -q | tar -xz; mv nightvision /usr/local/bin/",
                hide=True)
            logger.info("nightvision installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install nightvision.")
            print(f"Error: {exc.result.stderr}")
    # Linux (Intel)
    elif platform.system() == "Linux" and platform.machine() == "x86_64":
        try:
            invoke.run(
                "curl -L https://downloads.nightvision.net/binaries/latest/nightvision_latest_linux_amd64.tar.gz -q | tar -xz; sudo mv nightvision /usr/local/bin/",
                hide=True)
            logger.info("nightvision installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install nightvision.")
            print(f"Error: {exc.result.stderr}")
    # Linux (ARM)
    elif platform.system() == "Linux" and platform.machine() == "aarch64":
        try:
            invoke.run(
                "curl -L https://downloads.nightvision.net/binaries/latest/nightvision_latest_linux_arm64.tar.gz -q | tar -xz; sudo mv nightvision /usr/local/bin/",
                hide=True)
            logger.info("nightvision installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install nightvision.")
            print(f"Error: {exc.result.stderr}")
    # Windows (Intel)
    elif platform.system() == "Windows":
        raise NotImplementedError("Windows is not supported.")
