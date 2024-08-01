
from typing import TYPE_CHECKING
from lazy_imports import LazyImporter
import sys

_import_structure = {
    "src": [
        "Basedir",
        "Join",
        "Exists",
        "NotExists",
        "Uniquify",
        "IsDir",
        "Basename",
        "Suffix",
    ],
}

if TYPE_CHECKING:
    from .src import (
        Basedir,
        Join,
        Exists,
        NotExists,
        Uniquify,
        IsDir,
        Basename,
        Suffix,
    )
    from . import Path
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={},
    )


