# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
#from zope.app.traversing.browser.interfaces import IAbsoluteURL
from Products.Five import BrowserView
#from Acquisition import aq_inner, aq_parent
from zope.interface import implements
#from zope.component import queryMultiAdapter
#from DateTime import DateTime
from gites.skin.browser.interfaces import (IProprioInfo)
#from Products.CMFCore.utils import getToolByName
#from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.sqlalchemy import getSAWrapper


class ProprioInfo(BrowserView):
    """
    Infos relatives aux proprio
    """
    implements(IProprioInfo)

    def getAllProprio(self):
        """
        Liste tous les prorios
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        proprioTable = wrapper.getMapper('proprio')
        query = session.query(proprioTable)
        proprios = query.all()
        return proprios

    def getProprioByLogin(self, loginProprio):
        """
        Sélectionne les infos d'un proprio selon son login
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        proprioTable = wrapper.getMapper('proprio')
        query = session.query(proprioTable)
        query = query.filter(proprioTable.pro_log == loginProprio)
        proprio = query.all()
        return proprio
