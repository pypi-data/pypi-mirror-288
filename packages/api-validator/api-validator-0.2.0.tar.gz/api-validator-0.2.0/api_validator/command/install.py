import click
from click_option_group import optgroup

from api_validator.tools.prerequisites import Prerequisites


@click.command("install", help="Install prerequisites.")
@optgroup.group("Installation Options", help="")
@optgroup.option("--check-only", "-c", is_flag=True, help="Only check if prerequisites are installed.")
@optgroup.option("--force", "-f", is_flag=True, help="Force install prerequisites.")
def install(check_only: bool, force: bool):
    """
    Install prerequisites.
    """
    run_install(check_only, force)


def run_install(check_only: bool, force: bool):
    prerequisites = Prerequisites(check_only=check_only, force=force)
    prerequisites.validate()
    if not check_only:
        prerequisites.install()