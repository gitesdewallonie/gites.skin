# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.app.portlets.portlets import classic
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from Products.LinguaPlone.I18NBaseObject import AlreadyTranslated
from zope.app.component.interfaces import ISite


import logging
logger = logging.getLogger('gites.skin')

LANGUAGES = ['en', 'nl', 'fr', 'it', 'de']


def setupgites(context):
    logger.debug('Setup gites skin')
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    #setupNewsletter(portal)
    setupLanguages(portal)
    #setupHomePortlets(portal)
    #setupSimpleNavigationPortlet(portal, 'left')
    createContent(portal)

def publishObject(obj):
    portal_workflow = getToolByName(obj, 'portal_workflow')
    if portal_workflow.getInfoFor(obj, 'review_state') in ['visible','private']:
        portal_workflow.doActionFor(obj, 'publish')
    return

def setupLanguages(portal):
    lang = getToolByName(portal, 'portal_languages')
    lang.supported_langs = LANGUAGES
    lang.setDefaultLanguage('fr')
    lang.display_flags = 0

def setupNewsletter(folder):
    newsletterId = 'newsletter'
    if newsletterId not in folder.objectIds():
        newsletterId = folder.invokeFactory('MailmanSubForm', 'newsletter')
    newsletter = getattr(folder, newsletterId)
    publishObject(newsletter)
    newsletter.reindexObject()

def getManager(folder, column):
    if column == 'left':
        manager = getUtility(IPortletManager, name=u'plone.leftcolumn', context=folder)
    else:
        manager = getUtility(IPortletManager, name=u'plone.rightcolumn', context=folder)
    return manager

def addViewToType(portal, typename, templatename):
    pt = getToolByName(portal, 'portal_types')
    foldertype = getattr(pt, typename)
    available_views = list(foldertype.getAvailableViewMethods(portal))
    if not templatename in available_views:
        available_views.append(templatename)
        foldertype.manage_changeProperties(view_methods=available_views)

def changeFolderView(portal, folder, viewname):
    addViewToType(portal, 'Folder', viewname)
    if folder.getLayout() != viewname:
        folder.setLayout(viewname)

def clearColumnPortlets(folder, column):
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]

def clearPortlets(folder):
    clearColumnPortlets(folder, 'left')
    clearColumnPortlets(folder, 'right')

def blockParentPortlets(folder):
    manager = getManager(folder, 'left')
    assignable = getMultiAdapter((folder, manager,), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

    manager = getManager(folder, 'right')
    assignable = getMultiAdapter((folder, manager,), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

def setupSubNavigationPortlet(folder):
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)

    assignment = navigation.Assignment(name=u"Navigation",
                                       root=None,
                                       currentFolderOnly=False,
                                       includeTop=False,
                                       topLevel=1,
                                       bottomLevel=0)
    assignments['navtree'] = assignment
    setupClassicPortlet(folder, 'portlet_sub_menus', 'left')

def setupSimpleNavigationPortlet(folder, column):
    #Add simple navigation portlet to folder
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)
    assignment = navigation.Assignment()
    assignments['msmile_navigation'] = assignment

def setupClassicPortlet(folder, template, column):
    #Add classic portlet (using template) to folder
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)

    assignment = classic.Assignment(template=template, macro='portlet')
    if assignments.has_key(template):
        del assignments[template]
    assignments[template] = assignment

def movePortlet(folder, name, column, position):
    #Change position order of portlet
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)

    keys = list(assignments.keys())
    idx = keys.index(name)
    keys.remove(name)
    keys.insert(position, name)
    assignments.updateOrder(keys)

def createPage(parentFolder, documentId, documentTitle):
    if documentId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Document', documentId, title=documentTitle)
    document = getattr(parentFolder, documentId)
    #By default, created page are written in English
    #XXX bug here : document.setLanguage('en')
    publishObject(document)
    return document

def createFolder(parentFolder, folderId, folderTitle, excludeNav):
    if folderId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Folder', folderId, title=folderTitle, excludeFromNav=excludeNav)
    createdFolder = getattr(parentFolder, folderId)
    createdFolder.reindexObject()
    createdFolder.exclude_from_nav=excludeNav
    createdFolder.reindexObject()
    publishObject(createdFolder)
    createdFolder.reindexObject()
    return createdFolder
    
def createTranslationsForObject(enObject):
        translatedObjects = []

        for lang in LANGUAGES:
            try:
                enObject.addTranslation(lang)
            except AlreadyTranslated:
                pass
            translated = enObject.getTranslation(lang)
            publishObject(translated)
            translated.reindexObject()
            translatedObjects.append(translated)

        return translatedObjects

def setupHomePortlets(folder):
    #Creates portlets columns for root pages
    clearPortlets(folder)
    blockParentPortlets(folder)
    setupClassicPortlet(folder, 'navigation', 'left')


#def setupInternalPortlets(folder):
    #Creates the left portlet column for all internal pages
#    clearPortlets(folder)
#    blockParentPortlets(folder)
#    setupClassicPortlet(folder, 'portlet_left_header', 'left')
#    movePortlet(folder, 'portlet_left_header', 'left', 0)

def createContent(portal):
    #Create empty documents and folders

    
    ideesSejourFolder = createFolder(portal, "idees-sejour", "Idées Séjours",True)
    createPage(ideesSejourFolder, "idees-sejour", "Idées Séjours")
    ideesSejourFolder.setDefaultPage('idees-sejour')
    createTranslationsForObject(ideesSejourFolder)

    gitesMeublesFolder = createFolder(portal, "gites-meubles", "Gîtes Meublés",True)
    createPage(gitesMeublesFolder, "gites-meubles", "Gîtes Meublés")
    gitesMeublesFolder.setDefaultPage("gites-meubles")
    createTranslationsForObject(gitesMeublesFolder)

    chambresHotesFolder = createFolder(portal, "chambres-hotes", "Chambres d'Hôtes",True)
    createPage(chambresHotesFolder, "chambres-hotes", "Chambres d'Hôtes")
    chambresHotesFolder.setDefaultPage('chambres-hotes')
    createTranslationsForObject(chambresHotesFolder)

    associationFolder = createFolder(portal, "association", "Association",True)
    createPage(associationFolder, "association", "Association")
    associationFolder.setDefaultPage("association")
    createTranslationsForObject(associationFolder)

    contactsFolder = createFolder(portal, "contacts", "Contacts",True)
    createPage(contactsFolder, "contacts", "Contacts")
    contactsFolder.setDefaultPage("contacts")
    createTranslationsForObject(contactsFolder)

    coinPresseFolder = createFolder(portal, "coin-presse", "Coin Presse",True)
    createPage(coinPresseFolder, "coin-presse", "Coin Presse")
    coinPresseFolder.setDefaultPage("coin-presse")
    createTranslationsForObject(coinPresseFolder)

    coupleFolder = createFolder(portal, "couple", "Couple",True)
    createPage(coupleFolder, "couple", "Couple")
    coupleFolder.setDefaultPage("couple")
    createTranslationsForObject(coupleFolder)

    decouvrirWallonieFolder = createFolder(portal, "decouvrir-wallonie", "Découvrir la Wallonie",True)
    createPage(decouvrirWallonieFolder, "decouvrir-wallonie", "Découvrir la Wallonie")
    decouvrirWallonieFolder.setDefaultPage("decouvrir-wallonie")
    createTranslationsForObject(decouvrirWallonieFolder)

    dernieresMinutesFolder = createFolder(portal, "dernieres-minutes", "Dernières Minutes",True)
    createPage(dernieresMinutesFolder, "dernieres-minutes", "Dernières Minutes")
    dernieresMinutesFolder.setDefaultPage("dernieres-minutes")
    createTranslationsForObject(dernieresMinutesFolder)

    preparerSejourFolder = createFolder(portal, "preparer-sejour", "Préparer votre Séjour",True)
    createPage(preparerSejourFolder, "preparer-sejour", "Préparer votre Séjour")
    preparerSejourFolder.setDefaultPage("preparer-sejour")
    createTranslationsForObject(preparerSejourFolder)

    proposerHebergementFolder = createFolder(portal, "proposer-hebergement", "Proposer votre Hébergement",True)
    createPage(proposerHebergementFolder, "proposer-hebergement", "Proposer votre Hébergement")
    proposerHebergementFolder.setDefaultPage("proposer-hebergement")
    createTranslationsForObject(proposerHebergementFolder)

    proposerHebergementFolder = createFolder(portal, "proposer-hebergement", "Proposer votre Hébergement",True)
    createPage(proposerHebergementFolder, "proposer-hebergement", "Proposer votre Hébergement")
    proposerHebergementFolder.setDefaultPage("proposer-hebergement")
    createTranslationsForObject(proposerHebergementFolder)
