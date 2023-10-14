import inspect
import os

from functools import lru_cache


@lru_cache
def list_templates():
    templates = []
    path = os.path.dirname(os.path.abspath(__file__))
    for subfolder in [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]:
        subpath = os.path.join(path, subfolder)
        for py in [f[:-3] for f in os.listdir(subpath) if f.endswith('.py') and f != '__init__.py']:
            mod = __import__(
                '.'.join([__name__, subfolder, py]), fromlist=[py])
            classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type) and
                       hasattr(getattr(mod, x), 'template')]
            for cls in classes:
                if not inspect.isabstract(cls):
                    templates.append(cls)
                # print(cls, isinstance(cls(), Template))
                # print(cls, inspect.isabstract(cls))
                # setattr(sys.modules[__name__], cls.__name__, cls)
    return templates
