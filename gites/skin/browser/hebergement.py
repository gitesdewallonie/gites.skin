# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from urlparse import urljoin
from plone.memoize.instance import memoize
from zope.traversing.browser.interfaces import IAbsoluteURL
from Products.Five import BrowserView
from Acquisition import aq_inner, aq_parent
from zope.interface import implements
from zope.component import queryMultiAdapter
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.sqlalchemy import getSAWrapper

from gites.map.browser.interfaces import IMappableView
from gites.skin.browser.interfaces import (IHebergementView,
                                           IHebergementIconsView)


class HebergementView(BrowserView):
    """
    View for the full description of an hebergement
    """
    implements(IHebergementView, IMappableView)
    template = ViewPageTemplateFile("templates/hebergement.pt")

    def __init__(self, context, request):
        super(HebergementView, self).__init__(context, request)
        super(BrowserView, self).__init__(context, request)

    def calendarJS(self):
        """
        Calendar javascript
        """
        return """
        //<![CDATA[
            calsetup = function() {
                jQuery.noConflict();
                new GiteTimeframe('calendars', {
                                startField: 'start',
                                endField: 'end',
                                resetButton: 'reset',
                                weekOffset: 1,
                                hebPk: %s,
                                months:1,
                                language: '%s',
                                earliest: new Date()});}
            registerPloneFunction(calsetup);
        //]]>

        """ % (self.context.heb_pk,
               self.request.get('LANGUAGE', 'en'))

    def showCalendar(self):
        """
        Is the calendar activated for showing in description ?
        (if the calendar has been blocked due to inactivity, it will not
        appear because heb_calendrier_proprio will be 'bloque' by cron)
        """
        return (self.context.heb_calendrier_proprio == 'actif')

    def getCustomStylesheet(self):
        """
        Returns referer stylesheet URL where proprio can customize calendar
        CSS
        """
        referer = self.request.get('HTTP_REFERER', None)
        customCssUrl = urljoin(referer, 'calendar-custom.css')
        return customCssUrl

    def redirectInactive(self):
        """
        Redirect if gites / proprio is not active
        """
        if self.context.heb_site_public == '0' or \
           self.context.proprio.pro_etat == False:
            url = getToolByName(self.context, 'portal_url')()
            return self.request.response.redirect(url)

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

    @memoize
    def getHebergementDescription(self):
        """
        Get the hebergement type title translated
        """
        language = self.request.get('LANGUAGE', 'en')
        return self.context.getDescription(language)

    @memoize
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
        urlList = str(hebURL).split('/')
        urlList.pop()
        return '/'.join(urlList)

    @memoize
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
        for result in results:
            sejour = result.getObject()
            if pk in sejour.getHebPks():
                relatedSejour.append(sejour)
        return relatedSejour

    def getHebMetadatasByType(self, metadataType):
        """
        Return all metadata objects corresponding on metadataType
        cf: table metadata column metadata_type_id
        """
        heb = self.context
        dics = []
        language = self.request.get('LANGUAGE')
        for md in heb.activeMetadatas:
            if md.metadata_type_id == metadataType:
                dics.append({"id":md.met_id,"title":md.getTitre(language)})
        return dics

    def getAnimal(self):
        list = self.getHebMetadatasByType('autorisations')
        for item in list:
            if item['id'] == 'heb_animal':
                return item
        return {"id":"heb_no_animal","title":"NON CHIEN"}

    def getFumeur(self):
        list = self.getHebMetadatasByType('autorisations')
        for item in list:
            if item['id'] == 'heb_fumeur':
                return item
        return {"id":"heb_no_fumeur","title":"NON FUMEUR"}

    def render(self):
        return self.template()

    def getVignettesUrl(self):
        """
        Get the vignette of an hebergement
        """
        vignettes=[]
        codeGDW = self.context.heb_code_gdw
        listeImage = self.context.photos_heb.fileIds()
        for i in range(15):
            if i < 10:
                photo="%s0%s.jpg"%(codeGDW,i)
            else:
                photo="%s%s.jpg"%(codeGDW, i)
            if photo in listeImage:
                vignettes.append(photo)
        return vignettes


class HebergementExternCalendarView(HebergementView):
    """
    View for extern calendars
    """
    implements(IHebergementView)
    template = ViewPageTemplateFile("templates/externcalendar.pt")

    def __init__(self, context, request):
        hebPk = request.get('pk')
        hebergement = self.getHebergementByPk(hebPk)
        self.context = hebergement
        super(HebergementExternCalendarView, self).__init__(self.context, request)
        super(HebergementView, self).__init__(self.context, request)

    def getHebergementByPk(self, heb_pk):
        """
        Get the url of the hebergement by Pk
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        HebTable = wrapper.getMapper('hebergement')
        try:
            int(heb_pk)
        except ValueError:
            return None
        hebergement = session.query(HebTable).get(heb_pk)
        if hebergement and \
           int(hebergement.heb_site_public) == 1 and \
           hebergement.proprio.pro_etat:
           # L'hébergement doit être actif, ainsi que son propriétaire
            # hebURL = queryMultiAdapter((hebergement.__of__(self.context.hebergement), self.request), name="url")
            return hebergement
        else:
            return None

    def calendarJS(self):
        """
        Calendar javascript
        """
        return """
        //<![CDATA[
            new GiteTimeframe('calendars', {
                            startField: 'start',
                            endField: 'end',
                            resetButton: 'reset',
                            weekOffset: 1,
                            hebPk: %s,
                            months:1,
                            language: '%s',
                            earliest: new Date()});
        //]]>

        """ % (self.context.heb_pk, 'fr')


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
