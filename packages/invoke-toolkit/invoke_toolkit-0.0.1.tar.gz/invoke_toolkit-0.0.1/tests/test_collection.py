import importlib
import pkgutil
import sys
import types
from unittest import mock

from invoke_toolkit.collections import Collection


def my_function(package_path):
    modules = []
    for _, module_name, _ in pkgutil.walk_packages([package_path]):
        modules.append(module_name)
    return modules


def test_collection_load_submodules(monkeypatch):
    ns = Collection()

    def mock_walk_packages(path):
        # Simulate modules
        module1 = types.ModuleType("not_to_import")
        module2 = types.ModuleType("to_import.tasks.mod1")
        module3 = types.ModuleType("to_import.tasks.mod2")
        return [
            ("module1", "", module1),
            ("to_import.tasks.mod1", "", module2),
            ("to_import.tasks.mod2", "", module3),
        ]

    def mock_import_module(name):
        monkeypatch.setitem(name, types.ModuleType(name=name))

    monkeypatch.setattr(importlib, "import_module", mock.MagicMock())
    monkeypatch.setattr(pkgutil, "walk_packages", mock_walk_packages)
    module_to_import = types.ModuleType(name="to_import")
    monkeypatch.setitem(sys.modules, "to_import.tasks", module_to_import)
    result = ns.add_collections_from_namespace("to_import.tasks")
    breakpoint()
