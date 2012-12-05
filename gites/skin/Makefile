#!/usr/bin/make
#
# Makefile for gites translations domain

PYTHON=../../../../bin/python
ZOPE_HOME="../../../../parts/zope2/"
SOFTWARE_HOME="../../../../parts/zope2/lib/python/"
PYTHONPATH:=$(PYTHONPATH):$(SOFTWARE_HOME)

translations: extract-translations update-translations compile-translations

.PHONY: extract-translations
extract-translations:
	../../../../i18n/bin/i18ndude rebuild-pot --pot locales/gites.pot --create gites . ../../../gites.core/gites/core/ ../../../bnbelgium.skin/bnbelgium/skin/ ../../../gites.calendar/gites/calendar/ ../../../gites.map/src/gites/map/

.PHONY: update-translations
update-translations:
	../../../../i18n/bin/i18ndude merge --pot locales/gites.pot --merge locales/manual.pot
	msgmerge -U --backup=off locales/fr/LC_MESSAGES/gites.po locales/gites.pot
	msgmerge -U --backup=off locales/en/LC_MESSAGES/gites.po locales/gites.pot
	msgmerge -U --backup=off locales/de/LC_MESSAGES/gites.po locales/gites.pot
	msgmerge -U --backup=off locales/it/LC_MESSAGES/gites.po locales/gites.pot
	msgmerge -U --backup=off locales/nl/LC_MESSAGES/gites.po locales/gites.pot

.PHONY: compile-translations
compile-translations:
	set -e; \
	for f in locales/*/LC_MESSAGES/gites.po; do \
		msgfmt -o $${f%.po}.mo $$f;\
	done;\
