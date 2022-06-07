#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Denis Shipilov <shipilovds@gmail.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: gnome_extension
short_description: Gnome shell extensions management
description:
  - This module can install or enable/disable gnome shell extensions
  - You can install and then enable module by one task (use both arguments)
  - You need to reload Gnome Session to make extension enabled.
version_added: '1.0.0'
options:
    name:
        description:
          - Extension name (uuid)
        required: true
        type: str
    state:
        description:
          - State of installation in the system
        required: false
        type: str
        choices: [ present, absent ]
        default: present
    enabled:
        description:
          - Enable module when true / disable when false
          - Changes nothing if not set
        required: false
        type: bool
    src:
        description:
          - Module file path or URL (to zip file)
        required: false
        type: path
    force:
        description:
          - Force module installation
        required: false
        type: bool
        default: false
author:
    - Denis Shipilov (@shipilovds)
'''

EXAMPLES = r'''
- name: Ensure that extension is disabled
  gnome_extension:
    name: "user-theme@gnome-shell-extensions.gcampax.github.com"
    enabled: False

- name: Ensure that extension is uninstalled
  gnome_extension:
    name: "arcmenu@arcmenu.com"
    src: 'https://extensions.gnome.org/extension-data/arcmenuarcmenu.com.v6.shell-extension.zip'
    state: absent

- name: Ensure that extension is installed and enabled
  gnome_extension:
    name: "night-light-slider.timurlinux.com"
    src: 'https://extensions.gnome.org/extension-data/night-light-slider.timurlinux.com.v19.shell-extension.zip'
    enabled: True

# And there is a way for a many:
- set_fact:
    gnome_extensions:
      - name: 'dash-to-panel@jderose9.github.com'
        enabled: True
        url: 'https://extensions.gnome.org/extension-data/dash-to-paneljderose9.github.com.v40.shell-extension.zip'
      - name: 'openweather-extension@jenslody.de'
        state: absent

- name: 'Gnome Extensions : Install and Setup'
  shipilovds.workstation.gnome_extension:
    name: "{{ item.name }}"
    src: "{{ item.url | default(omit) }}"
    enabled: "{{ item.enabled | default(omit) }}"
    state: "{{ item.state | default(omit) }}"
    force: True
  loop: "{{ gnome_extensions }}"
  loop_control:
    label: "{{ item['name'].split('@')[0] }}"
'''

RETURN = r''' # '''  # TODO: write RETURN section and create doc generation model for it


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.shipilovds.workstation.plugins.module_utils.gsettings_helpers import GsettingsWrapper
import yaml
import re
from os import listdir
from os.path import expanduser, isdir, join

# 'Argument spec' is taken from 'DOCUMENTATION' ('options' block) as the primary source of truth
ARGS_SPEC = yaml.safe_load(DOCUMENTATION)['options']
GNOME_EXTENSION_EXECUTABLE = '/usr/bin/gnome-extensions'  # TODO: make this path an option for the module
GNOME_EXTENSION_DIRS = ['/usr/share/gnome-shell/extensions/', '~/.local/share/gnome-shell/extensions/']
CHECK_MOD = True


class GnomeExtension():
    '''Class that helps to operate with Gnome Shell Extension.

    Args:
        name (str): Extension name (uuid)
        src (:obj:`str`, optional): Path of a bundle (might be None)
        force (bool): `True` if force installation, `False` if not
        state (str): `present` or `absent`
        enabled (:obj:`bool`, optional): `True` if enabled, `False` if disabled, `None` if not set

    Attributes:
        uuid (str): Extension name (uuid)
        src (:obj:`str`, optional): Path of a bundle (might be None)
        force (bool): True if force installation
        eventual_state (:obj:`dict` of :obj:`bool`): `installed` key with bool, `enabled` key with bool or `None`
        current_state (:obj:`dict` of :obj:`bool`): `installed` key with bool, `enabled` key with bool or `None`
        result (:obj:`dict` of :obj:`bool`): Dict with data that ansible module returns
    '''
    def __init__(self, name, src, force, state, enabled):
        self.uuid = name
        self.src = src
        self.force = force
        self.eventual_state = self._describe_eventual_state(state, enabled)
        self.current_state = {}
        self.result = {}
        self._update_current_state()

    def _update_current_state(self):
        ''' Describes current state (looks like self.eventual_state) '''
        installed = self._check_if_installed()
        enabled = self._check_if_enabled()

        self.current_state = {'installed': installed, 'enabled': enabled}

    def _describe_eventual_state(self, installed, enabled):
        '''Helps to construct a dict with eventual states.'''
        if installed == 'present':
            installed = True
        else:
            installed = False

        return {'installed': installed, 'enabled': enabled}

    def _get_gsetting_value_with_key(self, key):
        '''Helps to get gsettings value with a key.'''
        gsettings = GsettingsWrapper('org.gnome.shell', None, key)
        value = gsettings.read().unpack()

        return value

    def _check_if_enabled(self):
        '''Checks if extension is enabled.'''
        enabled = None
        if self.uuid in self._get_gsetting_value_with_key('enabled-extensions'):
            enabled = True
        if self.uuid in self._get_gsetting_value_with_key('disabled-extensions'):
            enabled = False

        return enabled

    def _change_enabled(self):
        ''' Changes 'enabled' state.

        Gets enabled and disabled extensions lists through gsettings.
        Changes their values according to desired state.
        '''
        enabled = GsettingsWrapper('org.gnome.shell', None, 'enabled-extensions')
        enabled_list = enabled.read().unpack()
        disabled = GsettingsWrapper('org.gnome.shell', None, 'disabled-extensions')
        disabled_list = disabled.read().unpack()
        if self.eventual_state['enabled'] and self.uuid not in enabled_list:
            enabled_list.append(self.uuid)
            operation = 'enable'
        if self.eventual_state['enabled'] is False and self.uuid not in disabled_list:
            disabled_list.append(self.uuid)
            operation = 'disable'
        if self.uuid in disabled_list:
            if self.eventual_state['enabled'] is not False:
                disabled_list.remove(self.uuid)
        if self.uuid in enabled_list:
            if self.eventual_state['enabled'] is not True:
                enabled_list.remove(self.uuid)
        if self.eventual_state['enabled'] is None:
            operation = 'flush from enabled/disabled'

        enabled.write(enabled_list)
        disabled.write(disabled_list)
        self.result['operations'].update({operation: 'success'})

    def _check_if_installed(self):
        '''Checks if extension is installed.'''
        installed = False
        installed_extensions = []
        for src in GNOME_EXTENSION_DIRS:
            try:
                src = expanduser(src)
                for item in listdir(src):
                    if isdir(join(src, item)):
                        installed_extensions.append(item)
            except FileNotFoundError:
                # It means that local user extensions does not exist yet
                # A little dirty hack: do nothing here
                pass
        if self.uuid in installed_extensions:
            installed = True

        return installed

    def _define_install_cmd(self):
        '''Helps to define install/uninstall command arguments.'''
        if self.eventual_state['installed']:
            operation = ['install', self.src]
            if self.force:
                operation.append('--force')
        else:
            operation = ['uninstall', self.uuid]

        return operation

    def _run_cmd(self, ansible_module, operation):
        '''Run cmd with ansible_module.run_command().

        Does nothing if check_mode.
        '''
        if not ansible_module.check_mode:
            rc, stdout, stderr = ansible_module.run_command([GNOME_EXTENSION_EXECUTABLE] + operation)
            self.result['operations'].update({operation[0]: {}})
            if stdout or stderr:
                self.result['operations'][operation[0]]['stdout'] = stdout
                self.result['operations'][operation[0]]['stderr'] = stderr
            self.result['operations'][operation[0]]['rc'] = rc
            match = re.search(to_text('exists and --force was not specified'), stderr)
            if rc != 0 and match is None:
                msg = f'Gnome Extension Executable Error: {stderr}'
                self.result.update({'failed': True, 'msg': msg})

    def change_state(self, ansible_module):
        '''Changes a states of the extension.

        Method helps to set enabled/disabled and installed/uninstalled states.
        Removes from enabled/disabled lists if extension is uninstalled.

        Args:
            ansible_module (AnsibleModule): AnsibleModule object
        '''
        # TODO: I know - there is a better way to install/enable extension. And without session restart. I'll try it someday...
        self.result['operations'] = {}
        if self.current_state['installed'] != self.eventual_state['installed']:
            if self.eventual_state['installed'] and self.src is None:
                msg = 'Extension bundle path (\'src\' parameter) is missing! Cannot install extension without bundle path.'
                self.result.update({'failed': True, 'msg': msg})
                return

            self._run_cmd(ansible_module, self._define_install_cmd())
            if bool(self.result.get('failed')):
                return
            self._update_current_state()
            if self.current_state['installed'] == self.eventual_state['installed']:
                self.result['changed'] = True

        if self.eventual_state['enabled'] is None:
            return
        else:
            if not self.current_state['installed']:
                # if uninstalled - just make sure that extension deleted from enabled and disabled:
                self.eventual_state['enabled'] = None

        if self.current_state['enabled'] != self.eventual_state['enabled']:
            self._change_enabled()
            self._update_current_state()
            if self.current_state['enabled'] == self.eventual_state['enabled']:
                self.result['changed'] = True


def main():
    module = AnsibleModule(argument_spec=ARGS_SPEC, supports_check_mode=CHECK_MOD)
    try:
        extension = GnomeExtension(**module.params)
    except Exception as ex:
        module.fail_json(msg=str(ex), **extension.result)

    if extension.current_state != extension.eventual_state:
        try:
            extension.change_state(module)
        except Exception as ex:
            module.fail_json(msg=str(ex), **extension.result)

    module.exit_json(**extension.result)


if __name__ == '__main__':
    main()
