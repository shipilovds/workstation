# shipilovds.workstation.gnome_extension - Gnome shell extensions management

## Synopsis

This module can install or enable/disable gnome shell extensions

You can install and then enable module by one task (use both arguments)

You need to reload Gnome Session to make extension enabled.

## Parameters

|      Parameter       |       Comments       |
|----------------------|----------------------|
| **name**<br>str / *required* | Extension name (uuid)<br> |
| **state**<br>str | State of installation in the system<br>**Choices:**<br>* **present ←** (default)<br>* absent |
| **enabled**<br>bool | Enable module when true / disable when false<br>Changes nothing if not set<br> |
| **src**<br>path | Module file path or URL (to zip file)<br> |
| **force**<br>bool | Force module installation<br> |


## Examples

```yaml
- name: Ensure that extension is disabled
  gnome_extension:
    name: user-theme@gnome-shell-extensions.gcampax.github.com
    enabled: false


- name: Ensure that extension is uninstalled
  gnome_extension:
    name: arcmenu@arcmenu.com
    src: https://extensions.gnome.org/extension-data/arcmenuarcmenu.com.v6.shell-extension.zip
    state: absent


- name: Ensure that extension is installed and enabled
  gnome_extension:
    name: night-light-slider.timurlinux.com
    src: https://extensions.gnome.org/extension-data/night-light-slider.timurlinux.com.v19.shell-extension.zip
    enabled: true

# And there is a way for a many:

- set_fact:
    gnome_extensions:
    - name: dash-to-panel@jderose9.github.com
      enabled: true
      url: https://extensions.gnome.org/extension-data/dash-to-paneljderose9.github.com.v40.shell-extension.zip
    - name: openweather-extension@jenslody.de
      state: absent


- name: 'Gnome Extensions : Install and Setup'
  shipilovds.workstation.gnome_extension:
    name: '{{ item.name }}'
    src: '{{ item.url | default(omit) }}'
    enabled: '{{ item.enabled | default(omit) }}'
    state: '{{ item.state | default(omit) }}'
    force: true
  loop: '{{ gnome_extensions }}'
  loop_control:
    label: "{{ item['name'].split('@')[0] }}"

```

## Authors
* Denis Shipilov (@shipilovds)
