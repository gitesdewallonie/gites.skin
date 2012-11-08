# -*- coding: utf-8 -*-
import tempfile
from zope.interface import alsoProvides
from gites.skin.interfaces import (ISejourFuteRootFolder,
                                   IIdeeSejourRootFolder)
from zope.component import getMultiAdapter
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.app.portlets.portlets import (navigation)
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from zope.app.component.interfaces import ISite
from Products.LocalFS.LocalFS import manage_addLocalFS
from gites.skin.portlets import (sejourfute, derniereminute, ideesejour,
                                 laboutiquefolder, ideesejourfolder)
from gites.core.utils import (createFolder, publishObject, createPage,
                              setupClassicPortlet, getManager, clearPortlets)

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
    #setupLanguages(portal)
    createHebergement(portal)
    createContent(portal)
    createLocalFS(portal)
    setupHomePortlets(portal)


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


def changePageView(portal, page, viewname):
    addViewToType(portal, 'Document', viewname)
    if page.getLayout() != viewname:
        page.setLayout(viewname)


def blockParentPortlets(folder):
    manager = getManager(folder, 'left')
    assignable = getMultiAdapter((folder, manager), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

    manager = getManager(folder, 'right')
    assignable = getMultiAdapter((folder, manager), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)


def movePortlet(folder, name, column, position):
    #Change position order of portlet
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)

    keys = list(assignments.keys())
    keys.remove(name)
    keys.insert(position, name)
    assignments.updateOrder(keys)


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
    setupPortletsInIdeeSejour(ideeSejourFolder)
    associationFolder = getattr(folder, 'association')
    setupPortletsInAssociation(associationFolder)
    zoneMembreFolder = getattr(folder, 'zone-membre')
    setupPortletsInZoneMembre(zoneMembreFolder)


def setupPortletsInIdeeSejour(folder):
    blockParentPortlets(folder)
    setupRightColumnPortlets(folder)
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    if 'ideesejourfolder' not in assignments.keys():
        assignment = ideesejourfolder.Assignment('Idee sejour Folder')
        assignments['ideesejourfolder'] = assignment
    setupClassicPortlet(folder, 'portlet_outil', 'left')
    setupClassicPortlet(folder, 'portlet_partenaires', 'left')


def setupPortletsInZoneMembre(folder):
    blockParentPortlets(folder)
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    if 'navigation' not in assignments.keys():
        assignment = navigation.Assignment('Zone Membre')
        assignments['navigation'] = assignment


def setupPortletsInAssociation(folder):
    blockParentPortlets(folder)
    setupRightColumnPortlets(folder)
    setupClassicPortlet(folder, 'portlet_menu_association', 'left')
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

    # XXX see ticket http://trac.affinitic.be/trac/ticket/1466
    ideesSejourFolder = createFolder(portal, "idee-sejour", "Idées Séjours",
                                     True)
    associationFolder = createFolder(portal, "association", "Association",
                                     True)
    return

    sejourPage = createPage(ideesSejourFolder, "idees-sejours", "Idées Séjours")
    ideesSejourFolder.setDefaultPage('idees-sejours')
    ideesSejourFolder.setConstrainTypesMode(1)
    ideesSejourFolder.setLocallyAllowedTypes(['IdeeSejourFolder'])
    alsoProvides(ideesSejourFolder, IIdeeSejourRootFolder)
    changeFolderView(portal, ideesSejourFolder, 'ideesejour_root')

    gitesMeublesFolder = createFolder(portal, "gites-meubles", "Gîtes Meublés",
                                      True)
    createPage(gitesMeublesFolder, "gites-meubles", "Gîtes Meublés")
    gitesMeublesFolder.setDefaultPage("gites-meubles")

    chambresHotesFolder = createFolder(portal, "chambres-hotes",
                                       "Chambres d'Hôtes", True)
    createPage(chambresHotesFolder, "chambres-hotes", "Chambres d'Hôtes")
    chambresHotesFolder.setDefaultPage('chambres-hotes')

    createPage(associationFolder, "association", "Association")
    associationFolder.setDefaultPage("association")

    contactsFolder = createFolder(portal, "contacts", "Contacts", True)
    createPage(contactsFolder, "contacts", "Contacts")
    contactsFolder.setDefaultPage("contacts")

    coupleFolder = createFolder(portal, "couple", "Couple",
                                True)
    #createPage(coupleFolder, "couple", "Couple")
    coupleFolder.setDefaultPage("couple")

    familleFolder = createFolder(portal, "famille", "Famille", True)
    createPage(familleFolder, "famille", "Famille")
    familleFolder.setDefaultPage("famille")

    groupeFolder = createFolder(portal, "groupe", "Groupe", True)
    createPage(groupeFolder, "groupe", "Groupe")
    groupeFolder.setDefaultPage("Groupe")

    societeFolder = createFolder(portal, "societe", "Société", True)
    createPage(societeFolder, "societe", "Société")
    societeFolder.setDefaultPage("societe")

    decouvrirWallonieFolder = createFolder(portal, "decouvrir-wallonie",
                                           "Découvrir la Wallonie", True)
    createPage(decouvrirWallonieFolder, "decouvrir-wallonie", "Découvrir la Wallonie")
    decouvrirWallonieFolder.setDefaultPage("decouvrir-wallonie")

    proposerHebergementFolder = createFolder(portal, "proposer-hebergement",
                                             "Proposer votre Hébergement",
                                             True)
    createPage(proposerHebergementFolder, "proposer-hebergement",
               "Proposer votre Hébergement")
    proposerHebergementFolder.setDefaultPage("proposer-hebergement")

    coinPresseFolder = createFolder(portal, "coin-presse", "Coin Presse",
                                    True)
    createPage(coinPresseFolder, "coin-presse", "Coin Presse")
    coinPresseFolder.setDefaultPage("coin-presse")

    dernieresMinutesFolder = createFolder(portal, "dernieres-minutes",
                                          "Dernières Minutes", True)
    createPage(dernieresMinutesFolder, "dernieres-minutes", "Dernières Minutes")
    dernieresMinutesFolder.setDefaultPage("dernieres-minutes")
    dernieresMinutesFolder.setConstrainTypesMode(1)
    dernieresMinutesFolder.setLocallyAllowedTypes(['DerniereMinute'])

    preparerSejourFolder = createFolder(portal, "preparer-sejour",
                                        "Préparer votre Séjour", True)
    createPage(preparerSejourFolder, "preparer-sejour", "Préparer votre Séjour")
    preparerSejourFolder.setDefaultPage("preparer-sejour")

    proposerHebergementFolder = createFolder(portal, "proposer-hebergement",
                                             "Proposer votre Hébergement",
                                             True)
    createPage(proposerHebergementFolder, "proposer-hebergement", "Proposer votre Hébergement")
    proposerHebergementFolder.setDefaultPage("proposer-hebergement")

    mapFolder = createFolder(portal, "map", "Map", True)
    changeFolderView(portal, mapFolder, 'hebergement_map')

    signaletiquesFolder = createFolder(portal, "signaletiques", "Signalétiques",
                                       True)
    createPage(signaletiquesFolder, "signaletique-gites", "Signalétique gites")
    signaletiquesFolder.setDefaultPage("signaletiques")

    createPage(signaletiquesFolder, "signaletique-gite", "Signaletique Gites")
    createPage(signaletiquesFolder, "signaletique-chambre-hote", "Signaletique Gites")

    sejourFuteFolder = createFolder(portal, "sejour-fute", "Sejour Fute", True)
    sejourFuteFolder.setConstrainTypesMode(1)
    sejourFuteFolder.setLocallyAllowedTypes(['SejourFute'])
    alsoProvides(sejourFuteFolder, ISejourFuteRootFolder)
    changeFolderView(portal, sejourFuteFolder, 'sejourfute_root')

    associationFolder = portal.association
    createPage(associationFolder, "label-qualite", "Label Qualité")
    createPage(associationFolder, "objectifs", "Objectifs")
    createPage(associationFolder, "devenir-membre", "Devenir membre")
