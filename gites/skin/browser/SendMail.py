# -*- coding: utf-8 -*-
from zope.component import queryMultiAdapter
from zope.interface import implements
from z3c.sqlalchemy import getSAWrapper
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
        contactEmail = self.request.get('contactEmail', '')
        debutJour = self.request.get('debutJour')
        debutMois = self.request.get('debutMois')
        debutAn = self.request.get('debutAn')
        finJour = self.request.get('finJour')
        finMois = self.request.get('finMois')
        finAn = self.request.get('finAn')
        nombrePersonne = self.request.get('nombrePersonne')
        remarque = self.request.get('remarque', '')
        mailer = Mailer("localhost", "info@gitesdewallonie.be")
        mailer.setSubject("[DEMANDE D'INFORMATION PAR LE SITE]")
        mailer.setRecipients(proprioMail)
        mail = u"""<font color='#FF0000'><b>:: DEMANDE D'INFORMATION ::</b></font><br /><br />
              Une demande d'information vient d'être réalisée via le site pour %s référence %s.<br/>
              Il s'agit de :<br />
              <ul>
              <li>Civilité : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Nom : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Prénom : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Adresse : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Localit&eacute; : <font color='#ff9c1b'><b>%s</b> <b>%s</b></font></li>
              <li>Pays : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Langue : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Téléphone : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Fax : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>E-mail : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Date début séjour  : <font color='#ff9c1b'><b>%s</b>-<b>%s</b>-<b>%s</b></font></li>
              <li>Date fin séjour  : <font color='#ff9c1b'><b>%s</b>-<b>%s</b>-<b>%s</b></font></li>
              <li>Nombre de personne : <font color='#ff9c1b'><b>%s</b></font></li>
              <li>Remarque : <font color='#ff9c1b'><b>%s</b></font></li>
              </ul>
              """ \
              %(hebNom, \
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
        mailer.sendAllMail(mail.encode('utf-8'))

        translate = queryMultiAdapter((self.context, self.request),
                                       name='getTranslatedObjectUrl')

        if self.request.get('newsletter', False):
            url = translate('newsletter')
            self.request.RESPONSE.redirect(url)
        else:
            url = translate('mailsent')
            self.request.RESPONSE.redirect(url)
        return ''
