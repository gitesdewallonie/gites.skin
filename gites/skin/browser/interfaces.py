from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IGitesTheme(IDefaultPloneLayer):
    """
    Marker interface that defines a Zope 3 browser layer.
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
