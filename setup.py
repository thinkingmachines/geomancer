# -*- coding: utf-8 -*-

# Import modules
from setuptools import find_packages, setup

with open("README.md", encoding="utf8") as readme_file:
    readme = readme_file.read()

# Packages for installation
common = ["numpy", "pandas", "loguru", "sqlalchemy", "geoalchemy2", "pytz"]
test_requirements = ["pytest==3.6.4", "pytest-cov", "flake8==3.5.0", "tox"]

# Warehouse-specific installations
extras = {
    "bq": ["google-cloud-bigquery[pandas,pyarrow]", "pybigquery"],
    "sqlite": [],
    "psql": [],
}

# `pip install geomancer` will install everything
requirements = common + extras["bq"] + extras["sqlite"] + extras["psql"]

setup(
    name="geomancer",
    version="1.0.0",
    description="Automated Geospatial Feature Engineering Library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Thinking Machines Data Science",
    author_email="hello@thinkingmachin.es",
    url="https://github.com/thinkingmachines/geomancer",
    packages=find_packages(exclude=["docs", "tests"]),
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    extras_require=extras,
    dependency_links=[
        "git://github.com/thinkingmachines/pybigquery.git@gis#egg=pybigquery"
    ],
    license="MIT license",
    zip_safe=False,
    keywords=[
        "osm",
        "python client",
        "geospatial",
        "bigquery",
        "machine learning",
        "feature engineering",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
    ],
    test_suite="tests",
)
