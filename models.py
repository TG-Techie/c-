
from _models import *
from tg_tools import *

import builtin_models

@attributeof(ClassModel)
@classmethod
def from_item(cls, item, mod):
    return cls(item.location, item.name, mod, item._superclass_typeident, item._content_typeidents)

def _model(self):
    if self._superclassident is not None:
        self.superclass = superclass = _find_item_by_ident(self.location, self.module, self._superclassident)
        print(f"{self} subclasses {self.superclass}")
    else:
        self.superclass = superclass = None
        print(f"{self} has no superclass")



    if superclass is not None:
        base = superclass.contents
    else:
        base = {}

    ext = {}
    for name, typeident in self._content_typelist:
        ext[name] = _find_item_by_ident(self.location, self.module, typeident)

    self.contents = {**base, **ext}
    print(self.contents)
    for foo in self.contents.items():
        print(foo)
    return


@attributeof(ModuleModel)
@classmethod
def from_item(cls, src):
    mod_mdl = cls(src.location, src.name, None)

    for item in src:
        if isinstance(item, TraitDefItem):
            pass
            #trt_mdl = TraitModel.from_item(item, mod_mdl)
            #mod_mdl._items[trt_mdl.name] = trt_mdl
        elif isinstance(item, ClassItem):
            cls_mdl = ClassModel.from_item(item, mod_mdl)
            mod_mdl._items[cls_mdl.name] = cls_mdl
        elif isinstance(item, FuncItem):
            pass
            # TODO: add this back in
            #fn_mdl = FuncModel.from_item(item, mod_mdl)
            #mod_mdl._items[fn_mdl.name] = fn_mdl
        else:
            raise CMNSModelTimeError(src.location, f"unsupported/unidentifier item '{item}' in '{mod_mdl}'")

    for mdl in mod_mdl._items.values():
        mdl._model()

    return mod_mdl

print(dir())
