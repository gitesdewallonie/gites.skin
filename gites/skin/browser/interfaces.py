from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


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
