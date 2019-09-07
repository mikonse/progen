import pathlib

import click

from templates import Template


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument('type', type=str)
@click.argument('name', type=str)
@click.option('--template-dir', help='Base dir where to search for templates')
@click.option('--dest', help='Destination path where to bootstrap the template')
def cli(ctx, type: str, name: str, template_dir, dest):
    if ctx.invoked_subcommand is not None:
        return

    if template_dir is not None:
        base_dir = pathlib.Path(template_dir)
    else:
        # relative path to module install
        base_dir = pathlib.Path(__file__).resolve().parents[1] / 'templates'

    if dest is None:
        dest = pathlib.Path.cwd() / name
    else:
        dest = pathlib.Path(dest)

    template = Template(base_dir / type / name)
    template.render(dest)


@cli.command()
@click.argument('name')
def generate_template(name):
    pass


@cli.command()
@click.argument('name')
@click.option('--url', default='https://github.com/')
def get_template(name, url):
    pass


if __name__ == '__main__':
    cli()
