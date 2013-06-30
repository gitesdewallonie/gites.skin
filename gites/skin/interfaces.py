# -*- coding: utf-8 -*-
"""
gites.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""
from zope.interface import Interface


class IDerniereMinuteRootFolder(Interface):
    """
    Marker interface for DerniereMinuteRootFolder root folder
    """


class IBoutiqueRootFolder(Interface):
    """
    Marker interface for BoutiqueRootFolder root folder
    """


class ISejourFuteRootFolder(Interface):
    """
    Marker interface for Sejour Fute root folder
    """


class IIdeeSejourRootFolder(Interface):
    """
    Marker interface for Idee Sejour root folder
    """
