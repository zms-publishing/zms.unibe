import importlib
import pkgutil

from fastapi import FastAPI

import zms.unibe.fastapi as endpoints


# https://stackoverflow.com/questions/3365740/how-to-import-all-submodules#65021760
def import_submodules_recursively(module):
    for loader, module_name, is_pkg in pkgutil.walk_packages(
            module.__path__, module.__name__ + '.'):
        importlib.import_module(module_name)

# https://fastapi.tiangolo.com/#run-it
# https://fastapi.tiangolo.com/fastapi-cli/
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/#enable-proxy-forwarded-headers
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/#mounting-a-sub-application
# Please note:
# - The proxy_headers and the forwarded_allow_ips must be set for all mounted sub-applications as well.

api = FastAPI(
    openapi_url=None,
    proxy_headers=True,
    forwarded_allow_ips=["*"],
)

import_submodules_recursively(endpoints)
