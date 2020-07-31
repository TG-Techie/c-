from strictly import *
from dataclasses import dataclass

from lexer_parser import Location

'''
class BuiltinModuleItem(Item):

    @strictly
    def __init__(self,
        name : str,
        items : Union[dict, None] = None,
        outer = None,
        root = None
        ):
        if items is None:
            items = {}

        self.location = Location(name)
        self.name = name
        self.outer = outer
        self._root = root
        self.modeled = True

        self.items = self._items = items

class BuiltinClassItem():
    pass
'''
