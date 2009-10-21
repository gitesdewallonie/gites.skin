import gites.skin.monkey
from zope.i18nmessageid import MessageFactory
GitesMessage = MessageFactory("gites")
GitesLocalesMessage = MessageFactory("giteslocales")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
