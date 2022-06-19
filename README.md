[![Galaxy page](https://img.shields.io/badge/galaxy-shipilovds.workstation-blue?style=flat-square&logo=Ansible)](https://galaxy.ansible.com/shipilovds/workstation)

# shipilovds.workstation

This colection created to store some modules and roles I wrote to setup my workstation.

## Included content

### Modules

|                                                                      Name                                                                      |              Description               |
|------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|
| [shipilovds.workstation.gnome_extension](https://github.com/shipilovds/workstation/blob/latest/docs/shipilovds.workstation.gnome_extension.md) | Gnome shell extensions management      |
|       [shipilovds.workstation.gsettings](https://github.com/shipilovds/workstation/blob/latest/docs/shipilovds.workstation.gsettings.md)       | Gnome applications settings management |

> NOTE: I`ve made some cool stuff to make "[docs.ansible.com](https://docs.ansible.com/ansible/latest/)"-like modules documentation. Generated pages you can find on the links above.
> Template file and tool itself:
> - [Template](https://github.com/shipilovds/workstation/blob/latest/helpers/docs_template.j2)
> - [Tool](https://github.com/shipilovds/workstation/blob/latest/helpers/generate_md_docs.py)

### Roles

|                                     Name                                         |                                        Description                                         |
|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
|    [gnome](https://github.com/shipilovds/workstation/tree/latest/roles/gnome)    | Setup Gnome and Gnome-Shell                                                                |
|     [pkgs](https://github.com/shipilovds/workstation/tree/latest/roles/pkgs)     | Install dnf, apt and pip packages                                                          |
| [services](https://github.com/shipilovds/workstation/tree/latest/roles/services) | Setup for system services (Shadowsocks for now)                                            |
|    [tools](https://github.com/shipilovds/workstation/tree/latest/roles/tools)    | Setup system tools and shell environment (git, neovim, ohmyzsh, pypi, ssh, tmux, yamllint) |

> See more [here](https://github.com/shipilovds/workstation/blob/latest/docs/roles.md)

## Ansible version compatibility

Honestly, I have never really checked compatibility with ansible version.

Modules 100% works with `ansible core == 2.12`

## Installation

### Ansible galaxy

You can install the `shipilovds.workstation` collection with the Ansible Galaxy CLI:

```
# Install from https://galaxy.ansible.com
ansible-galaxy collection install shipilovds.workstation

# Install from GitHub
ansible-galaxy collection install git@github.com:shipilovds/workstation.git
```

You can also include it in a `requirements.yml` file and install it with

`ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: shipilovds.workstation
```

### PIP (deprecated method)

To get pip package with modules just type `pip install git+https://github.com/shipilovds/workstation@latest`

> You can choose pip installation if you only need modules. I've decided not to make roles installation via pip.

## Using this collection

See [roles documentation](https://github.com/shipilovds/workstation/blob/latest/docs/roles.md#usage) to understand how to use roles.

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

- [Issues](https://github.com/shipilovds/workstation/issues)
- [Pull Requests](https://github.com/shipilovds/workstation/pulls)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
