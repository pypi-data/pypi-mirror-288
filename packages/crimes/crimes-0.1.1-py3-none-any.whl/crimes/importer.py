from __future__ import annotations

import sys
from ctypes import CDLL
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Sequence

from crimes.compiler import compile_and_link


class CDLLModule(ModuleType):
    def __init__(self, name: str, src_path: str):
        # Initialize this first to prevent fruitless recursive getattr() calls
        self.__cdll__: CDLL | None = None
        super().__init__(name)
        self.__file__: str = src_path

    def __getattr__(self, name):
        if self.__cdll__ is not None:
            return getattr(self.__cdll__, name)
        raise AttributeError(name)


class CImporter(MetaPathFinder, Loader):
    def find_spec(
        self, fullname: str, path: Sequence | None, target: ModuleType | None = None
    ) -> ModuleSpec | None:
        if p := find_on_sys_path(fullname):
            return ModuleSpec(
                name=fullname, loader=self, loader_state={"path": str(p.resolve())}
            )

        # Could not find the C source code file
        return None

    def create_module(self, spec: ModuleSpec) -> CDLLModule:
        # Pass both the name and the source code path so that exec_module knows where to find the source code.
        return CDLLModule(spec.name, spec.loader_state["path"])

    def exec_module(self, module: ModuleType) -> None:
        assert isinstance(module, CDLLModule)
        cdll = compile_and_link(module.__file__)
        module.__cdll__ = cdll


def find_on_sys_path(fullname: str) -> Path | None:
    """
    Returns a path to a C file on the path that we can try to compile.
    """
    # Yup, we just try importing it for each directory in the path...
    for directory in sys.path:
        candidate = Path(directory) / f"{fullname}.c"
        if candidate.exists():
            return candidate
    return None


def install_importer() -> CImporter:
    """
    Enable the import of C source code.

    This works by inserting a Finder before all pre-existing finders in sys.meta_path.
    """
    importer = CImporter()
    sys.meta_path.insert(0, importer)
    return importer


def uninstall_importer(importer: CImporter):
    """
    Removes the importer returned by :py:func:install_importer().

    Usage:
    >>> from crimes.importer import install_importer, uninstall_importer
    >>> imp = install_importer()
    >>> uninstall_importer(imp)
    """

    i = sys.meta_path.index(importer)
    del sys.meta_path[i]
