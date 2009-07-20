# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from z3c.sqlalchemy import getSAWrapper
from zope.component import queryMultiAdapter

#from sqlalchemy import Table
#from sqlalchemy import select

class MoteurRecherche(BrowserView):

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
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            return queryMultiAdapter((portal, self.request),
                                      name="unknown_gites")()
        hebergement = session.query(HebTable).get(heb_pk)
        if hebergement:
            hebURL = queryMultiAdapter((hebergement.__of__(self.context.hebergement), self.request), name="url")
            return self.request.RESPONSE.redirect(str(hebURL))
        else:
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            return queryMultiAdapter((portal, self.request),
                                       name="unknown_gites")()

    def getGroupedHebergementTypes(self):
        """
        retourne les deux groupes de types d'hebergements
        """
        # get some translation interfaces

        translation_service = getToolByName(self.context,
                                            'translation_service')

        utranslate = translation_service.utranslate
        lang = self.request.get('LANGUAGE', 'en')
        return [{'pk': -2,
                 'name': utranslate('gites', "Gites et Meubles",
                                    context=self.context,
                                    target_language=lang,
                                    default="Gites")},
                {'pk': -3,
                 'name': utranslate('gites', "Chambre d'hote",
                                    context=self.context,
                                    target_language=lang,
                                    default="Chambre d'hote")}]

    def getHebergementTypes(self):
        """
        retourne les types d hebergements
        table type_heb
        """
        wrapper = getSAWrapper('gites_wallons')
        session = wrapper.session
        TypeHeb = wrapper.getMapper('type_heb')
        results = session.query(TypeHeb).select()
        language = self.request.get('LANGUAGE', 'en')
        typesList = []
        for typeHeb in results:
            types = {}
            types['pk'] = typeHeb.type_heb_pk
            types['name'] = typeHeb.getTitle(language)
            typesList.append(types)
        return typesList
