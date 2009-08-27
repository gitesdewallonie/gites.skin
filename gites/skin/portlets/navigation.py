# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from plone.app.portlets.portlets.navigation import Renderer as BaseRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Renderer(BaseRenderer):

    _template = ViewPageTemplateFile('templates/navigation.pt')
