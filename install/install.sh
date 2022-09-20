#!/bin/bash

poetry install

# Jupyter extension config (see: ./binder/postBuild)
poetry run jupyter contrib nbextension install --user
poetry run jupyter nbextension enable --py widgetsnbextension
poetry run jupyter nbextensions_configurator enable --user