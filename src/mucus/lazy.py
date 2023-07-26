import importlib.util


def import_module(name, package=None):
    spec = importlib.util.find_spec(name, package)
    if spec is None:
        raise ModuleNotFoundError(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module
