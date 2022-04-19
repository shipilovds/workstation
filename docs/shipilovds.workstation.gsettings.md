# shipilovds.workstation.gsettings - Gnome applications settings management

## Synopsis

Module to set gsettings options

## Parameters

|      Parameter       |       Comments       |
|----------------------|----------------------|
| **schema**<br>str / *required* | The name of the schema for this Gsettings object<br> |
| **path**<br>str | The path within the backend where the settings are<br>A valid path begins and ends with '/' and does not contain two consecutive '/' characters.<br> |
| **key**<br>str / *required* | Gsettings schema key<br> |
| **value**<br>raw / *required* | Gsettings schema value<br> |


## Examples

```yaml
### simple usage:

- name: 'Gsettings : Setup Schema'
  shipilovds.workstation.gsettings:
    schema: org.gnome.nautilus.preferences
    key: default-folder-viewer
    value: list-view

### a little more complicated:
## tasks/main.yml:

- set_fact:
    gsettings:
      org.gnome.desktop.wm.keybindings:
        keys:
          switch-input-source:
          - <Alt>Shift_L
      org.gnome.desktop.input-sources:
        keys:
          sources:
          - ('xkb', 'us')
          - ('xkb', 'ru')
      org.gtk.Settings.FileChooser:
        keys:
          location-mode: filename-entry
          sort-directories-first: true
      org.gnome.desktop.notifications.application:
        path: /org/gnome/desktop/notifications/application/org-gnome-software/
        keys:
          enable: false


- name: Gsettings management
  include_tasks: gsettings.yml
  loop: '{{ env_gsettings | dict2items }}'
  loop_control:
    loop_var: _schema
    label: '{{ _schema.key }}'

## tasks/gsettings.yml:

- name: "Gsettings : Setup '{{ _schema.key }}'"
  shipilovds.workstation.gsettings:
    schema: '{{ _schema.key }}'
    path: "{{ _schema.value['path'] | default(omit) }}"
    key: '{{ item.key }}'
    value: '{{ item.value }}'
  loop: "{{ _schema.value['keys'] | dict2items }}"


```

## Authors
* Denis Shipilov (@shipilovds)
