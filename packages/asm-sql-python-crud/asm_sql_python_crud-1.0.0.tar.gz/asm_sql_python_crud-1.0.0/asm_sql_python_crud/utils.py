"""
...
"""

import os
import re
import importlib

from inspect import getmembers, isclass
from importlib import import_module

from typing import List, Optional, Union

from tornado.web import url

from base.routers import (
    BaseRouter
)
from base.models import BaseModel
from base.settings import (
    BASE_DIR,
    API_PREFIX,
    TRAILING_SLASH,
    ROUTERS_FOLDER,
    MODELS_FOLDER
)


def _load_modules_from_spec_path(path: str):
    """..."""

    pattern = r"^[a-zA-Z].*\.py"
    modules = []

    for filename in os.listdir(path):
        if not re.match(pattern, filename):
            continue
        root, _ = os.path.splitext(filename)
        package = os.path.relpath(path).replace(os.sep, ".")
        module = importlib.import_module(package + "." + root)
        modules.append(module)
      
    return modules


def get_routes(
    path: str = f"{BASE_DIR}/{ROUTERS_FOLDER}",
    api_prefix: str = API_PREFIX,
    trailing_slash: bool = TRAILING_SLASH,
) -> List[url]:
    """..."""

    routes = []
    
    for module in _load_modules_from_spec_path(path):
        routers = [
            router for _, router in getmembers(module)
            if isinstance(router, BaseRouter)
        ]
        for router in routers:
            router.api_prefix = api_prefix
            router.trailing_slash = trailing_slash
            routes += router.rules

    return routes


def get_models(
    path: str = f"{BASE_DIR}/{MODELS_FOLDER}",
):
    """..."""

    for module in _load_modules_from_spec_path(path):

        for name, obj in getmembers(module, isclass):
            if issubclass(obj, BaseModel) and obj.__name__ != "BaseModel":
                map(__import__, [f"{module.__name__}.{name}"])