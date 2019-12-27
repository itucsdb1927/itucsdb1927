Developer Guide
===============

Project Structure
-----------------

Audiocasts rely on the **MVP (Model, View, Template)** paradigm.

The `models` package contains the custom base model implementation
and the models representing tables of the database.

The sub-packages under `routes` folder represents *Flask Blueprints*,
and each module implements a view with the same name as the module.

The `templates` folder contains the templates files. Folder structure
and file names mirror the `routes` folder, apart from the base files
extended by the other files, for clear structure and view-template pairing.

Other top level modules not provided in the base module include `proj_config.py`,
which fetches environment variables used for providing the database
and the secret keys. These values are then used for Flask configuration in `server.py`.

.. toctree::

   database_design
   code
