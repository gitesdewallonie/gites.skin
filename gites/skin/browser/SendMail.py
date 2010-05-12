# -*- coding: utf-8 -*-
from zope.component import queryMultiAdapter
from zope.interface import implements
from z3c.sqlalchemy import getSAWrapper
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from Products.Five import BrowserView
from interfaces import ISendMail
from mailer import Mailer

LANG_MAP = {'en': 'Anglais',
            'fr': 'Français',
            'nl': 'Néerlandais',
            'de': 'Allemand'}


class SendMail(BrowserView):
    """
    Envoi de mail
    """
    implements(ISendMail)

    def sendBlogSubscriptionMail(self):
        """
        envoi des informations d'inscription à la newsletter du blog
        """
        nom = self.request.get('nom', '')
        email = self.request.get('email', '')
        fromMail = "info@gitesdewallonie.be"
        if not email:
            return
        try:
            checkEmailAddress(email)
        except EmailAddressInvalid:
            return
        mailer = Mailer("localhost", fromMail)
        mailer.setSubject("[INSCRIPTION NEWSLETTER BLOG]")
        mailer.setRecipients("michael@gitesdewallonie.be")
        mail = u""":: INSCRIPTION ::

Une demande d'inscription a été envoyée via le blog :

    * Nom : %s
    * Email : %s
""" \
           %(unicode(nom, 'utf-8'), \
             unicode(email, 'utf-8'))
        mailer.sendAllMail(mail.encode('utf-8'), plaintext=True)

    def sendMailToProprio(self):
        """
        envoi d'un mail au proprio suite a un contact via hebergement description
        """
        hebPk = self.request.get('hebPk')
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        Hebergement = wrapper.getMapper('hebergement')
        heb = session.query(Hebergement).get(int(hebPk))
        hebNom = heb.heb_nom
        proprioMail = heb.proprio.pro_email
        if not proprioMail:
            proprioMail = u'info@gitesdewallonie.be'
        contactCivilite = self.request.get('contactCivilite')
        contactNom = self.request.get('contactNom', '')
        contactPrenom = self.request.get('contactPrenom', '')
        contactAdresse = self.request.get('contactAdresse', '')
        contactCp = self.request.get('contactCp')
        contactLocalite = self.request.get('contactLocalite', '')
        contactPays = self.request.get('contactPays', '')
        contactLangue = self.request.get('contactLangue', None)
        if not contactLangue or contactLangue.strip() == '...':
            language = self.request.get('LANGUAGE', 'en')
            contactLangue = LANG_MAP.get(language, '')
        contactTelephone = self.request.get('contactTelephone', '')
        contactFax = self.request.get('contactFax', '')
        contactEmail = self.request.get('contactEmail', None)
        debutJour = self.request.get('debutJour')
        debutMois = self.request.get('debutMois')
        debutAn = self.request.get('debutAn')
        finJour = self.request.get('finJour')
        finMois = self.request.get('finMois')
        finAn = self.request.get('finAn')
        nombrePersonne = self.request.get('nombrePersonne')
        remarque = self.request.get('remarque', '')

        fromMail = "info@gitesdewallonie.be"
        if contactEmail is not None:
            try:
                checkEmailAddress(contactEmail)
                fromMail = contactEmail
            except EmailAddressInvalid:
                pass

        mailer = Mailer("localhost", fromMail)
        mailer.setSubject("[DEMANDE D'INFORMATION PAR LE SITE]")
        mailer.setRecipients(proprioMail)
        mail = u""":: DEMANDE D'INFORMATION ::

Une demande d'information vient d'être réalisée via le site pour %s référence %s.

Il s'agit de :

    * Civilité : %s
    * Nom : %s
    * Prénom : %s
    * Adresse : %s
    * Localité : %s %s
    * Pays : %s
    * Langue : %s
    * Téléphone : %s
    * Fax : %s
    * E-mail : %s
    * Date début séjour  : %s-%s-%s
    * Date fin séjour  : %s-%s-%s
    * Nombre de personne : %s
    * Remarque : %s
""" \
              % (hebNom, \
                hebPk, \
                contactCivilite, \
                unicode(contactNom, 'utf-8'), \
                unicode(contactPrenom, 'utf-8'), \
                unicode(contactAdresse, 'utf-8'), \
                contactCp, \
                unicode(contactLocalite, 'utf-8'), \
                unicode(contactPays, 'utf-8'), \
                unicode(contactLangue, 'utf-8'), \
                contactTelephone, \
                contactFax, \
                unicode(contactEmail, 'utf-8'), \
                debutJour, \
                debutMois, \
                debutAn, \
                finJour, \
                finMois, \
                finAn, \
                nombrePersonne,\
                unicode(remarque, 'utf-8'))
        mailer.sendAllMail(mail.encode('utf-8'), plaintext=True)

        translate = queryMultiAdapter((self.context, self.request),
                                       name='getTranslatedObjectUrl')

        if self.request.get('newsletter', False):
            url = translate('newsletter')
            self.request.RESPONSE.redirect(url)
        else:
            url = translate('mailsent')
            self.request.RESPONSE.redirect(url)
        return ''
