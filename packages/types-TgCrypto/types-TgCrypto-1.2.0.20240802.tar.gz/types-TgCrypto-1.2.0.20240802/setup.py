from setuptools import setup

name = "types-TgCrypto"
description = "Typing stubs for TgCrypto"
long_description = '''
## Typing stubs for TgCrypto

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`TgCrypto`](https://github.com/pyrogram/tgcrypto) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`TgCrypto`.

This version of `types-TgCrypto` aims to provide accurate annotations
for `TgCrypto==1.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/TgCrypto. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`17af88919f23b909f7e87eb6bd0877c383c9227d`](https://github.com/python/typeshed/commit/17af88919f23b909f7e87eb6bd0877c383c9227d) and was tested
with mypy 1.10.1, pyright 1.1.374, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="1.2.0.20240802",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/TgCrypto.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['tgcrypto-stubs'],
      package_data={'tgcrypto-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
