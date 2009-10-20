# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from zope.app.traversing.browser.interfaces import IAbsoluteURL
from Products.Five import BrowserView
from Acquisition import aq_inner, aq_parent
from zope.interface import implements
from zope.component import queryMultiAdapter
from DateTime import DateTime
from gites.skin.browser.interfaces import (IHebergementView,
                                           IHebergementIconsView)
from Products.CMFCore.utils import getToolByName
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.sqlalchemy import getSAWrapper


class HebergementView(BrowserView):
    """
    View for the full description of an hebergement
    """
    implements(IHebergementView)
    template = ViewPageTemplateFile("templates/hebergement.pt")

    def getHebergementByProprietaire(self, proprioFk):
        """
        Sélectionne les infos d'un proprio selon son login
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        hebergementTable = wrapper.getMapper('hebergement')
        query = session.query(hebergementTable)
        query = query.filter(hebergementTable.heb_pro_fk == proprioFk)
        hebergement = query.all()
        return hebergement

    def getTypeHebergement(self):
        """
        Get the hebergement type title translated
        """
        language = self.request.get('LANGUAGE', 'en')
        return self.context.type.getTitle(language)

    def getHebergementSituation(self):
        """
        Get the hebergement type title translated
        """
        language = self.request.get('LANGUAGE', 'en')
        return self.context.getSituation(language)

    def getHebergementDescription(self):
        """
        Get the hebergement type title translated
        """
        language = self.request.get('LANGUAGE', 'en')
        return self.context.getDescription(language)

    def getHebergementCharge(self):
        """
        Get the hebergement type title translated
        """
        language = self.request.get('LANGUAGE', 'en')
        return self.context.charge.getTitle(language)

    def getHebergementDistribution(self):
        """
        Get the hebergement type title translated
        """
        language = self.request.get('LANGUAGE', 'en')
        return self.context.getDistribution(language)

    def getHebergementSeminaireVert(self):
        """
        Get the hebergement seminaire vert information translated
        """
        language = self.request.get('LANGUAGE', 'en')
        return self.context.getSeminaireVert(language)

    def getTypeHebInCommuneURL(self):
        """
        Get the commune and type hebergement URL
        """
        hebURL = queryMultiAdapter((self.context, self.request), name="url")
        urlList= str(hebURL).split('/')
        urlList.pop()
        return '/'.join(urlList)

    def getRelatedSejourFute(self):
        """
        Get Sejour Fute related to this hebergement
        """
        self.cat = getToolByName(self.context, 'portal_catalog')
        pk = self.context.heb_pk
        results = self.cat.searchResults(portal_type='SejourFute',
                                         end={'query': DateTime(),
                                              'range': 'min'},
                                         review_state='published')
        relatedSejour = []
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        MaisonTourisme = wrapper.getMapper('maison_tourisme')
        for result in results:
            sejour = result.getObject()
            hebs = [int(heb_pk) for heb_pk in sejour.getHebergementsConcernes()]
            maisonTourismes = [int(i) for i in sejour.getMaisonsTourisme()]
            hebergements = []
            for maisonTourisme in maisonTourismes:
                maison = session.query(MaisonTourisme).get(maisonTourisme)
                for commune in maison.commune:
                    hebergements += list(commune.relatedHebergement)
            hebs += [heb.heb_pk for heb in hebergements]
            if pk in hebs:
                relatedSejour.append(sejour)
        return relatedSejour

    def render(self):
        return self.template()


class HebergementIconsView(BrowserView):
    """
    View for the icons of an hebergement
    """
    implements(IHebergementIconsView)

    def getSignaletiqueUrl(self):
        """
        return the url of the signaletique
        """
        url = getToolByName(self.context, 'portal_url')()
        translate = queryMultiAdapter((self.context, self.request),
                                       name='getTranslatedObjectUrl')
        if self.context.type.type_heb_code in ['CH', 'MH', 'CHECR']:
            url = translate('signaletiques/signaletique-chambre-hote')
        else:
            url = translate('signaletiques/signaletique-gite')
        return url

    def getEpisIcons(self, number):
        result = []
        url = getToolByName(self.context, 'portal_url')()
        if self.context.type.type_heb_code in ['MV']:
            for i in range(number):
                result.append('<img src="1_clef.png" src="%s1_clef.png"/>' % url)
        else:
            for i in range(number):
                result.append('<img src="1_epis.gif" src="%s1_epis.gif"/>' % url)
        return " ".join(result)

    def getEpis(self):
        """
        Get the epis icons
        """
        l = [self.getEpisIcons(i.heb_nombre_epis) for i in self.context.epis]
        return " - ".join(l)


class HebergementAbsoluteURL(BrowserView):
    implements(IAbsoluteURL)

    def __str__(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        commune = context.commune.com_id
        language = self.request.get('LANGUAGE', 'en')
        typeHeb = context.type.getId(language)
        hebId = context.heb_id
        return "%s/%s/%s/%s" % (container.absolute_url(),
                             typeHeb,
                             commune,
                             hebId,
                             )

    __call__ = __str__


class HebergementMapView(BrowserView):
    """
    Methods useful for the maps
    """

    def getJs(self):
        """
        return the js code to set the longitude in the map
        """
        language = self.request.get('LANGUAGE', 'en')
        long = self.request.form.get('long', None)
        lat = self.request.form.get('lat', None)
        pk = self.request.form.get('pk', None)
        url = getToolByName(self.context, 'portal_url')()
        if long and lat and pk:
            js = """
              var so = new SWFObject("gitesmap.swf","Gites","934","549","9","#ffffff");
              so.addVariable("externalLanguage", "%s");
              so.addVariable("externalLat", "%s");
              so.addVariable("externalLon", "%s");
              so.addVariable("externalPk", "%s");
              so.addVariable("externalURL","%s")
              so.write("flashcontent");
          """ % (language, long, lat, pk, url)
        else:
            js = """
              var so = new SWFObject("gitesmap.swf","Gites","934","549","9","#ffffff");
              so.addVariable("externalLanguage", "%s");
              so.addVariable("externalURL","%s")
              so.write("flashcontent");
          """ % (language, url)
        return js
