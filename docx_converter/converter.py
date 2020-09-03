#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert a md file to a docx.

Overview
--------
Jinja or cookiecutter {or something to the like} will easily generate a
plaintext file based on slugs and responses given by the user.

As both jinja and cookiecutter are python projects, we utilize a python
file to fully expose the API.

Then we can use pandoc in a subprocess to convert it to a docx or a pdf
that's ready to use for customers.

The ultimate goal is that with a minimal number of questions we can effectively
template out business proposals.

.. compound::

    These are brainstorming ideas and may not be representative of what actually
    needs to be done.

    - Decide whether we use md or rst.
    - Worst case bundle pandoc with this so that nobody has weird downloads they need to do.
    - Make a GUI with QT and have them fill out a form
        - Have that GUI include a file explorer so they can pick new templates

.. warning::

    This requires python3 specifically. It will crash immediately with python2 which I believe mac is bundled with.

"""
import json
import logging
import os
import shutil
import subprocess
# import sys

from collections import OrderedDict
from pathlib import Path

import jinja2
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError, UndefinedError


logging.basicConfig(level=logging.WARNING)


def test_pandoc_installation():
    try:
        ret = subprocess.run(['pandoc'], timeout=10)
        # , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.SubprocessError:
        print("Pandoc must be installed!")
        raise

    if ret.returncode != 0:
        print("Running pandoc in a subshell didn't work.")


def convert_using_template(template):
    """Take an rst file, ``template``, and convert to docx."""
    template = Path(template).resolve()
    if not template.exists():
        raise FileNotFoundError
    return subprocess.run(['pandoc', '-t', 'docx', template.stem + '.rst', '-o', template.stem + '.docx', '--reference-doc=./custom_reference.docx'], shell=True)


def load_default_options(options_file='cookiecutter.json'):
    context = OrderedDict()
    try:
        with open(options_file) as f:
            obj = json.load(f, object_pairs_hook=OrderedDict)
    except ValueError as e:
        # JSON decoding error
        logging.error(
            "JSON decoding error while loaded %s."
            "Error was: \n%s", (Path(options_file), e))
        return

    context[options_file] = obj
    logging.debug('Options generated. %s', context)
    return obj


def generate_rst(infile, context, env):
    """Convert the preferred options to an rst file with all jinja slugs converted.

    Options are generated in cookiecutter.json and eventually will be
    created from user provided arguments on the CLI.

    Hopefully after that options will be provided in a GUI.

    Parameters
    ----------
    infile : Path
        Input file to generate the file from.
    context : OrderedDict
        Dict for populating the cookiecutter variables.
    env : jinja2.Environment
        Jinja2 template execution environment.

    """
    logging.debug("Processing file %s", infile)
    outfile_tmpl = env.from_string(infile)
    outfile = outfile_tmpl.render(**context)
    logging.debug("Created file at %s", outfile)

    # Force fwd slashes on Windows. This is a by-design bug in Jinja
    infile_corrected = infile.replace(os.path.sep, '/')

    try:
        tmpl = env.get_template(infile_corrected)
    except TemplateSyntaxError as e:
        # Disable this so that traceback is verbose
        e.translated = False
        raise

    rendered_file = tmpl.render(**context)

    with open(outfile + ".generated.rst", 'w') as f:
        f.write(rendered_file)

    # apply file permissions to output file
    shutil.copymode(infile, outfile)


loader = FileSystemLoader('.')
env = jinja2.Environment(loader=loader)
generate_rst("todo.rst", context=load_default_options(), env=env)
