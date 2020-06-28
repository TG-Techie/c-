#will be exported to a seperate repo later
NoneType = type(None)

def attributeof(cls):
    assert isinstance(cls, type), f"argument 'cls' must be a class, got type '{type(cls).__name__}'"

    def _add_attr_to__(attr):
        if isinstance(attr, (classmethod, staticmethod)):
            name  = attr.__func__.__name__
        else:
            assert hasattr(attr, '__name__'), f"must be a named attribute to add to {cls}, got an attribute of type '{type(attr).__name__}'"

            name = meth.__name__

        if hasattr(cls, name):
            raise AttributeError(f"{cls} alreay has attribute '{name}', cannot be added to {cls}")
        else:
            setattr(cls, name, attr)
        attr

    _add_attr_to__.__name__ = _add_attr_to__.__name__.replace('__', f'_{cls.__name__}')
    return _add_attr_to__
