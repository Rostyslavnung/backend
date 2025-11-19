import os
import importlib

__all__ = []

package_dir = os.path.dirname(__file__)

for filename in os.listdir(package_dir):
    if filename.endswith(".py") and filename not in ("__init__.py",):
        module_name = filename[:-3]
        module = importlib.import_module(f".{module_name}", package=__name__)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            # Export classes defined in the module into the package namespace.
            # Previously modules with the same name as their primary class were
            # left as module objects on the package, so `from app.src import
            # BaseEntity` returned the module instead of the class. Always
            # export types so the class name in the package refers to the
            # actual class, not the module.

            if isinstance(attr, type):
                globals()[attr_name] = attr
                __all__.append(attr_name)
