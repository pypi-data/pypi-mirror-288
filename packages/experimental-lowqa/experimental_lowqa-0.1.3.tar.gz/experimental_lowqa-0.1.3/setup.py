# =====================================
# generator=datazen
# version=3.1.4
# hash=a53787c3d6b80f7872e346b656147959
# =====================================

"""
experimental-lowqa - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from experimental_lowqa_bootstrap.setup import setup  # type: ignore

# internal
from experimental_lowqa import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.10",
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
