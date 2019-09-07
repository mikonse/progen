from pathlib import Path
from typing import Dict, List, Optional

from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from jinja2 import Environment, FileSystemLoader
import click


class NotInitializedError(Exception):
    pass


class InvalidConfigError(Exception):
    pass


class TemplateConfig:
    def __init__(self, template_path: Path):
        self.template_path = template_path
        if not self.template_path.exists() or not (self.template_path / 'config.yml').exists():
            raise FileNotFoundError(f'Invalid template path: "{self.template_path}"')

        with (self.template_path / 'config.yml').open('r') as config_file:
            self._config = load(config_file, Loader=Loader)

        if not self.validate():
            raise InvalidConfigError(f'Invalid config file')

    def files(self) -> List:
        return self._config.get('files', [])

    def validate(self) -> bool:
        for f in self._config.get('files', []):
            if not (self.template_path / f).exists():
                return False
        if not self._validate_params(self._config.get('params', {})):
            return False

        return True

    def _validate_params(self, params: List) -> bool:
        for param in params:
            if not all(k in param for k in ('name', 'prompt')):
                return False
            if param.get('type', 'str') == 'group':
                if isinstance(param.get('subfields', []), list) or not self._validate_params(param.get('subfields')):
                    return False
        return True

    def prompt_params(self) -> Dict:
        return self._prompt_params(self._config.get('params', {}))

    def _prompt_params(self, params: List) -> Dict:
        result = {}
        for param in params:
            if param.get('type', 'str') == 'group':
                click.echo(param.get('prompt'))
                result[param.get('name')] = self._prompt_params(param.get('subfields'))
            else:
                result[param.get('name')] = click.prompt(param.get('prompt'))
        return result


class Template:
    def __init__(self, file_path: Path, params: Optional[Dict] = None):
        self.file_path = file_path

        self.env = Environment(
            loader=FileSystemLoader(str(self.file_path))
        )

        self.config = TemplateConfig(self.file_path)
        if not params:
            self._params = self.config.prompt_params()
        else:
            self._params = params

    @property
    def params(self) -> Dict:
        return self._params

    @params.setter
    def params(self, val: Dict):
        # TODO: sanity checking of params defined in config.yaml
        self._params = val

    def render(self, dest: Path):
        if self.params is None:
            raise NotInitializedError('Template variables not initialized yet')

        for f in self.config.files():
            self._render_template(dest, f)

    def _render_template(self, dest: Path, name: str) -> None:
        t = self.env.get_template(name).render(**self.params)
        dest.mkdir(parents=True, exist_ok=True)
        f = dest / name
        f.touch()
        f.write_text(t)


if __name__ == '__main__':
    t = Template(Path.cwd().parent / 'templates' / 'latex' / 'letter')
    t.render(Path.cwd().parent)
