"""
Generate an OpenAPI spec by analyzing code using NightVision.
"""

import click


@click.command("generate", help="Generate an OpenAPI spec by analyzing code using NightVision.")
def generate():
    run_generate()


def run_generate():
    raise NotImplementedError("This command is not implemented yet.")
