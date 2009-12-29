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
from Products.CMFCore.utils import getToolByName
#from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.sqlalchemy import getSAWrapper
from mailer import Mailer


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

    def getProprioByLogin(self):
        """
        Sélectionne les infos d'un proprio selon son login
        """
        pm = getToolByName(self, 'portal_membership')
        user = pm.getAuthenticatedMember()
        proprioLogin = user.getUserName()
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        proprioTable = wrapper.getMapper('proprio')
        query = session.query(proprioTable)
        query = query.filter(proprioTable.pro_log == proprioLogin)
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

    def getAllCivilites(self):
        """
        Sélectionne les civilites
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        civiliteTable = wrapper.getMapper('civilite')
        query = session.query(civiliteTable)
        civilites = query.all()
        return civilites

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

    def getProprioMajByProPk(self, proPk):
        """
        retourne un proprio selon sa clé depuis la table proprio_maj
        """
        proprioMajExist = False
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        proprioMajTable = wrapper.getMapper('proprio_maj')
        query = session.query(proprioMajTable)
        query = query.filter(proprioMajTable.pro_maj_propk == proPk)
        records = query.all()
        if len(records) > 0:
            proprioMajExist = True
        else:
            proprioMajExist = False
        return proprioMajExist

    def sendMail(self, sujet, message):
        """
        envoi de mail à secretariat GDW
        """
        mailer = Mailer("localhost", "info@gitesdewallonie.be")
        #mailer = Mailer("smtp.scarlet.be", "alain.meurant@affinitic.be")
        mailer.setSubject(sujet)
        mailer.setRecipients("alain.meurant@affinitic.be")
        #mailer.setRecipients("alain.meurant@skynet.be")
        mail = message
        mailer.sendAllMail(mail)

    def modifyStatutMajProprio(self, proPk, proMajInfoEtat):
        """
        change le statut de mise à jour d'un hebergement
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        updateProprio = wrapper.getMapper('proprio')
        query = session.query(updateProprio)
        query = query.filter(updateProprio.pro_pk == proPk)
        record = query.one()
        record.pro_maj_info_etat = proMajInfoEtat
        session.save_or_update(record)
        session.flush()

    def  updateProprioMaj(self):
        """
        mise à jour des données maj du proprio
        """
        fields = self.request
        proMajProPk=fields.get('pro_maj_propk')
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        updateProprioMaj = wrapper.getMapper('proprio_maj')
        query = session.query(updateProprioMaj)
        query = query.filter(updateProprioMaj.pro_maj_propk == proMajProPk)
        record = query.one()
        record.pro_maj_civ_fk = fields.get('pro_maj_civ_fk')
        record.pro_maj_nom1 = unicode(fields.get('pro_maj_nom1'), 'utf-8')
        record.pro_maj_prenom1 = unicode(fields.get('pro_maj_prenom1'), 'utf-8')
        record.pro_maj_nom2 = unicode(fields.get('pro_maj_nom2'), 'utf-8')
        record.pro_maj_prenom2 = unicode(fields.get('pro_maj_prenom2'), 'utf-8')
        record.pro_maj_societe = unicode(fields.get('pro_maj_societe'), 'utf-8')
        record.pro_maj_adresse = unicode(fields.get('pro_maj_adresse'), 'utf-8')
        record.pro_maj_com_fk = fields.get('pro_maj_com_fk')
        record.pro_maj_email = fields.get('pro_maj_email')
        record.pro_maj_tel_priv = fields.get('pro_maj_tel_priv')
        record.pro_maj_fax_priv = fields.get('pro_maj_fax_priv')
        record.pro_maj_gsm1 = fields.get('pro_maj_gsm1')
        record.pro_maj_url = fields.get('pro_maj_url')
        record.pro_maj_tva = fields.get('pro_maj_tva')
        record.pro_maj_langue = fields.get('pro_maj_langue')
        record.pro_maj_info_etat = unicode(fields.get('pro_maj_info_etat'), 'utf-8')
        session.add(record)
        session.flush()

    def insertProprioMaj(self):
        """
        insère les infos mise à jour par proprio dans table provisoire
        """
        fields = self.request
        proPk=fields.get('pro_maj_propk')
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        insertProprioMaj = wrapper.getMapper('proprio_maj')
        newEntry = insertProprioMaj(pro_maj_propk=proPk,\
                                    pro_maj_civ_fk=fields.get('pro_maj_civ_fk'),\
                                    pro_maj_nom1=fields.get('pro_maj_pronom1'),\
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
                                    pro_maj_info_etat=fields.get('pro_maj_info_etat'))
        session.add(newEntry)
        session.flush()

    def addProprioMaj(self):
        """
        gestion de l'ajout des données de maj par le proprio
        """
        fields = self.request
        proPk = fields.get('pro_maj_propk')
        proNom = fields.get('pro_maj_nom1')
        proprio = self.getProprioByLogin()
        for elem in proprio:
            propriopk=elem.pro_pk
        
        if int(proPk) == propriopk:
            proNom = fields.get('pro_maj_pronom1')
            isProprioMajExist = self.getProprioMajByProPk(proPk)

            if isProprioMajExist:
                self.updateProprioMaj()
            else:
                self.insertProprioMaj()

            proMajInfoEtat="En attente confirmation"
            self.modifyStatutMajProprio(proPk, proMajInfoEtat)

            sujet="Modification des donn&eacute;es personnelles par un proprio"
            message="""Le proprio %s dont la référence est %s vient de modifier ses
                       données. Il faut les vérifier et les valider
                       via le lien suivant http://gdwadmin.affinitic.be/"""%(proNom, proPk)
            self.sendMail(sujet, message)
            return {'status':1}
        else:
            sujet="Un proprio a essayé modifié ses données personnelles"
            message="""Le proprio %s dont la référence est %s a essayé de modifier ses
                       données. Le processus est avorté suite à un problème de PK"""%(proNom, proPk)
            self.sendMail(sujet, message)
            return {'status':-1}
