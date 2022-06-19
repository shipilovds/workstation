# Ansible Role: `tools`

**>> [Back to full roles readme](https://github.com/shipilovds/workstation/tree/latest/docs/roles.md)**

Helps to setup a set of various tools.

### Role tasks

| Tasks | Description | Tags |
|-------|-------------|------|
| [git](https://github.com/shipilovds/workstation/tree/latest/roles/tools/tasks/git.yml) | Setup Git Credentials | `credentials`, `git` |
| [neovim](https://github.com/shipilovds/workstation/tree/latest/roles/tools/tasks/neovim.yml) | Setup NeoVim | `neovim`, `nvim` |
| [ohmyzsh](https://github.com/shipilovds/workstation/tree/latest/roles/tools/tasks/ohmyzsh.yml) | Setup Oh My Zsh | `ohmyzsh` |
| [pypi](https://github.com/shipilovds/workstation/tree/latest/roles/tools/tasks/pypi.yml) | Setup PyPi Credentials | `credentials`, `pypi` |
| [ssh](https://github.com/shipilovds/workstation/tree/latest/roles/tools/tasks/ssh.yml) | Setup SSH | `ssh` |
| [tmux](https://github.com/shipilovds/workstation/tree/latest/roles/tools/tasks/tmux.yml) | Setup Tmux | `tmux` |
| [yamllint](https://github.com/shipilovds/workstation/tree/latest/roles/tools/tasks/yamllint.yml) | Setup Yamllint | `yamllint`, `lint` |

### Role Variables

```yaml
tools_user_name: user
tools_user_privkey_filename: id_ed25519
tools_user_privkey: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  ...
  -----END OPENSSH PRIVATE KEY-----
tools_user_pubkey: ''
### Example:
# tools_user_pubkey: 'ssh-ed25519 AAAAC3N2ezgGUa2yV5fSCZHccSbz55JNLr2LekER8AGbbRCMfEZkCE83HB6SLwW8TzFN user@localhost'

tools_ohmyzsh_pkgs:
  - zsh

tools_ohmyzsh_additional_plugins: []
### Example:
# tools_ohmyzsh_additional_plugins:
#   - 'https://github.com/zsh-users/zsh-syntax-highlighting.git'

tools_ohmyzsh_config_plugins: []
### Example:
# tools_ohmyzsh_config_plugins:
#   - 'colored-man-pages'

tools_neovim_dnf_pkgs:
  - neovim

tools_neovim_pip_pkgs: []

tools_neovim_plugins: []
### Example:
# tools_neovim_plugins:
#   - 'git@github.com:dense-analysis/ale.git'
#   - 'git@github.com:nvie/vim-flake8.git'

tools_neovim_init_content: ''
### Example:
# tools_neovim_init_content: |
#   autocmd Filetype make setlocal ts=4 sts=4 sw=4
#   autocmd FileType groovy setlocal et
#   autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab indentkeys-=0#
#   au BufNewFile,BufReadPost * if &filetype == "yaml" | set softtabstop=2 | set indentkeys-=0# | endif
#   let g:syntastic_yaml_checkers = ['yamllint']

tools_tmux_config_url: 'https://gist.githubusercontent.com/shipilovds/1472461cf0c77dd1ef293b8ee0bf3310/raw/8e0482157cbe0fbb0a0ac56a977dde1a160498cb/tmux.conf'

tools_tmux_pkgs:
  - tmux

tools_yamllint_pkgs:
  - yamllint

tools_git_config_settings: {}
### Example:
# tools_git_config_settings:
#   user.email: "you@example.com"
#   user.name: "Your Name"

tools_pypirc_token: ''
### Example:
# tools_pypirc_token: > pypi-iq9ej3RT0aVzznGSg2USvLu9IuivX1iJ3DKtuQptqccI8cGiHZlmiqYIAJDeRBBVf3vvFoVK
#   6DUmLViKOPepr3vHM147MeCY5ePVzfjWILR6SZvqDydwdYowB76yKBTiG_jiIbbI-A92jQCfYMzDHxHeVaMsQHQJmZs-BK5
```
