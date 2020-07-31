from sharedbases import *

builtin_module_location = Location('!BuiltinModule')

builtin_module = ModuleItem('Builtins', builtin_module_location)

inttype = ClassItem(builtin_module_location, 'Int', builtin_module, builtin_module)
floattype = ClassItem(builtin_module_location, 'Float', builtin_module, builtin_module)
booltype = ClassItem(builtin_module_location, 'Bool', builtin_module, builtin_module)
strtype = ClassItem(builtin_module_location, 'Str', builtin_module, builtin_module)

nonetype = ClassItem(builtin_module_location, 'NoneType', builtin_module, builtin_module)
sometype = ClassItem(builtin_module_location, 'SomeType', builtin_module, builtin_module)
selftype = ClassItem(builtin_module_location, 'SelfType', builtin_module, builtin_module)

builtin_types = (
    inttype,
    floattype,
    booltype,
    strtype,

    nonetype,
    sometype,
    selftype,
)

for builtin_type in builtin_types:
    builtin_module[builtin_type.name] = builtin_type
