# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from zope.interface import Interface


class IDerniereMinuteRootFolder(Interface):
    """
    Marker interface for DerniereMinuteRootFolder root folder
    """


class ISejourFuteRootFolder(Interface):
    """
    Marker interface for Sejour Fute root folder
    """


class IIdeeSejourRootFolder(Interface):
    """
    Marker interface for Idee Sejour root folder
    """

class IMajInfoMenuPortlet(Interface):
    """
    Marker interface for Menu mise à jour des infos proprio et heb
    """