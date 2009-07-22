from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface
from zope import schema
from schema import List
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

    def getHebergementByPk(heb_pk):
        """
        Get the url of the hebergement by Pk
        """

    def getHebergementTypes():
        """
        retourne les types d hebergements
        """

    def getGroupedHebergementTypes(self):
        """
        retourne les deux groupes de types d hebergements
        """


class IHebergementView(Interface):
    """
    View for the full description of an hebergement
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

    def getHebergementSeminaireVert(self):
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

    def sendMailToProprio():
        """
        Envoi un mail au proprio via le site
        """


class ISearchHebergement(Interface):
    """
    A search module to search hebergement
    """

    hebergementType = List(title=_("Hebergement Type"),
                           description=_("Select a type of Hebergement"),
                           unique=True,
                           required=False,
                           value_type=schema.Choice(
                           vocabulary="gitescontent.typehebergement"))

    provinces = List(
            title=_('Province'),
            description=_("Select a province"),
            unique = True,
            required=False,
            value_type=schema.Choice(
            vocabulary="gitescontent.provinces"))

    classification = List(
            title=_('Classification'),
            description=_("Select a classification"),
            unique = True,
            required=False,
            value_type=schema.Choice(
            vocabulary="gitescontent.classification"))

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


class IBasicSearchHebergement(Interface):
    """
    A basic search module to search hebergement
    """

    hebergementType = List(
        title=_("Hebergement Type"),
        description=_("Select a type of Hebergement"),
        unique=True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.groupedtypehebergement"))

    provinces = List(
        title=_('Province'),
        description=_("Select a province"),
        unique = True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.provinces"))

    classification = List(
        title=_('Classification'),
        description=_("Select a classification"),
        unique = True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.classification"))

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


class IBasicSearchHebergementTooMuch(Interface):
    """
    A basic search module to search hebergement
    """
    seeResults = schema.Bool(title=_('Show results even if more than 50'),
                             description=_('Show results even if there are more than 50'),
                             required=False)

    hebergementType = List(
        title=_("Hebergement Type"),
        description=_("Select a type of Hebergement"),
        unique=True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.groupedtypehebergement"))

    provinces = List(
        title=_('Province'),
        description=_("Select a province"),
        unique = True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.provinces"))

    classification = List(
        title=_('Classification'),
        description=_("Select a classification"),
        unique = True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.classification"))

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


class ISearchHebergementTooMuch(Interface):
    """
    A search module to search hebergement
    """

    seeResults = schema.Bool(title=_('Show results even if more than 50'),
                             description=_('Show results even if there are more than 50'),
                             required=False)

    hebergementType = List(
        title=_("Hebergement Type"),
        description=_("Select a type of Hebergement"),
        unique = True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.typehebergement"))

    provinces = List(
        title=_('Province'),
        description=_("Select a province"),
        unique = True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.provinces"))

    classification = List(
        title=_('Classification'),
        description=_("Select a classification"),
        unique = True,
        required=False,
        value_type=schema.Choice(
            vocabulary="gitescontent.classification"))

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


class ISearchPk(Interface):
    """
    Search module to search hebergement among the site content
    """

    pk = schema.Int(title=_('Heb Pk'),
                        required=True)