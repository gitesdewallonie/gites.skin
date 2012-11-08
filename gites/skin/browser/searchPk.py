# -*- coding: utf-8 -*-
"""
GitesContent

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: searchPk.py 1901 2008-03-14 14:24:46Z jfroche $
"""
from five.formlib import formbase
from gites.skin import GitesMessage as _
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from gites.skin import GitesLocalesMessage as localTranslate
from interfaces import ISearchPk
from Products.CMFCore.utils import getToolByName
from zc.table.column import GetterColumn
from zc.table import table

class SearchPk(formbase.PageForm):
    """
    Search module to search hebergement among the site content
    """

    label = _("Search Hebergement by Pk in website")
    form_fields = form.FormFields(ISearchPk)

    template = ViewPageTemplateFile('templates/search_bypk.pt')

    def __init__(self, context, request):
        super(SearchPk, self).__init__(context, request)
        self.selectedItems = []

    @form.action(localTranslate(u"Search"))
    def action_search(self, action, data):
        pk = data.get('pk')
        cat = getToolByName(self.context, 'portal_catalog')
        self.selectedItems = []
        for sejourFuteBrain in cat(portal_type='SejourFute'):
            sejourFute = sejourFuteBrain.getObject()
            hebList = [int(i) for i in sejourFute.getHebergementsConcernes()]
            if pk in hebList:
                self.selectedItems.append(sejourFuteBrain)

        self.selectedIdeeSejour = []
        for ideeSejourBrain in cat(portal_type='IdeeSejour'):
            ideeSejour = ideeSejourBrain.getObject()
            hebList = [int(i) for i in ideeSejour.getHebergements()]
            if pk in hebList:
                self.selectedItems.append(ideeSejourBrain)

        self.selectedDerniereMinute = []
        for derniereMinuteBrain in cat(portal_type='DerniereMinute'):
            derniereMinute = derniereMinuteBrain.getObject()
            hebList = [int(i) for i in derniereMinute.getHebergementsConcernes()]
            if pk in hebList:
                self.selectedItems.append(derniereMinuteBrain)
        self.resetForm()
        self.update_status = ''

    def sortOn(self):
        return (("type", False),)

    def urlFormatter(self, value, item, formatter):
        return u'<a href="%s">%s</a>' % (item.getURL(),
                                         unicode(value, 'utf-8'))

    def columns(self):
        return [GetterColumn(name='title',
                             title=u"Title",
                             cell_formatter=self.urlFormatter,
                             getter=lambda i, f: i.Title,
                             subsort=True),
                GetterColumn(name='type',
                             title=u"Content Type",
                             getter=lambda i, f: i.meta_type,
                             subsort=True),]

    def renderTable(self):
        """
        """
        formatter = table.FormFullFormatter(
            self.context, self.request, self.selectedItems,
            columns=self.columns(),
            sort_on=self.sortOn())
        formatter.cssClasses['table'] = 'listing'
        return formatter()

