** ⚠️ This repository is archived and functionnalities have been moved to https://github.com/etalab/udata-gouvfr/ (now moved to https://github.com/etalab/udata-front).**

# udata-schema-gouvfr

This udata plugin provides an integration with [schema.data.gouv.fr](https://schema.data.gouv.fr)

## Features

- Adds a schema button to resources with a schema
- Displays a modal when clicking this button providing links to documentation and validation


## Usage

Install the plugin package in your udata environment:

```bash
pip install udata-schema-gouvfr
```

Then activate it in your `udata.cfg`:

```python
PLUGINS = ['schema-gouvfr']
```

## Configuration

You can control this plugin behavior with the following `udata.cfg` parameters:

- **`SCHEMA_GOUVFR_VALIDATA_URL`**: the URL to your [Validata](https://validata.fr/) instance (without trailing slash). **ex:** `https://validata.etalab.studio`
- **`SCHEMA_GOUVFR_IRVE_STABLE_RESOURCE_URL`**: the permalink to the consolidated [IRVE dataset](irve-dataset)'s latest resource. **ex:** `https://www.data.gouv.fr/fr/datasets/r/50625621-18bd-43cb-8fde-6b8c24bdabb3`

## Jobs

This plugin declares jobs.

- **`udata job run set-irve-schemas`**: sets the `schema` attribute of resources that are consolidated as part of [the national IRVE dataset](irve-dataset)


[irve-dataset]: https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/
