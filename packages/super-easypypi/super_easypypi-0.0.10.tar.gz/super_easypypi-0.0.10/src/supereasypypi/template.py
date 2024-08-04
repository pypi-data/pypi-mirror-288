SETUP_CFG = '''
[metadata]
version = 0.0.1
name = {package_name}
author = {author}
author_email = {author_email}
description = {description}
long_description = file: README.md
long_description_content_type = text/markdown
url = {home_page_url}
project_urls =
    Bug Tracker = {bug_tracker_url}
classifiers =
    Programming Language :: Python :: 3
    Operating System :: OS Independent
license = MIT
keywords = {keywords}


[options]
package_dir =
    = src
packages = find:
python_requires = {python_requires}
install_requires = 

[options.packages.find]
where = src


[options.entry_points]
console_scripts = 
    {adapted_package_name} = {adapted_package_name}.cli:main
'''


VERSION = '0.0.1'


PROJECT_TOML = '''
[build-system]
requires = [
    "setuptools",
    "wheel"
]
build-backend = "setuptools.build_meta"
'''


BUILD = r'''
#!/usr/bin/env bash

SCRIPT_DIR=$(realpath "$(dirname "${{0}}")")
VENV_DIR=${{SCRIPT_DIR}}/.venv-build
POSITIONAL=()


usage() {{
cat << EOF
Build and push library to pypi index.

Usage:
    ${{0}} [OPTIONS] [EXTRA_ARGS]

All the EXTRA_ARGS are passed to twine. 
Credentials are in ~/.pypirc.

Options:
    --push      Push to pypi
    --test      Use test pypi
    --debug     Set bash 'x' option
    --help      Shows help message
EOF
}}

while [ "${{#}}" -gt 0 ]; do
    case "${{1}}" in
        -h|--help)
            usage
            exit
            ;;

        --test)
            USE_TEST_PYPI=1
            ;;

        --push)
            PUSH=1
            ;;

        --debug)
            set -x
            ;;

        *)
            POSITIONAL+=("${{1}}")
            ;;
    esac
    
   shift
done

set -eu

VERSION="$(cat ${{SCRIPT_DIR}}/VERSION)"
sed -E -i "s/version = [0-9]+\.[0-9]+\.[0-9]+/version = ${{VERSION}}/g" "${{SCRIPT_DIR}}/setup.cfg"
sed -E -i "s/__version__ = '[0-9]+\.[0-9]+\.[0-9]+'/__version__ = '${{VERSION}}'/g" "${{SCRIPT_DIR}}/src/{adapted_package_name}/__init__.py"

if [ -d "${{VENV_DIR}}" ]; then
    source "${{VENV_DIR}}/bin/activate"
else
    python3 -m venv "${{VENV_DIR}}" && \
    source "${{VENV_DIR}}/bin/activate" && \
    pip3 install build==0.10.0 twine==3.7.1
fi

rm -rf "${{SCRIPT_DIR}}/dist"
cd "${{SCRIPT_DIR}}"
python -m build

if [ -z "${{PUSH+x}}" ]; then
    exit 0
fi

if [ -n "${{USE_TEST_PYPI+x}}" ]; then
    echo -e "\033[0;33mUsing test repository\033[0m"
    twine upload --repository testpypi "${{SCRIPT_DIR}}/dist/*" "${{POSITIONAL[@]}}"
else
    echo -e "\033[0;33mUsing production repository\033[0m"
    twine upload "${{SCRIPT_DIR}}/dist/*" "${{POSITIONAL[@]}}"
fi
'''


LICENSE = '''
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


GITIGNORE = '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
.venv-build
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

.vscode
*~
.temp
examples
__pycache__
backup
.*
'''


ENV = '''
PYTHONPATH=./src
'''


CLI_PY = '''
# from {adapted_package_name}.whatever import Whatever

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import sys


def cli(args=sys.argv[1:]):
    parser = ArgumentParser(description='{adapted_package_name} desription goes here')
    parser.add_argument('--change-me', default='An option sample', required=False, 
        help='Just an option sample of your cli to be substituted by real ones')

    return parser.parse_args(args)


def main():
    args = cli()
    print('Package {package_name} created with EasyPyPi')


if __name__ == '__main__':
    main()
'''


MAIN_PY = '''
from {adapted_package_name}.cli import main


if __name__ == '__main__':
    main()
'''


INIT_PY = '''
__version__ = '0.0.1'
'''


REQUIREMENTS_TXT = '''
'''

README_MD = '''
# {package_name}


```
pip install {adapted_package_name}
```
'''


PYPIRC = '''
[pypi]
  username = __token__
  password = {pypi_token}
  
[testpypi]
  username = __token__
  password = {testpypi_token}
'''


import re, os


def extract_fields(tempate_str):
    field_names = re.findall(r'[^$]{(.*)}', tempate_str)
    return bool(field_names)


def files_list():
    return [
        dict(name='setup.cfg', fields=extract_fields(SETUP_CFG), template_str=SETUP_CFG, src=False),
        dict(name='VERSION', fields=extract_fields(VERSION), template_str=VERSION, src=False),
        dict(name='pyproject.toml', fields=extract_fields(PROJECT_TOML), template_str=PROJECT_TOML, src=False),
        dict(name='build', fields=extract_fields(BUILD), template_str=BUILD, src=False, exec=True),
        dict(name='LICENSE', fields=extract_fields(LICENSE), template_str=LICENSE, src=False),
        dict(name='README.md', fields=extract_fields(README_MD), template_str=README_MD, src=False),
        dict(name='.gitignore', fields=extract_fields(GITIGNORE), template_str=GITIGNORE, src=False),
        dict(name='.env', fields=extract_fields(ENV), template_str=ENV, src=False),
        dict(name='requirements.txt', fields=extract_fields(REQUIREMENTS_TXT), template_str=REQUIREMENTS_TXT, src=False),
        dict(name='cli.py', fields=extract_fields(CLI_PY), template_str=CLI_PY, src=True),
        dict(name='__main__.py', fields=extract_fields(MAIN_PY), template_str=MAIN_PY, src=True),
        dict(name='__init__.py', fields=extract_fields(INIT_PY), template_str=INIT_PY, src=True),
        dict(name='.pypirc', fields=extract_fields(PYPIRC), template_str=PYPIRC, path=os.environ['HOME']),
    ]    
