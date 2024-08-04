from supereasypypi import __version__
from supereasypypi.template import files_list

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os, sys
from pathlib import Path


class Color:
    off = '\033[0m'
    black = '\033[0;30m'
    red = '\033[0;31m'
    green = '\033[0;32m'
    yellow = '\033[0;33m'
    blue = '\033[0;34m'
    purple = '\033[0;35m'
    cyan = '\033[0;36m'
    white = '\033[0;37m'
    gray = '\x1b[90m'

c = Color


def cli(args=sys.argv[1:]):
    desc = 'Super EasyPyPi. Simple and easy to use tools for creating and publishing python packages.'

    parser = ArgumentParser(prog='supereasypypi', description=desc)
    parser.add_argument('-d', '--dir', default=os.environ.get('PWD', '.'), required=False, 
        help='Directory to create package in (default: %(default)s)')
    parser.add_argument('--replace-char', default='', required=False, 
        help='Make package directory name from provided PACKAGE_NAME parameter by replacing dashes to the specified value (default: "%(default)s")')
    parser.add_argument('-a', '--author', default=os.environ.get('USER', 'unknown'), required=False, 
        help='Author (default: %(default)s)')
    parser.add_argument('-m', '--author-email', default=None, required=False, 
        help='Author e-mail. (default: AUTHOR@example.com)')
    parser.add_argument('-D', '--description', default='', required=False, 
        help='Package short description (default: "%(default)s")')
    parser.add_argument('-u', '--home-page-url', default='https://example.com', required=False, 
        help='Package home page url. Provide your project\'s GitHub page e.g. (default: "%(default)s")')
    parser.add_argument('-U', '--bug-tracker-url', default='https://example.com', required=False, 
        help='Package bug tracker url. Provide your project\'s GitHub issues page e.g. (default: "%(default)s")')
    parser.add_argument('-k', '--keywords', default='', required=False, 
        help='Package keywords. (default: "%(default)s")')
    parser.add_argument('-V', '--python-version-required', default='>='+'.'.join([str(v) for v in sys.version_info][:2]), required=False, 
        help='Package required python version. (default: %(default)s)')
    parser.add_argument('-t', '--pypi-token', default='', required=False, 
        help='PyPi token. (default: "%(default)s")')
    parser.add_argument('-T', '--testpypi-token', default='', required=False, 
        help='Test PyPi token. (default: "%(default)s")')
    parser.add_argument('-f', '--force', default=False, required=False, action='store_true',
        help='Overwrite existing files. By default exits with error. (default: %(default)s)')
    parser.add_argument('-i', '--interactive', action='store_true', 
        help='Use wizard like interactive mode to fill in fields.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}', 
        help='Prints EasyPyPi version.')

    parser.add_argument('package_name', metavar='PACKAGE_NAME', help='Package name you would like to appear in PyPi. ' 
        'Preferrably use dashes to separate words like "my-package". Undescores will be replaced with dashes.')

    return parser.parse_args(args)


def settle_files(project_path, src_path, vars, force):
    src_path.mkdir(parents=True, exist_ok=True)

    for file_meta in files_list():
        if 'src' in file_meta:
            path = src_path if file_meta['src'] else project_path
        else:
            path = Path(file_meta['path'])

        fn = file_meta['name']
        full_fn = path.joinpath(fn)
        if full_fn.exists():
            if fn == '.pypirc':
                print(f'{c.yellow}Warning: {c.white}File exists [{full_fn}]. We don\'t overwrite it{c.off}')
                continue
            elif not force:
                raise FileExistsError(f'File exists [{full_fn}]. Use -f option to overwrite')

        with open(full_fn, 'w') as f:
            template_str = file_meta['template_str']
            f.write(template_str.format(**vars) if file_meta['fields'] else template_str) 

        if 'exec' in file_meta:
            full_fn.chmod(0o755)


def clear_line():
    print('\x1b[K')


def input_field(field_name, fields):
    label = field_name.replace('_', ' ').capitalize()
    return input(f'{c.cyan}{label} {c.white}({c.gray}{fields[field_name]}{c.white}) {c.cyan}>{c.off}')


def interactive(fields):
    field_names = [
        'package_name', 
        'home_page_url', 
        'bug_tracker_url', 
        'pypi_token', 
        'testpypi_token',
        'author', 
        'author_email', 
        'keywords', 
        'description', 
        'python_requires'
    ]

    print('\x1b[2J\x1b[H')
    print(f'{c.white}Default values are in the parentheses and used if empty value is specified.\n'
           'Tokens are needed to succesfully push to PyPi.\n')
    for field_name in field_names:
        value = input_field(field_name, fields)
        if value:
            fields[field_name] = value

    return fields


def print_hint(text):
    print(f'{c.blue}Hint: {c.white}{text}{c.off}')


def main():
    def norm_package_name(name):
        return name.replace('_', '-').replace(' ', '-').lower()

    args = cli()
    args.dir = Path(args.dir)
    args.package_name = norm_package_name(args.package_name)

    fields = vars(args) | dict(
                                python_requires=args.python_version_required,
                                author_email=f'{args.author}@example.com' if args.author_email is None else args.author_email
    )

    if args.interactive:
        interactive(fields)

    package_name = norm_package_name(fields['package_name'])
    fields |= dict(
        package_name = package_name,
        adapted_package_name=package_name.replace('-', args.replace_char)
    )

    project_path = args.dir.joinpath(fields['package_name'])
    src_path = project_path.joinpath(f'src/{fields["adapted_package_name"]}')

    try:
        settle_files(project_path, src_path, fields, args.force)
        print_hint(f"Now '{package_name}/build --push' to build and push to PyPi")
        print_hint(f"If necessary to change package version use 'VERSION' file")
        print_hint(f'If token is valid but 403 error appears maybe package name conflicts with an existing one in PyPi')
    except FileExistsError as e:
        print(f'{c.red}Error: {c.white}{e}{c.off}')


if __name__ == '__main__':
    main()