# Super EasyPyPi

```
pip install super-easypypi
```

Then
```
$ supereasypypi my-package
```

Then to push to production repo.

```
$ my-package/build --push
```

And to push to test repo.

```
$ my-package/build --push --test
```

```
$ my-package/build --help
Build and push library to pypi index.

Usage:
    /home/q/work/temp/mypackage/build [OPTIONS] [EXTRA_ARGS]

All the EXTRA_ARGS are passed to twine. 
Credentials are in ~/.pypirc.

Options:
    --push      Push to pypi
    --test      Use test pypi
    --debug     Set bash 'x' option
    --help      Shows help message
```

To overwrite existing files use `-f` option. For interactive mode use `-i` option.

```
$ supereasypypi --help
usage: easypypi [-h] [-d DIR] [--replace-char REPLACE_CHAR] [-a AUTHOR] [-m AUTHOR_EMAIL] [-D DESCRIPTION] [-u HOME_PAGE_URL] [-U BUG_TRACKER_URL]
                [-k KEYWORDS] [-V PYTHON_VERSION_REQUIRED] [-t PYPI_TOKEN] [-T TESTPYPI_TOKEN] [-f] [-v] [-i]
                PACKAGE_NAME

Super EasyPyPi. Simple and easy to use tools for creating and publishing python packages.

positional arguments:
  PACKAGE_NAME          Package name you would like to appear in PyPi. Preferrably use dashes to separate words like "my-package". Undescores will be
                        replaced with dashes.

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Directory to create package in (default: /home/q/work/.temp/7)
  --replace-char REPLACE_CHAR
                        Make package directory name from provided PACKAGE_NAME parameter by replacing dashes to the specified value (default: "")
  -a AUTHOR, --author AUTHOR
                        Author (default: q)
  -m AUTHOR_EMAIL, --author-email AUTHOR_EMAIL
                        Author e-mail. (default: AUTHOR@example.com)
  -D DESCRIPTION, --description DESCRIPTION
                        Package short description (default: "")
  -u HOME_PAGE_URL, --home-page-url HOME_PAGE_URL
                        Package home page url. Provide your project's GitHub page e.g. (default: "https://example.com")
  -U BUG_TRACKER_URL, --bug-tracker-url BUG_TRACKER_URL
                        Package bug tracker url. Provide your project's GitHub issues page e.g. (default: "https://example.com")
  -k KEYWORDS, --keywords KEYWORDS
                        Package keywords. (default: "")
  -V PYTHON_VERSION_REQUIRED, --python-version-required PYTHON_VERSION_REQUIRED
                        Package required python version. (default: >=3.11)
  -t PYPI_TOKEN, --pypi-token PYPI_TOKEN
                        PyPi token. (default: "")
  -T TESTPYPI_TOKEN, --testpypi-token TESTPYPI_TOKEN
                        Test PyPi token. (default: "")
  -f, --force           Overwrite existing files. By default exits with error. (default: False)
  -v, --version         Prints EasyPyPi version.
  -i, --interactive     Use wizard like interactive mode to fill in fields.
```
