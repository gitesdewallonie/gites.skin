# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
import random
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class IdeeSejourRootFolder(BrowserView):

    def getIdeesTypes(self):
        """
        Returns the list of IdeeTypes available in the current folder
        """
        cat = getToolByName(self.context, 'portal_catalog')
        ideeSejour = getattr(self.context, 'idee-sejour')
        url = '/'.join(ideeSejour.getPhysicalPath())
        contentFilter = {}
        path = {}
        path['query'] = url
        path['depth'] = 1
        contentFilter['path'] = path
        contentFilter['portal_type'] = ['IdeeSejourFolder', 'IdeeSejour']
        contentFilter['sort_on'] = 'getObjPositionInParent'
        contentFilter['review_state'] = 'published'
        results = cat.queryCatalog(contentFilter)
        results = list(results)
        return results

    def getRandomVignette(self, sejour_url, amount=1):
        """
        Return a random vignette for a sejour fute
        """
        cat = getToolByName(self.context, 'portal_catalog')
        results = cat.searchResults(portal_type='Vignette',
                                    path={'query': sejour_url})
        results = list(results)
        random.shuffle(results)
        return results[:amount]

    def getVignetteURL(self):
        """
        Return vignette URL for an idee sejour
        """
        cat = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        results = cat.searchResults(portal_type='Vignette',
                                    path={'query': path})
        if results:
            return results[0].getURL()
