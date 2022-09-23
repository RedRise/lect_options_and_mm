# #!/bin/bash

# if ! [ -x "$(command -v dot)" ]; then
#   echo 'Installing graphviz.' >&2
#   apt install graphviz
# fi


if ! [ -x "$(command -v poetry)" ]; then
  echo 'Installing poetry.' >&2
  curl -sSL https://install.python-poetry.org | python3 -
  printf 'export PATH="$PATH:/home/gitpod/.local/bin"' >> $HOME/.bashrc
  source $HOME/.bashrc
fi

if ! [ -x "$(command -v poetry)" ]; then
  echo "Poetry is not installed. abort"
  exit 0
fi


# Install package dependencies
poetry install

# Jupyter extension config (see: ./binder/postBuild)
poetry run jupyter contrib nbextension install --user
poetry run jupyter nbextension enable --py widgetsnbextension
poetry run jupyter nbextensions_configurator enable --user



