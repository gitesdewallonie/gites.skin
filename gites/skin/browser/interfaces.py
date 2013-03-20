# -*- coding: utf-8 -*-
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface
from zope import schema
from gites.skin import GitesMessage as _


class IGitesTheme(IDefaultPloneLayer):
    """
    Marker interface that defines a Zope 3 browser layer.
    """


class IMeublesView(Interface):
    """
    """

    def getMeubles():
        """
        return the meubles in the folder
        """


class ILogoView(Interface):
    """
    Logo
    """

    def getLogoUrl():
        """
        return the default url of the logo
        """

    def getButton(image):
        """
        Return correct button regarding language
        """


class IMoteurRecherche(Interface):

    def getHebergementByNameOrPk(reference):
        """
        Get the url of the hebergement by Pk or part of the name
        """

    def getHebergementTypes():
        """
        retourne les types d hebergements
        """

    def getGroupedHebergementTypes():
        """
        retourne les deux groupes de types d hebergements
        """


class IHebergementView(Interface):
    """
    View for the full description of an hebergement
    """

    def redirectInactive():
        """
        Redirect if gites / proprio is not active
        """

    def getTypeHebergement():
        """
        Get the hebergement type title translated
        """

    def getHebergementSituation():
        """
        Get the hebergement type title translated
        """

    def getHebergementDescription():
        """
        Get the hebergement type title translated
        """

    def getHebergementDistribution():
        """
        Get the hebergement type title translated
        """

    def getHebergementSeminaireVert():
        """
        Get the hebergement seminaire vert information translated
        """

    def getHebergementCharge():
        """
        Get the hebergement type title translated
        """

    def getTypeHebInCommuneURL():
        """
        Get the commune and type hebergement URL
        """

    def getRelatedSejourFute():
        """
        Get Sejour Fute related to this hebergement
        """


class IHebergementGallery(Interface):
    """
    Affichage de la galerie
    """

    def getVignettesUrl():
        """
        Get the vignette of an hebergement
        """

    def redirectInactive():
        """
        Redirect if gites / proprio is not active
        """


class IHebergementIconsView(Interface):
    """
        View for the icons of an hebergement
    """

    def getEpis():
        """
        Get the epis icons
        """

    def getSignaletiqueUrl():
        """
        return the url of the signaletique
        """


class ITypeHebCommuneView(Interface):
    """
    Vue sur un type d hebergement et une commune
    """

    def typeHebergementName():
        """
        Get the hebergement type title translated
        """

    def communeName():
        """
        Get the name of the commune
        """

    def getHebergements():
        """
        Return the concerned hebergements in this Town for the selected
        type of hebergement
        """


class ISendMail(Interface):
    """
    Send Mail
    """

    def sendBlogSubscriptionMail():
        """
        envoi des informations d'inscription à la newsletter du blog
        """

    def sendMailToProprio():
        """
        Envoi un mail au proprio via le site
        """


class ISearchHebergement(Interface):
    """
    A search module to search hebergement
    """

    hebergementType = schema.Choice(title=_("Hebergement Type"),
                                    description=_("Select a type of Hebergement"),
                                    required=True,
                                    vocabulary="gitescontent.typehebergement")

    provinces = schema.Choice(
            title=_('Province'),
            description=_("Select a province"),
            required=True,
            vocabulary="gitescontent.provinces")

    communes = schema.Choice(
            title=_('Commune'),
            description=_("Select a commune"),
            required=True,
            vocabulary="gitescontent.communes")

    classification = schema.Choice(
            title=_('Classification'),
            description=_("Select a classification"),
            required=True,
            vocabulary="gitescontent.classification")

    capacityMin = schema.Int(title=_('Minimum Capacity'),
                                 description=_('The minimum capacity of your hebergement'),
                                 required=False)

    roomAmount = schema.Int(title=_('Number of rooms'),
                                description=_('The number of rooms in hebergement'),
                                required=False)

    animals = schema.Bool(title=_('Animals authorized'),
                              description=_('Are animals authorized in the Hebergement'),
                              required=False)

    smokers = schema.Bool(title=_('Smoking allowed'),
                              description=_('Are people allowed to smoke in the Hebergement'),
                              required=False)

    fromDate = schema.Date(title=_('Sejour du'),
                              description=_('Stay from'),
                              required=False)

    toDate = schema.Date(title=_('Sejour au'),
                              description=_('Stay to'),
                              required=False)


class IBasicSearchHebergement(Interface):
    """
    A basic search module to search hebergement
    """

    hebergementType = schema.Choice(
        title=_("Hebergement Type"),
        description=_("Select a type of Hebergement"),
        required=True,
        vocabulary="gitescontent.groupedtypehebergement")

    provinces = schema.Choice(
        title=_('Province'),
        description=_("Select a province"),
        required=True,
        vocabulary="gitescontent.provinces")

    communes = schema.Choice(
        title=_('Commune'),
        description=_("Select a commune"),
        required=True,
        vocabulary="gitescontent.communes")

    classification = schema.Choice(
        title=_('Classification'),
        description=_("Select a classification"),
        required=True,
        vocabulary="gitescontent.classification")

    capacityMin = schema.Int(title=_('Minimum Capacity'),
                             description=_('The minimum capacity of your hebergement'),
                             required=False)

    roomAmount = schema.Int(title=_('Number of rooms'),
                            description=_('The number of rooms in hebergement'),
                            required=False)

    animals = schema.Bool(title=_('Animals authorized'),
                          description=_('Are animals authorized in the Hebergement'),
                          required=False)

    smokers = schema.Bool(title=_('Smoking allowed'),
                          description=_('Are people allowed to smoke in the Hebergement'),
                          required=False)

    fromDate = schema.Date(title=_('Sejour du'),
                              description=_('Stay from'),
                              required=False)

    toDate = schema.Date(title=_('Sejour au'),
                              description=_('Stay to'),
                              required=False)


class IBasicSearchHebergementTooMuch(Interface):
    """
    A basic search module to search hebergement
    """
    seeResults = schema.Bool(title=_('Show results even if more than 50'),
                             description=_('Show results even if there are more than 50'),
                             required=False)

    hebergementType = schema.Choice(
        title=_("Hebergement Type"),
        description=_("Select a type of Hebergement"),
        required=True,
        vocabulary="gitescontent.groupedtypehebergement")

    provinces = schema.Choice(
        title=_('Province'),
        description=_("Select a province"),
        required=True,
        vocabulary="gitescontent.provinces")

    communes = schema.Choice(
        title=_('Commune'),
        description=_("Select a commune"),
        required=True,
        vocabulary="gitescontent.communes")

    classification = schema.Choice(
        title=_('Classification'),
        description=_("Select a classification"),
        required=True,
        vocabulary="gitescontent.classification")

    capacityMin = schema.Int(title=_('Minimum Capacity'),
                             description=_('The minimum capacity of your hebergement'),
                             required=False)

    roomAmount = schema.Int(title=_('Number of rooms'),
                            description=_('The number of rooms in hebergement'),
                            required=False)

    animals = schema.Bool(title=_('Animals authorized'),
                          description=_('Are animals authorized in the Hebergement'),
                          required=False)

    smokers = schema.Bool(title=_('Smoking allowed'),
                          description=_('Are people allowed to smoke in the Hebergement'),
                          required=False)

    fromDate = schema.Date(title=_('Sejour du'),
                              description=_('Stay from'),
                              required=False)

    toDate = schema.Date(title=_('Sejour au'),
                              description=_('Stay to'),
                              required=False)


class ISearchHebergementTooMuch(Interface):
    """
    A search module to search hebergement
    """

    seeResults = schema.Bool(title=_('Show results even if more than 50'),
                             description=_('Show results even if there are more than 50'),
                             required=False)

    hebergementType = schema.Choice(
        title=_("Hebergement Type"),
        description=_("Select a type of Hebergement"),
        required=True,
        vocabulary="gitescontent.typehebergement")

    provinces = schema.Choice(
        title=_('Province'),
        description=_("Select a province"),
        required=True,
        vocabulary="gitescontent.provinces")

    communes = schema.Choice(
        title=_('Commune'),
        description=_("Select a commune"),
        required=True,
        vocabulary="gitescontent.communes")

    classification = schema.Choice(
        title=_('Classification'),
        description=_("Select a classification"),
        required=True,
        vocabulary="gitescontent.classification")

    capacityMin = schema.Int(title=_('Minimum Capacity'),
                             description=_('The minimum capacity of your hebergement'),
                             required=False)

    roomAmount = schema.Int(title=_('Number of rooms'),
                            description=_('The number of rooms in hebergement'),
                            required=False)

    animals = schema.Bool(title=_('Animals authorized'),
                          description=_('Are animals authorized in the Hebergement'),
                          required=False)

    smokers = schema.Bool(title=_('Smoking allowed'),
                          description=_('Are people allowed to smoke in the Hebergement'),
                          required=False)

    fromDate = schema.Date(title=_('Sejour du'),
                              description=_('Stay from'),
                              required=False)

    toDate = schema.Date(title=_('Sejour au'),
                              description=_('Stay to'),
                              required=False)


class ISearchPk(Interface):
    """
    Search module to search hebergement among the site content
    """

    pk = schema.Int(title=_('Heb Pk'),
                        required=True)


class IProprioInfo(Interface):
    """
    mise à jour info proprio
    """

    def getAllPorprio():
        """
        Liste tous les proprios
        """

    def getProprioByLogin(proprioFk):
        """
        Selectionne les infos d'un hébergement d'un proprio selon propk
        """

    def getHebergementByHebPk(hebPk):
        """
        Selectionne les infos d'un hébergement selon hebpk
        """

    def getAllProprioMaj():
        """
        recupère tous les proprio en attente de modification
        """

    def addProprioMaj():
        """
        ajoute les infos mise à jour du proprio par le prorpio dans la table provisoire
        """
