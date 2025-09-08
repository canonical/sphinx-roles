# sphinx-roles

`sphinx-roles` houses the `literalref`, `spellexception`, and `none` roles.

## Basic usage

### literalref

To add a monospaced reference to your document, pass the target or URL to the
`literalref` role:

```
:literalref:`link text <ref-target>`

:literalref:`link text <https://example.com>`
```

### spellexception

To exempt a string from spell checking, wrap it in the `spellexception` role:

```
:spellexception:`Lorem ipsum`
```

### none

To prevent a string from being rendered in the document, wrap it in the `none` role:

```
:none:`This text isn't rendered.`
```

## Project setup

sphinx-roles is published on PyPI and can be installed with:

```bash
pip install sphinx-roles
```

After adding sphinx-roles to your Python project, update your Sphinx's `conf.py`
file to include `sphinx_roles` as an extension:

```python
extensions = [
    "sphinx_roles"
]
```

## Community and support

You can report any issues or bugs on the project's [GitHub
repository](https://github.com/canonical/sphinx-roles).

sphinx-roles is covered by the [Ubuntu Code of
Conduct](https://ubuntu.com/community/ethos/code-of-conduct).

## License and copyright

sphinx-roles is released under the [GPL-3.0 license](LICENSE).

© 2025 Canonical Ltd.
