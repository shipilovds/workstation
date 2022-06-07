.PHONY: clean clean-build clean-pyc docs pip-build pip-install pip-uninstall pip-publish galaxy-build galaxy-install galaxy-uninstall galaxy-publish lint

NAMESPACE = shipilovds
NAME = workstation
VERSION = 1.0.3


lint:
	@flake8 plugins/ || true

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info/
	rm -f $(NAMESPACE)-$(NAME)-*.tar.gz

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

docs:
	python3 helpers/generate_md_docs.py

dist: clean
	pip3 install --user -r requirements.txt
	python3 setup.py sdist bdist_wheel
	python3 -m twine check dist/*

pip-build: dist

pip-install: dist
	pip3 install -U --user --no-index --find-links=./dist ansible-modules-$(NAMESPACE)-$(NAME)

pip-uninstall:
	pip3 uninstall ansible-modules-$(NAMESPACE)-$(NAME) -y

#pip-publish: dist
#	# NOTE: you need to have ~/.pypirc with your creds!
#	python3 -m twine upload --disable-progress-bar --non-interactive dist/*

%.tar.gz:
	ansible-galaxy collection build

galaxy-build: $(NAMESPACE)-$(NAME)-$(VERSION).tar.gz

galaxy-install: $(NAMESPACE)-$(NAME)-$(VERSION).tar.gz
	ansible-galaxy collection install $(NAMESPACE)-$(NAME)-$(VERSION).tar.gz

galaxy-uninstall:
	rm -fr ~/.ansible/collections/ansible_collections/$(NAMESPACE)

galaxy-publish: $(NAMESPACE)-$(NAME)-$(VERSION).tar.gz
	# NOTE: you need to have ~/.ansible/galaxy_token or ansible.cfg with required options!
	ansible-galaxy collection publish $(NAMESPACE)-$(NAME)-$(VERSION).tar.gz

build: pip-build galaxy-build
publish: galaxy-publish # pip-publish
