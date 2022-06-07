#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Denis Shipilov <shipilovds@gmail.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: gsettings
short_description: Gnome applications settings management
description:
  - Module to set gsettings options
version_added: "1.0.0"
options:
    schema:
        description:
          - The name of the schema for this Gsettings object
        required: true
        type: str
    path:
        description:
          - The path within the backend where the settings are
          - A valid path begins and ends with '/' and does not contain two consecutive '/' characters.
        required: False
        type: str
    key:
        description:
          - Gsettings schema key
        required: true
        type: str
    value:
        description:
          - Gsettings schema value
        required: true
        type: raw
author:
    - Denis Shipilov (@shipilovds)
'''

EXAMPLES = r'''
### simple usage:
- name: "Gsettings : Setup Schema"
  shipilovds.workstation.gsettings:
    schema: 'org.gnome.nautilus.preferences'
    key: 'default-folder-viewer'
    value: 'list-view'

### a little more complicated:
## tasks/main.yml:
- set_fact:
    gsettings:
      org.gnome.desktop.wm.keybindings:
        keys:
          switch-input-source: ['<Alt>Shift_L']
      org.gnome.desktop.input-sources:
        keys:
          sources: ['(xkb, us)', '(xkb, ru)']
      org.gtk.Settings.FileChooser:
        keys:
          location-mode: 'filename-entry'
          sort-directories-first: True
      org.gnome.desktop.notifications.application:
        path: '/org/gnome/desktop/notifications/application/org-gnome-software/'
        keys:
          enable: False

- name: Gsettings management
  include_tasks: gsettings.yml
  loop: "{{ env_gsettings | dict2items }}"
  loop_control:
    loop_var: _schema
    label: "{{ _schema.key }}"

## tasks/gsettings.yml:
- name: "Gsettings : Setup '{{ _schema.key }}'"
  shipilovds.workstation.gsettings:
    schema: "{{ _schema.key }}"
    path: "{{ _schema.value['path'] | default(omit) }}"
    key: "{{ item.key }}"
    value: "{{ item.value }}"
  loop: "{{ _schema.value['keys'] | dict2items }}"

'''

RETURN = r''' # '''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.shipilovds.workstation.plugins.module_utils.gsettings_helpers import GsettingsWrapper, ValueProcessor
import yaml


ARGS_SPEC = yaml.safe_load(DOCUMENTATION)['options']
CHECK_MOD = True


def main():
    module = AnsibleModule(argument_spec=ARGS_SPEC, supports_check_mode=CHECK_MOD)
    schema_id = module.params.get('schema')
    schema_key = module.params.get('key')
    schema_path = module.params.get('path')
    schema_eventual_value = ValueProcessor.process_unknown(module.params.get('value'))
    result = {'changed': False}
    try:
        gsettings = GsettingsWrapper(schema_id, schema_path, schema_key)
    except Exception as ex:
        module.fail_json(msg=str(ex), **result)
    if gsettings.value.unpack() != schema_eventual_value and not module.check_mode:
        try:
            gsettings.write(schema_eventual_value)
            result['changed'] = True
        except Exception as ex:
            module.fail_json(msg=str(ex), **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
