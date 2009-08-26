# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
import random
from DateTime import DateTime
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class SejourFuteRootFolder(BrowserView):

    def __init__(self, context, request, *args, **kw):
        super(BrowserView, self).__init__(context, request, *args, **kw)
        utool = getToolByName(context, 'portal_url')
        self.portal_url = utool()
        self.portal = utool.getPortalObject()
        self.cat = getToolByName(self.context, 'portal_catalog')

    def getRandomVignette(self, sejour_url, amount=1):
        """
        Return a random vignette for a sejour fute
        """
        results = self.cat.searchResults(portal_type='Vignette',
                                         path={'query': sejour_url})
        results = list(results)
        random.shuffle(results)
        return results[:amount]

    def getAllSejourFute(self):
        results = self.cat.searchResults(portal_type='SejourFute',
                                               end={'query': DateTime(),
                                                    'range': 'min'},
                                               review_state='published')
        results = list(results)
        random.shuffle(results)
        return results
