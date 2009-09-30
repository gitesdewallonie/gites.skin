# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: viewlets.py 4587 2009-02-22 22:32:37Z alain
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from zope.component import getMultiAdapter
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from plone.app.i18n.locales.browser.selector import LanguageSelector
from plone.app.layout.navigation.defaultpage import isDefaultPage

from Acquisition import aq_inner
from Acquisition import aq_parent

from Products.LinguaPlone.interfaces import ITranslatable
from ZTUtils import make_query


class GitesSectionsViewlet(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/header_gites.pt')

    def logo_tag(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        portal = portal_state.portal()
        logoName = portal.restrictedTraverse('base_properties').logoName
        return portal.restrictedTraverse(logoName).tag()


class GitesFooterViewlet(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/footer_gites.pt')


class GitesMoteurRechercheViewlet(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/moteur_recherche.pt')


class ApplicaTranslatableLanguageSelector(TranslatableLanguageSelector):
    """Language selector for translatable content.
    """
    render = ViewPageTemplateFile('templates/language_selector.pt')

    def languages(self):
        context = aq_inner(self.context)
        results = LanguageSelector.languages(self)
        translatable = ITranslatable(context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

        # We want to preserve the current template / view as used for the
        # current object and also use it for the other languages

        # We need to find the actual translatable content object. As an
        # optimization we assume it is one of the last two path segments
        match = filter(None, context.getPhysicalPath()[-2:])
        current_path = filter(None, self.request.get('PATH_INFO', '').split('/'))
        append_path = []
        stop = False
        while current_path and not stop:
            check = current_path.pop()
            if check not in match:
                append_path.insert(0, check)
            else:
                stop = True
        #XXX we remove virtualhostroot
        if 'VirtualHostRoot' in append_path:
            append_path.remove('VirtualHostRoot')
        if append_path:
            append_path.insert(0, '')
        formvariables = self.request.form
        for k, v in formvariables.items():
            if isinstance(v, unicode):
                formvariables[k] = v.encode('utf-8')
        for data in results:
            data['translated'] = data['code'] in translations

            try:
                appendtourl = '/'.join(append_path) + \
                          '?' + make_query(formvariables, dict(set_language=data['code']))
            except UnicodeError:
                appendtourl = '/'.join(append_path) + '?set_language=' + data['code']

            if data['translated']:
                trans = translations[data['code']][0]
                container = aq_parent(trans)
                if isDefaultPage(container, trans):
                    trans = container
                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + appendtourl
            else:
                container = aq_parent(context)
                if isDefaultPage(container, context):
                    context = container
                state = getMultiAdapter((context, self.request),
                        name='plone_context_state')
                try:
                    data['url'] = state.view_url() + appendtourl
                except AttributeError:
                    data['url'] = context.absolute_url() + appendtourl

        return results
