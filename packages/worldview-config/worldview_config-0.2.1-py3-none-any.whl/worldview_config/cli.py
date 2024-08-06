import logging
from pathlib import Path

import typer
from typing_extensions import Annotated

from worldview_config import models
from worldview_config.merge import merge_config
from worldview_config.render import render_templates

app = typer.Typer(add_completion=False, no_args_is_help=True)
state = {"verbose": False}


@app.callback()
def main(verbose: bool = False):
    """
    Commands for working with worldview configuration.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)0.1s %(asctime)s -- %(message)s",
    )
    if verbose:
        state["verbose"] = True


@app.command(no_args_is_help=True)
def merge(
    new_root: Annotated[
        Path,
        typer.Argument(
            help="""Root directory of the new configuration that
you wish to merge.""",
        ),
    ],
    target_root: Annotated[
        Path,
        typer.Argument(
            help="""Root directory of the existing configuration.""",
        ),
    ],
):
    """Merge one set of config files into another."""
    merge_config(new_root=new_root, target_root=target_root)


@app.command(no_args_is_help=True)
def render(
    layer_config: Annotated[
        Path,
        typer.Argument(
            help="A JSON file containing layer configuration.",
        ),
    ],
    target: Annotated[
        Path,
        typer.Option(
            help="target path to render the templates into.",
        ),
    ] = Path.cwd(),
):
    """Render templates from a layer configuration file."""
    with open(layer_config) as fp:
        layers = models.LayerConfigs.model_validate_json(fp.read())
    render_templates(target=target, layers=layers)
