# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class Translate(BrowserView):
    """
    Translate object
    """

    def getTranslatedObjectUrl(self, path):
        """
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        obj = self.context.restrictedTraverse(path)
        translatedObject = obj.getTranslation()
        if translatedObject:
            url = translatedObject.absolute_url()
        else:
            url = obj.absolute_url()
        return url
