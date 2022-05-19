[![Galaxy page](https://img.shields.io/badge/galaxy-shipilovds.workstation-lightgrey?logo=Ansible)](https://galaxy.ansible.com/shipilovds/workstation)

# shipilovds.workstation

This colection created to store some modules I wrote to setup my workstation.

## Included content

### Modules

| Name | Description |
|------|-------------|
| [shipilovds.workstation.gsettings](https://github.com/shipilovds/workstation/blob/latest/docs/shipilovds.workstation.gsettings.md) | Gnome applications settings management |
| [shipilovds.workstation.gnome_extension](https://github.com/shipilovds/workstation/blob/latest/docs/shipilovds.workstation.gnome_extension.md) | Gnome shell extensions management |

> NOTE: I`ve made some cool stuff to make "[docs.ansible.com](https://docs.ansible.com/ansible/latest/)"-like modules documentation. Generated pages you can find on the links above.
> Template file and tool itself:
> * [Template](https://github.com/shipilovds/workstation/blob/latest/helpers/docs_template.j2)
> * [Tool](https://github.com/shipilovds/workstation/blob/latest/helpers/generate_md_docs.py)

## Ansible version compatibility

Honestly, I have never really checked compatibility with ansible version.

Modules 100% works with `ansible core == 2.12`

## Installing this modules

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

### PIP

To get pip package with modules just type `pip install git+https://github.com/shipilovds/workstation@latest`

## Using this collection

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

- [Issues](https://github.com/shipilovds/workstation/issues)
- [Pull Requests](https://github.com/shipilovds/workstation/pulls)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
