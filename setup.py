#!/usr/bin/env python
import os
import yaml
import re
from setuptools import setup
from setuptools.command.build_py import build_py
from shutil import copyfile

# Let's load some data from galaxy.yml to avoid duplication
with open('galaxy.yml', 'r') as data:
    galaxy = yaml.safe_load(data)

collection_path = f"ansible_collections/{galaxy['namespace']}/{galaxy['name']}"
long_description = open(galaxy['readme'], 'r').read()

extra_files = [
    'galaxy.yml',  # To avoid warnings from ansible-galaxy (cannot detect version)
    'README.md'
]

py_files = [
    collection_path + '/plugins/module_utils/gsettings_helpers',
    collection_path + '/plugins/modules/gnome_extension',
    collection_path + '/plugins/modules/gsettings'
]


def get_emails(authors_list):
    pattern = r'<(\S+@\S+\.\S+)>'
    emails = []
    for author in authors_list:
        email = re.findall(pattern, author)
        emails.extend(email)

    return ', '.join(emails)


class BuildCommand(build_py):
    def run(self):
        build_py.run(self)

        if not self.dry_run:
            current_dir = os.path.abspath(os.path.dirname(__file__))
            target_dir = os.path.join(self.build_lib, collection_path)
            for file_name in extra_files:
                copyfile(os.path.join(current_dir, file_name), os.path.join(target_dir, file_name))


setup(
    name=f"ansible-modules-{galaxy['namespace']}-{galaxy['name']}",
    version=galaxy['version'],
    description=galaxy['description'],
    author=", ".join(galaxy['authors']),
    author_email=get_emails(galaxy['authors']),
    url=galaxy['homepage'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=py_files,
    cmdclass={"build_py": BuildCommand},
    install_requires=[
        'ansible-core>=2.12.0',
    ],
    license='GPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Ansible',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration'
    ],
    project_urls={
        'Source Code': galaxy['repository'],
        'Documentation': galaxy['documentation'],
        'Bug Tracker': galaxy['issues']
    }
)
