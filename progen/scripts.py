import pathlib

import click

from templates import Template


@click.command()
@click.argument('type', type=str)
@click.argument('name', type=str)
@click.option('--template-dir', help='Base dir where to search for templates')
@click.option('--dest', help='Destination path where to bootstrap the template')
def cli(type: str, name: str, template_dir, dest):
    if template_dir is not None:
        base_dir = pathlib.Path(template_dir)
    else:
        base_dir = pathlib.Path(__file__).resolve().parents[1] / 'templates'

    if dest is None:
        dest = pathlib.Path.cwd() / name
    else:
        dest = pathlib.Path(dest)

    template = Template(base_dir / type / name)
    template.prompt_vars()
    template.render(dest)


if __name__ == '__main__':
    cli()
