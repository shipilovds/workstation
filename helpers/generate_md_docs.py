#!/usr/bin/python

import re
import importlib
import sys
import os
from os.path import isfile, join
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from jinja2 import Environment, FileSystemLoader


MODULES_PATH = 'plugins/modules'
DOCS_PATH = 'docs'
TEMPLATE_FILE = 'helpers/docs_template.j2'
args = []


class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


def get_modules_list():
    """
    This fucntion helps to discover our modules
    Returns list of strings. Each string is a module name.
    """
    modules = []
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(curr_dir)
    sys.path.insert(0, parent_dir)  # from here: now we are moving to project`s root dir
    for module in os.listdir(MODULES_PATH):
        if isfile(join(MODULES_PATH, module)) and re.fullmatch(r'.*\.py', module):
            modules.append(module.split('.')[0])
    return modules


def import_var_as_yaml(module, var, yml):
    """
    Helps to get module by name and extract yaml documentation blocks
    Returns yaml obj.
    """
    modpath = "{}.{}".format(MODULES_PATH.replace('/', '.'), module)
    module_imported = importlib.import_module(modpath)
    content = getattr(module_imported, var)

    return yml.load(content)


def add_empty_line(string):
    """
    To make ansible tasks in 'examples' separated by empty line
    """
    return string.replace('\n- ', '\n\n- ')


templateLoader = FileSystemLoader(searchpath="./")
templateEnv = Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)

for module in get_modules_list():
    yml = MyYAML()  # Use round-trip settings. But now we need to pass it everywhere.
    module_documentation = import_var_as_yaml(module, 'DOCUMENTATION', yml)
    module_examples = import_var_as_yaml(module, 'EXAMPLES', yml)
    module_return = import_var_as_yaml(module, 'RETURN', yml)

    # Render examples as yaml text:
    module_examples_processed = yml.dump(module_examples, transform=add_empty_line)

    # Why don't we get namespace and collection name from galaxy config?:)
    with open('galaxy.yml', 'r') as data:
        galaxy = yml.load(data)
    full_module_name = '{}.{}.{}'.format(galaxy['namespace'], galaxy['name'], module)
    module_readme_file = '{}/{}.md'.format(DOCS_PATH, full_module_name)

    with open(module_readme_file, 'w') as readme:
        readme.write(template.render(
            full_module_name=full_module_name,
            documentation=module_documentation,
            doc_examples=module_examples_processed,
            doc_return=module_return
        ))
