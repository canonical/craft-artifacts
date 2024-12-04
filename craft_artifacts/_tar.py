# This file is part of craft-artifacts.
#
# Copyright 2024 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tar artifact generation support."""

import enum
import tarfile
from dataclasses import dataclass

from craft_artifacts import BaseArtifact


class TarCompression(enum.Enum):
    """Enum values that represent valid tar compressions."""

    UNCOMPRESSED = ""
    BZIP2 = "bz2"
    GZIP = "gz"
    XZ = "xz"


@dataclass
class TarArtifact(BaseArtifact):
    """Generate a tar archive."""

    compression: TarCompression = TarCompression.UNCOMPRESSED
    name: str = "tarball"
    suffix: str = ".tar"

    def _pack(self) -> None:
        """Tar the given directory."""
        compression_suffix = ""
        if self.compression.value:
            compression_suffix = f".{self.compression.value}"
        filename = f"{self.name}{self.suffix}{compression_suffix}"
        dest = self.work_dir / filename
        with tarfile.open(dest, mode="w:" + self.compression.value) as tar:
            tar.add(self.input_dirs.default_prime_dir, arcname=".", recursive=True)

        self.outputs = [dest]
