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

    def getAllCommunes(self):
        """
        Sélectionne les communes et les cp
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        communeTable = wrapper.getMapper('commune')
        query = session.query(communeTable)
        communes = query.all()
        return communes

    def getAllProprioMaj(self):
        """
        Liste tous les prorios en attente de modification
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        proprioMajTable = wrapper.getMapper('proprio_maj')
        query = session.query(proprioMajTable)
        propriosMaj = query.all()
        return propriosMaj
        
    def addProprioMaj(self):
        """
        ajoute les infos mise à jour par proprio dans table provisoire
        """
        fields = self.context.REQUEST
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        insertProprioMaj = wrapper.getMapper('proprio_maj')
        newEntry = insertProprioMaj(pro_maj_propk=fields.get('pro_maj_propk'),\
                                    pro_maj_civ_fk=fields.get('pro_maj_civ_fk'),\
                                    pro_maj_nom1=fields.get('pro_maj_nom1'),\
                                    pro_maj_prenom1=fields.get('pro_maj_prenom1'),\
                                    pro_maj_nom2=fields.get('pro_maj_nom2'),\
                                    pro_maj_prenom2=fields.get('pro_maj_prenom2'),\
                                    pro_maj_societe=fields.get('pro_maj_societe'),\
                                    pro_maj_adresse=fields.get('pro_maj_adresse'),\
                                    pro_maj_com_fk=fields.get('pro_maj_com_fk'),\
                                    pro_maj_email=fields.get('pro_maj_email'),\
                                    pro_maj_tel_priv=fields.get('pro_maj_tel_priv'),\
                                    pro_maj_fax_priv=fields.get('pro_maj_fax_priv'),\
                                    pro_maj_gsm1=fields.get('pro_maj_gsm1'),\
                                    pro_maj_url=fields.get('pro_maj_url'),\
                                    pro_maj_tva=fields.get('pro_maj_tva'),\
                                    pro_maj_langue=fields.get('pro_maj_langue'),\
                                    pro_maj_data=fields.get('pro_maj_data'))
        session.save(newEntry)
        session.flush()

