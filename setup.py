# -*- coding: utf-8 -*-

# Import modules
from setuptools import find_packages, setup

with open('README.md', encoding='utf8') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements-dev.txt') as f:
    dev_requirements = f.read().splitlines()

setup(
    name='geomancer',
    version='1.0.0-alpha',
    description='Automated OSM Feature Engineering',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Thinking Machines Data Science',
    author_email='hello@thinkingmachin.es',
    url='https://github.com/thinkingmachines/geomancer',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    tests_require=dev_requirements,
    extras_require={'test': dev_requirements},
    license='GNU General Public License v3 (GPLv3)',
    zip_safe=False,
    keywords=['osm', 'python client', 'geospatial'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
    ],
)
