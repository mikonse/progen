from pathlib import Path
from typing import Dict

from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from jinja2 import Environment, FileSystemLoader
import click


class NotInitializedError(Exception):
    pass


class Template:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        if not self.file_path.exists() or not (self.file_path / 'config.yml').exists():
            raise FileNotFoundError(f'Invalid template path: "{file_path}"')

        self.env = Environment(
            loader=FileSystemLoader(str(self.file_path))
        )

        with (self.file_path / 'config.yml').open('r') as config_file:
            self.config = load(config_file, Loader=Loader)

        self._vars = None

    @property
    def vars(self) -> Dict:
        return self._vars

    @vars.setter
    def vars(self, val: Dict):
        # TODO: sanity checking of vals defined in config.yaml
        self._vars = val

    @classmethod
    def _prompt_vars(cls, params: Dict) -> Dict:
        result = {}
        for param_name, prompt in params.items():
            if isinstance(prompt, dict):
                result[param_name] = cls._prompt_vars(prompt)
            else:
                result[param_name] = click.prompt(prompt)
        return result

    def prompt_vars(self) -> Dict:
        self.vars = self._prompt_vars(self.config.get('params', {}))
        return self.vars

    def render(self, dest: Path):
        if self.vars is None:
            raise NotInitializedError('Template variables not initialized yet')

        for f in self.config['files']:
            self._render_template(dest, f)

    def _render_template(self, dest: Path, name: str) -> None:
        t = self.env.get_template(name).render(**self.vars)
        dest.mkdir(parents=True, exist_ok=True)
        f = dest / name
        f.touch()
        f.write_text(t)


if __name__ == '__main__':
    t = Template(Path.cwd().parent / 'templates' / 'latex' / 'letter')
    t.prompt_vars()
    t.render(Path.cwd().parent)
