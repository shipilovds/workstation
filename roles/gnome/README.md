# Ansible Role: `gnome`

**>> [Back to full roles readme](https://github.com/shipilovds/workstation/tree/latest/docs/roles.md)**

Helps to setup Gnome Shell Environment.

> This role uses [shipilovds.workstation.gnome-extension](https://github.com/shipilovds/workstation/tree/latest/plugins/modules/gnome_extension.py) and [shipilovds.workstation.gsettings](https://github.com/shipilovds/workstation/tree/latest/plugins/modules/gsettings.py) modules

### Role tasks

| Tasks | Description | Tags |
|-------|-------------|------|
| [extensions](https://github.com/shipilovds/workstation/tree/latest/roles/gnome/tasks/extensions.yml) | Gnome Shell Extensions management | `gnome_extensions` |
| [gsettings](https://github.com/shipilovds/workstation/tree/latest/roles/gnome/tasks/gsettings.yml) | Gsettings management | `gsettings` |

### Role Variables

```yaml
gnome_extensions: []
### Example:
# gnome_extensions:
#   - name: 'dash-to-panel@jderose9.github.com'
#     enabled: True
#     url: 'https://extensions.gnome.org/extension-data/dash-to-paneljderose9.github.com.v40.shell-extension.zip'
#   - name: 'apps-menu@gnome-shell-extensions.gcampax.github.com'
#     enabled: False

gnome_gsettings: {}
### Example:
# gnome_gsettings:
#   org.gnome.desktop.input-sources:
#     keys:
#       sources:
#         - ('xkb', 'us')
#         - ('xkb', 'ru')
#   org.gtk.Settings.FileChooser:
#     keys:
#       location-mode: 'filename-entry'
#       sort-directories-first: True
#   org.gnome.desktop.notifications.application:
#     path: '/org/gnome/desktop/notifications/application/org-gnome-software/'
#     keys:
#       enable: False
```
