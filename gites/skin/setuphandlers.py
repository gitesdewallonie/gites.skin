# -*- coding: utf-8 -*-
import tempfile
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.app.portlets.portlets import classic
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from zope.app.component.interfaces import ISite
from Products.LocalFS.LocalFS import manage_addLocalFS
from gites.skin.portlets import (sejourfute, derniereminute, ideesejour,
                                 laboutiquefolder, ideesejourfolder)


import logging
logger = logging.getLogger('gites.skin')

LANGUAGES = ['en', 'nl', 'fr', 'it', 'de']


def setupgites(context):
    if context.readDataFile('gites.skin_various.txt') is None:
        return
    logger.debug('Setup gites skin')
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    setupLanguages(portal)
    createHebergement(portal)
    createContent(portal)
    setupHomePortlets(portal)
    createLocalFS(portal)


def createHebergement(portal):
    if 'hebergement' not in portal.objectIds():
        portal.invokeFactory('HebergementFolder', 'hebergement')
    createdFolder = getattr(portal, 'hebergement')
    createdFolder.reindexObject()
    publishObject(createdFolder)
    createdFolder.reindexObject()
    createdFolder.update()


def createLocalFS(portal):
    if 'photos_heb' not in portal.objectIds():
        manage_addLocalFS(portal, 'photos_heb', 'Photos heb',
                          tempfile.gettempdir())


def publishObject(obj):
    portal_workflow = getToolByName(obj, 'portal_workflow')
    if portal_workflow.getInfoFor(obj, 'review_state') in ['visible', 'private']:
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
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]


def clearPortlets(folder):
    clearColumnPortlets(folder, 'left')
    clearColumnPortlets(folder, 'right')


def blockParentPortlets(folder):
    manager = getManager(folder, 'left')
    assignable = getMultiAdapter((folder, manager), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

    manager = getManager(folder, 'right')
    assignable = getMultiAdapter((folder, manager), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)


def setupClassicPortlet(folder, template, column):
    #Add classic portlet (using template) to folder
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)

    assignment = classic.Assignment(template=template, macro='portlet')
    if template in assignments:
        del assignments[template]
    assignments[template] = assignment


def movePortlet(folder, name, column, position):
    #Change position order of portlet
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)

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
        if not enObject.hasTranslation(lang):
            translated = enObject.addTranslation(lang)
            publishObject(translated)
            translated.reindexObject()
            translatedObjects.append(translated)
    return translatedObjects


def setupHomePortlets(folder):
    #Creates portlets columns for root pages
    clearPortlets(folder)
    blockParentPortlets(folder)
    setupClassicPortlet(folder, 'portlet_je_suis', 'left')
    setupClassicPortlet(folder, 'portlet_outil', 'left')
    setupClassicPortlet(folder, 'portlet_partenaires', 'left')
    setupRightColumnPortlets(folder)
    ideeSejourFolder = getattr(folder, 'idee-sejour')
    setupPortlesInIdeeSejour(ideeSejourFolder)


def setupPortlesInIdeeSejour(folder):
    blockParentPortlets(folder)
    setupRightColumnPortlets(folder)
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    if 'ideesejourfolder' not in assignments.keys():
        assignment = ideesejourfolder.Assignment('Idee sejour Folder')
        assignments['ideesejourfolder'] = assignment
    setupClassicPortlet(folder, 'portlet_outil', 'left')
    setupClassicPortlet(folder, 'portlet_partenaires', 'left')


def setupRightColumnPortlets(folder):
    manager = getManager(folder, 'right')
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    if 'sejourfute' not in assignments.keys():
        assignment = sejourfute.Assignment('Sejour Fute')
        assignments['sejourfute'] = assignment
    if 'derniereminute' not in assignments.keys():
        assignment = derniereminute.Assignment('Derniere minute')
        assignments['derniereminute'] = assignment
    if 'ideesejour' not in assignments.keys():
        assignment = ideesejour.Assignment('Idee sejour')
        assignments['ideesejour'] = assignment
    if 'laboutique' not in assignments.keys():
        assignment = laboutiquefolder.Assignment('La boutique')
        assignments['laboutique'] = assignment


def createContent(portal):
    #Create empty documents and folders

    ideesSejourFolder = createFolder(portal, "idee-sejour", "Idées Séjours",
                                     True)
    createPage(ideesSejourFolder, "idees-sejours", "Idées Séjours")
    ideesSejourFolder.setDefaultPage('idees-sejours')
    createTranslationsForObject(ideesSejourFolder)
    ideesSejourFolder.setConstrainTypesMode(1)
    ideesSejourFolder.setLocallyAllowedTypes(['IdeeSejourFolder'])

    gitesMeublesFolder = createFolder(portal, "gites-meubles", "Gîtes Meublés",
                                      True)
    createPage(gitesMeublesFolder, "gites-meubles", "Gîtes Meublés")
    gitesMeublesFolder.setDefaultPage("gites-meubles")
    createTranslationsForObject(gitesMeublesFolder)

    chambresHotesFolder = createFolder(portal, "chambres-hotes",
                                       "Chambres d'Hôtes", True)
    createPage(chambresHotesFolder, "chambres-hotes", "Chambres d'Hôtes")
    chambresHotesFolder.setDefaultPage('chambres-hotes')
    createTranslationsForObject(chambresHotesFolder)

    associationFolder = createFolder(portal, "association", "Association",
                                     True)
    createPage(associationFolder, "association", "Association")
    associationFolder.setDefaultPage("association")
    createTranslationsForObject(associationFolder)

    contactsFolder = createFolder(portal, "contacts", "Contacts", True)
    createPage(contactsFolder, "contacts", "Contacts")
    contactsFolder.setDefaultPage("contacts")
    createTranslationsForObject(contactsFolder)

    coupleFolder = createFolder(portal, "couple", "Couple",
                                True)
    createPage(coupleFolder, "couple", "Couple")
    coupleFolder.setDefaultPage("couple")
    createTranslationsForObject(coupleFolder)

    familleFolder = createFolder(portal, "famille", "Famille", True)
    createPage(familleFolder, "famille", "Famille")
    familleFolder.setDefaultPage("famille")
    createTranslationsForObject(familleFolder)

    groupeFolder = createFolder(portal, "groupe", "Groupe", True)
    createPage(groupeFolder, "groupe", "Groupe")
    groupeFolder.setDefaultPage("Groupe")
    createTranslationsForObject(groupeFolder)

    societeFolder = createFolder(portal, "societe", "Société", True)
    createPage(societeFolder, "societe", "Société")
    societeFolder.setDefaultPage("societe")
    createTranslationsForObject(societeFolder)

    decouvrirWallonieFolder = createFolder(portal, "decouvrir-wallonie",
                                           "Découvrir la Wallonie", True)
    createPage(decouvrirWallonieFolder, "decouvrir-wallonie", "Découvrir la Wallonie")
    decouvrirWallonieFolder.setDefaultPage("decouvrir-wallonie")
    createTranslationsForObject(decouvrirWallonieFolder)

    proposerHebergementFolder = createFolder(portal, "proposer-hebergement",
                                             "Proposer votre Hébergement",
                                             True)
    createPage(proposerHebergementFolder, "proposer-hebergement",
               "Proposer votre Hébergement")
    proposerHebergementFolder.setDefaultPage("proposer-hebergement")
    createTranslationsForObject(proposerHebergementFolder)

    coinPresseFolder = createFolder(portal, "coin-presse", "Coin Presse",
                                    True)
    createPage(coinPresseFolder, "coin-presse", "Coin Presse")
    coinPresseFolder.setDefaultPage("coin-presse")
    createTranslationsForObject(coinPresseFolder)

    dernieresMinutesFolder = createFolder(portal, "dernieres-minutes",
                                          "Dernières Minutes", True)
    createPage(dernieresMinutesFolder, "dernieres-minutes", "Dernières Minutes")
    dernieresMinutesFolder.setDefaultPage("dernieres-minutes")
    createTranslationsForObject(dernieresMinutesFolder)
    ideesSejourFolder.setConstrainTypesMode(1)
    ideesSejourFolder.setLocallyAllowedTypes(['DerniereMinute'])

    preparerSejourFolder = createFolder(portal, "preparer-sejour",
                                        "Préparer votre Séjour", True)
    createPage(preparerSejourFolder, "preparer-sejour", "Préparer votre Séjour")
    preparerSejourFolder.setDefaultPage("preparer-sejour")
    createTranslationsForObject(preparerSejourFolder)

    proposerHebergementFolder = createFolder(portal, "proposer-hebergement",
                                             "Proposer votre Hébergement",
                                             True)
    createPage(proposerHebergementFolder, "proposer-hebergement", "Proposer votre Hébergement")
    proposerHebergementFolder.setDefaultPage("proposer-hebergement")
    createTranslationsForObject(proposerHebergementFolder)

    mapFolder = createFolder(portal, "map", "Map", True)
    createPage(mapFolder, "map", "Map")
    mapFolder.setDefaultPage("map")
    createTranslationsForObject(mapFolder)

    signaletiquesFolder = createFolder(portal, "signaletiques", "Signalétiques",
                                       True)
    createPage(signaletiquesFolder, "signaletique-gites", "Signalétique gites")
    signaletiquesFolder.setDefaultPage("signaletiques")
    createTranslationsForObject(signaletiquesFolder)

    createPage(signaletiquesFolder, "signaletique-gite", "Signaletique Gites")
    createPage(signaletiquesFolder, "signaletique-chambre-hote", "Signaletique Gites")

    sejourFuteFolder = createFolder(portal, "sejour-fute", "Sejour Fute", True)
    sejourFuteFolder.setConstrainTypesMode(1)
    sejourFuteFolder.setLocallyAllowedTypes(['SejourFute'])
