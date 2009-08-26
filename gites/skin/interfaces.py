# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from zope.interface import Interface


class ISejourFuteRootFolder(Interface):
    """
    Marker interface for Sejour Fute root folder
    """


class IIdeeSejourRootFolder(Interface):
    """
    Marker interface for Idee Sejour root folder
    """
