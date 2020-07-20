# udata-schema

This udata plugin provides an integration with [schema.data.gouv.fr](https://schema.data.gouv.fr)

## Features

- Adds a schema button to resources with a schema
- Displays a modal when clicking this button providing links to documentation and validation


## Usage

Install the plugin package in you udata environement:

```bash
pip install udata-schema
```

Then activate it in your `udata.cfg`:

```python
PLUGINS = ['schema']
```
