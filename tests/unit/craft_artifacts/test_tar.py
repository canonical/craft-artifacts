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

import tarfile

import pytest
from craft_artifacts import (
    BaseArtifactInputDirs,
    TarArtifact,
    TarCompression,
)


def test_tarball_default_artifact(tmp_path):
    work_dir = tmp_path / "work"
    prime_dir = tmp_path / "work/prime"
    prime_dir.mkdir(parents=True)

    # Create some directories and files
    for d in ["d1/d11", "d2/d21", "d3/d31"]:
        (prime_dir / d).mkdir(parents=True)
    for file in ["a", "d1/b", "d3/d31/c"]:
        full_path = tmp_path / "work/prime" / file
        full_path.touch()

    input_dirs = BaseArtifactInputDirs(default_prime_dir=prime_dir)
    artifact = TarArtifact(
        input_dirs=input_dirs,
        work_dir=work_dir,
        compression=TarCompression.UNCOMPRESSED,
    )

    assert artifact.name == "tarball"
    assert artifact.suffix == ".tar"

    artifact.pack()

    default_tarball = "tarball.tar"
    assert artifact.outputs == [work_dir / default_tarball]

    with tarfile.open(work_dir / default_tarball, "r") as tar:
        assert tar.getnames() == [
            ".",
            "./a",
            "./d1",
            "./d1/b",
            "./d1/d11",
            "./d2",
            "./d2/d21",
            "./d3",
            "./d3/d31",
            "./d3/d31/c",
        ]


@pytest.mark.parametrize(
    ("compression", "output"),
    [
        (TarCompression.UNCOMPRESSED, "tarball.tar"),
        (TarCompression.BZIP2, "tarball.tar.bz2"),
        (TarCompression.GZIP, "tarball.tar.gz"),
        (TarCompression.XZ, "tarball.tar.xz"),
    ],
)
def test_tarball_artifact_compression(
    tmp_path, compression: TarCompression, output: str
):
    work_dir = tmp_path / "work"
    prime_dir = tmp_path / "work/prime"
    prime_dir.mkdir(parents=True)

    input_dirs = BaseArtifactInputDirs(default_prime_dir=prime_dir)
    artifact = TarArtifact(
        input_dirs=input_dirs,
        work_dir=work_dir,
        compression=compression,
    )
    artifact.pack()

    assert artifact.outputs == [work_dir / output]


def test_tarball_overwriting_archive(tmp_path):
    work_dir = tmp_path / "work"
    prime_dir = tmp_path / "work/prime"
    prime_dir.mkdir(parents=True)

    input_dirs = BaseArtifactInputDirs(default_prime_dir=prime_dir)
    artifact = TarArtifact(input_dirs=input_dirs, work_dir=work_dir, name="test-name")

    (work_dir / "test-name.tar").touch()

    artifact.pack()
