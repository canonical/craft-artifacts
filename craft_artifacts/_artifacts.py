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

"""Artifacts support."""

import abc
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast, final

from pydantic import BaseModel, PrivateAttr


@dataclass
class BaseArtifactInputDirs:
    """Base artifact input directories.

    Artifacts classes should expand this to declare their own required input dirs.
    """

    default_prime_dir: Path


@dataclass
class BaseArtifact(metaclass=abc.ABCMeta):
    """Base artifact definition."""

    input_dirs: BaseArtifactInputDirs
    name: str
    outputs: list[Path] = field(init=False, default_factory=list[Path])
    work_dir: Path = Path.cwd()
    keep: bool = False

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return self.name == cast(BaseArtifact, other).name

        return False

    @abc.abstractmethod
    def _pack(self) -> None:
        """Pack one or more artifacts.

        Must store the list of packed outputs in self.outputs.
        """
        return

    @final
    def pack(self) -> list[Path]:
        """Pack one or more artifacts.

        :returns: A list of paths to created artifacts.
        """
        self._pack()

        return self.outputs


class Artifacts(BaseModel):
    """Collection of artifacts to pack."""

    _artifacts: set[BaseArtifact] = PrivateAttr(default_factory=set[BaseArtifact])
    dest: Path

    def add(self, artifacts: list[BaseArtifact]) -> None:
        """Add artifacts to the collection.

        Explicitly adding an artifact indicates it should
        be kept in the final outputs.

        For each artifact, it must:
        - control the name is unique
        - skip if already in the set
        - set the "keep" property to True

        :raise ValueError: If the artifact is already in the set
        """
        for a in artifacts:
            a.keep = True
            if a in self._artifacts:
                raise ValueError(f"artifact {a.name} already in the set")
            self._artifacts.add(a)

    def pack(self) -> list[Path]:
        """Pack every artifacts.

        :returns: A list of paths to created artifacts.
        """
        outputs: list[Path] = []

        for artifact in self._artifacts:
            artifact_outputs = artifact.pack()
            if artifact.keep:
                _move_outputs(
                    artifact=artifact,
                    dest_root=self.dest,
                    artifact_outputs=artifact_outputs,
                    outputs=outputs,
                )

        return outputs


def _move_outputs(
    artifact: BaseArtifact,
    dest_root: Path,
    artifact_outputs: list[Path],
    outputs: list[Path],
) -> None:
    """Move an artifact outputs to the dest directory."""
    for output in artifact_outputs:
        dest_dir = dest_root / artifact.name
        dest_dir.mkdir()
        dest = dest_dir / output.name
        shutil.copy2(output, dest)
        outputs.append(dest)
