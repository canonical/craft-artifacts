# This file is part of craft-artifacts.
#
# Copyright 2024 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Artifacts packing."""

from ._artifacts import (
    Artifacts,
    BaseArtifact,
    BaseArtifactInputDirs,
)
from ._tar import TarArtifact, TarCompression

try:
    from ._version import __version__
except ImportError:  # pragma: no cover
    from importlib.metadata import version, PackageNotFoundError

    try:
        __version__ = version("craft-artifacts")
    except PackageNotFoundError:
        __version__ = "dev"

__all__ = [
    "__version__",
    "Artifacts",
    "BaseArtifact",
    "BaseArtifactInputDirs",
    "TarArtifact",
    "TarCompression",
]
