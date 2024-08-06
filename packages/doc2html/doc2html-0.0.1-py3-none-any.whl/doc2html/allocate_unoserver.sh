#!/bin/bash

if [ ! -d "environments" ]; then
    mkdir environments
    echo "Created 'environments' directory."

    virtualenv --python=/usr/bin/python3 --system-site-packages environments/virtenv
    echo "Allocated system packages"

    ./environments/virtenv/bin/pip install unoserver
    echo "Unoserver has been installed in the local environment"
else
    echo "    'environments' directory already exists.
    This typically means that the environment for unoserver has been allocated already."
fi
