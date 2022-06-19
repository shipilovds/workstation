# Ansible Role: `pkgs`

**>> [Back to full roles readme](https://github.com/shipilovds/workstation/tree/latest/docs/roles.md)**

Helps to install system pkgs.

### Role tasks

| Tasks | Description | Tags |
|-------|-------------|------|
| [dnf](https://github.com/shipilovds/workstation/tree/latest/roles/pkgs/tasks/dnf.yml) | Install dnf packages | `dnf` |
| [pip](https://github.com/shipilovds/workstation/tree/latest/roles/pkgs/tasks/pip.yml) | Install pip packages | `pip` |

### Role Variables

```yaml
pkgs_dnf_repos: []
### Example:
# pkgs_dnf_repos:
#   - name: GoogleChrome
#     description: 'Official google crome repo'
#     baseurl: 'http://dl.google.com/linux/chrome/rpm/stable/x86_64'
#     gpgkey: 'https://dl.google.com/linux/linux_signing_key.pub'
#     gpgcheck: True
pkgs_dnf_packages: []
### Example:
# pkgs_dnf_packages:
#   - git
#   - google-chrome-stable
#   - htop
pkgs_pip_packages: []
### Example:
# pkgs_pip_packages:
#   - ansible-lint
#   - flake8
```
