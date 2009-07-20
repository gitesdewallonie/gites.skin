# -*- coding: utf-8 -*-
"""
GitesSkin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: meubles.py 1857 2008-03-12 12:59:44Z jfroche $
"""
from Products.Five import BrowserView
from interfaces import IMeublesView
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

class MeublesView(BrowserView):
    """
    """
    implements(IMeublesView)

    def getMeubles(self):
        """
        return the meubles in the folder
        """
        cat = getToolByName(self.context, 'portal_catalog')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        gitesmeubles = getattr(portal, 'gites-meubles')
        defaultPage = gitesmeubles.getDefaultPage()
        url = '/'.join(gitesmeubles.getPhysicalPath())
        contentFilter = {}
        path = {}
        path['query'] = url
        path['depth'] = 1
        contentFilter['path'] = path
        contentFilter['portal_type'] = ['Document']
        contentFilter['sort_on'] = 'getObjPositionInParent'
        contentFilter['review_state'] = 'published'
        results = cat.queryCatalog(contentFilter)
        results = [result for result in results if result.getId != defaultPage]
        return results

