from Acquisition import Explicit
from zope.schema._field import AbstractCollection
from zope.schema.interfaces import IList
from zope.interface import implements

class List(Explicit, AbstractCollection):
    """A field representing a List."""
    implements(IList)
    _type = list

