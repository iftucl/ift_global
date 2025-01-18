.. _readyaml-howto:

ReadConf: How to
==================

Rational
--------

YAML is a common way for storing local configurations for a script that might run in different environments.

As a common practice, within ift big data in quantitative finance, inside each script there must be a subfolder called ``properties``.
Inside the properties folder a YAML file shoudl be placed when is needed. The file namig conventions must follow this pattern:

- ``conf.yaml``

The ``conf.yaml`` file needs to be organised by environment (local, dev, prepord, prod).

.. codeblock:: yaml
    dev:
        database:
            postgres:
                url: localhost:9090
            mongodb:
                url: localhost:27017


How to use
----------

If the yaml file is structured in this way, the usage of ReadConfig will help in loading the config file.

.. ipython:: python
    
    from ift_global.utils.read_yaml import ReadConfig
    # ReadConfig("dev")