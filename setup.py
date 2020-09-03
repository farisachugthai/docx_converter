#!/usr/bin/env python
"""The setup script."""
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ["jinja2"]

setup_requirements = []

test_requirements = ["pytest"]

setup(
    name='docx_converter',
    author="Faris A Chugthai",
    author_email='farischugthai@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Convert an rst file and template to a docx file",
    entry_points={
        'console_scripts': [
            'convert=converter:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords=['jinja', 'templating', 'docx'],
    packages=find_packages(include=['src']),
    python_requires='>=3.5',
    setup_requires=setup_requirements,
    test_suite='test',
    tests_require=test_requirements,
    url='https://github.com/farisachugthai/json_sorter',
    version='0.1.0',
    zip_safe=False,
)
