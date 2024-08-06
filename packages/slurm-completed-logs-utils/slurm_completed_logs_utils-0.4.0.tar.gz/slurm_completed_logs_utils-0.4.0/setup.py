#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "Rich",
    "pydantic",
    "PyYAML",
]

test_requirements = []

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of utilities for parsing the SLURM Completed Logs file.",
    entry_points={
        'console_scripts': [
            'slurm-log-to-sqlite=slurm_completed_logs_utils.completed_log_to_sqlite:main',
            # 'insert-lines=slurm_completed_logs_utils.insert_lines:main',
            # 'make-substitutions=slurm_completed_logs_utils.make_substitutions:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='slurm_completed_logs_utils',
    name='slurm_completed_logs_utils',
    packages=find_packages(include=['slurm_completed_logs_utils', 'slurm_completed_logs_utils.*']),
    package_data={
        "slurm_completed_logs_utils": [
            "conf/config.yaml",
            "sqlite/*",
            ]
        },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/slurm-completed-logs-utils',
    version='0.4.0',
    zip_safe=False,
)
