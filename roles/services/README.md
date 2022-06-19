# Ansible Role: `services`

**>> [Back to full roles readme](https://github.com/shipilovds/workstation/tree/latest/docs/roles.md)**

Helps to setup system services.

### Role tasks

| Tasks | Description | Tags |
|-------|-------------|------|
| [shadowsocks](https://github.com/shipilovds/workstation/tree/latest/roles/services/tasks/shadowsocks.yml) | Setup Shadowsocks Client | `shadowsocks`, `ss` |

### Role Variables

```yaml
services_shadowsocks_pip_pkg: 'git+https://github.com/shipilovds/shadowsocks-pyclient.git@main'

services_shadowsocks_conf: {}
# services_shadowsocks_conf:
#   server: 'example.com'
#   server_port: 8388
#   local_port: 8787
#   password: 'Pa$$word'
#   timeout: 300
#   method: 'aes-256-cfb'
#   fast_open: True
```
