# Copyright 2024 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/kerncraft


from pathlib import Path

import pytest
from craft_artifacts import (
    Artifacts,
    BaseArtifact,
    BaseArtifactInputDirs,
)


class NoOpArtifact(BaseArtifact):
    def _pack(self) -> None:
        return


def test_base_artifact_input_dirs_init():
    expected = "missing 1 required positional argument: 'default_prime_dir'"
    with pytest.raises(TypeError, match=expected):
        BaseArtifactInputDirs()  # pyright: ignore[reportCallIssue]


def test_child_artifact_init():
    class ExampleArtifact(BaseArtifact):
        def _pack(self) -> None:
            return

    expected = "missing 2 required positional arguments: 'input_dirs' and 'name'"

    with pytest.raises(TypeError, match=expected):
        ExampleArtifact()  # pyright: ignore[reportAbstractUsage, reportCallIssue]


def test_base_artifact_faulty_artifact():
    class FaultyArtifact(BaseArtifact):
        """A faulty artifact not implementing required methods."""

    expected = (
        r"^Can't instantiate abstract class FaultyArtifact with(out an "
        r"implementation for)? abstract method '?_pack'?$"
    )
    input_dirs = BaseArtifactInputDirs(default_prime_dir=Path("./prime"))

    with pytest.raises(TypeError, match=expected):
        FaultyArtifact(
            name="a",
            input_dirs=input_dirs,
        )  # pyright: ignore[reportAbstractUsage]


def test_artifacts_add():
    input_dirs = BaseArtifactInputDirs(default_prime_dir=Path("./prime"))

    artifact_a = NoOpArtifact(
        name="a",
        input_dirs=input_dirs,
        work_dir=Path("./a"),
    )
    artifact_b = NoOpArtifact(
        name="b",
        input_dirs=input_dirs,
        keep=True,
    )
    artifact_c = NoOpArtifact(
        name="c",
        input_dirs=input_dirs,
    )
    artifact_d = NoOpArtifact(
        name="d",
        input_dirs=input_dirs,
        keep=True,
    )

    artifacts = Artifacts(
        dest=Path("./output"),
    )
    artifacts.add([artifact_a, artifact_b])

    assert artifacts._artifacts == {artifact_a, artifact_b}

    # Try to add the same artifacts twice
    with pytest.raises(ValueError, match="artifact a already in the set"):
        artifacts.add([artifact_a, artifact_b])

    artifacts.add([artifact_c, artifact_d])
    assert artifacts._artifacts == {
        artifact_a,
        artifact_b,
        artifact_c,
        artifact_d,
    }

    for artifact in artifacts._artifacts:
        assert artifact.keep

    # Try to add another artifact with the same name as another
    # already in the collection
    artifact_a_duplicate = NoOpArtifact(
        name="a",
        input_dirs=input_dirs,
        work_dir=Path("./a_duplicate"),
    )
    with pytest.raises(ValueError, match="artifact a already in the set"):
        artifacts.add([artifact_a_duplicate])

    assert artifacts._artifacts == {
        artifact_a,
        artifact_b,
        artifact_c,
        artifact_d,
    }


def test_artifacts_no_artifact_init():
    input_dirs = BaseArtifactInputDirs(default_prime_dir=Path("./prime"))

    artifact_a = NoOpArtifact(
        name="a",
        input_dirs=input_dirs,
        work_dir=Path("./a"),
    )
    artifact_b = NoOpArtifact(
        name="b",
        input_dirs=input_dirs,
        keep=True,
    )
    # Setting artifacts here will be ignored
    artifacts = Artifacts(dest=Path("./output"), _artifacts={artifact_a, artifact_b})  # pyright: ignore[reportCallIssue]
    assert artifacts._artifacts == set()


def test_artifacts_pack(tmp_path):
    class ExampleArtifact(BaseArtifact):
        def _pack(self) -> None:
            self.work_dir.mkdir(parents=True)
            output = self.work_dir / f"{self.name}.output"
            output.touch()
            self.outputs = [output]

    work_dir = tmp_path / "work"
    work_dir.mkdir()
    dest_dir = work_dir / "output"
    dest_dir.mkdir()
    prime_dir = work_dir / "prime"
    prime_dir.mkdir()

    input_dirs = BaseArtifactInputDirs(default_prime_dir=prime_dir)

    artifact_a = ExampleArtifact(
        name="a",
        input_dirs=input_dirs,
        work_dir=work_dir / "a",
    )
    artifact_b = ExampleArtifact(
        name="b",
        input_dirs=input_dirs,
        work_dir=work_dir / "b",
    )
    artifacts = Artifacts(dest=dest_dir)
    artifacts.add([artifact_a, artifact_b])
    outputs = artifacts.pack()

    outputs.sort()

    assert outputs == [
        dest_dir / "a" / "a.output",
        dest_dir / "b" / "b.output",
    ]
