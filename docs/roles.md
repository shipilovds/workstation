[comment]: <> (TODO: make it templated)
# shipilovds.workstation roles

A set of roles to setup workstation system

# Requirements

 - `ansible-core` >= `2.12` (Because of the modules used in `gnome` role)

# Supported platforms

- `Fedora` >= `36`

# Roles

| Role | Description |
|------|-------------|
| [gnome](https://github.com/shipilovds/workstation/tree/latest/roles/gnome/README.md) | Helps to setup Gnome Shell Environment. |
| [pkgs](https://github.com/shipilovds/workstation/tree/latest/roles/pkgs/README.md) | Helps to install system pkgs. |
| [services](https://github.com/shipilovds/workstation/tree/latest/roles/services/README.md) | Helps to setup system services. |
| [tools](https://github.com/shipilovds/workstation/tree/latest/roles/tools/README.md) | Helps to setup a set of various tools. |

# Example Playbook

```yaml
---
- hosts: localhost
  collections:
    - shipilovds.workstation
  vars_files:
    - vars/general.yml
    - vars/enctypted.yml
  roles:
    - role: pkgs
      tags: ['pkgs']
    - role: tools
      tags: ['tools']
    - role: gnome
      tags: ['gnome']
    - role: services
      tags: ['services']
```
