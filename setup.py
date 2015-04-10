#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import subprocess
from setuptools import setup

setup(
    name='pdnsnexus',
    packages=['pdnsnexus', 'pdnsnexus.cli'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'flask_oauthlib', 'requests', 'gunicorn'],
    entry_points={
        'console_scripts': [
            'pdnsnexusd = pdnsnexus.cli.server:run',
            'nxs_ctl = pdnsnexus.cli.manager:run',
        ]
    },
)
