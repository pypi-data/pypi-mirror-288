from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any, Generic, Mapping, TypeVar

from loguru import logger
from slugify import slugify

from statickg.helper import CacheProcess, get_classpath
from statickg.models.prelude import BaseType, ETLOutput, InputFile, RelPath, Repository

A = TypeVar("A")


class BaseService(Generic[A]):
    def __init__(
        self,
        name: str,
        workdir: Path,
        args: Any,
        services: Mapping[str, BaseService],
    ):
        raise NotImplementedError()

    def __call__(self, repo: Repository, args: A | list[A], output: ETLOutput):
        if isinstance(args, list):
            outputs = []
            for arg in args:
                outputs.append(self.forward(repo, arg, output))
            return outputs
        return self.forward(repo, args, output)

    def forward(self, repo: Repository, args: A, output: ETLOutput):
        raise NotImplementedError()


class BaseFileService(BaseService[A]):
    def __init__(
        self,
        name: str,
        workdir: Path,
        args: Any,
        services: Mapping[str, BaseService],
    ):
        self.name = name
        self.workdir = workdir
        self.services = services
        self.cache = CacheProcess(
            workdir / f"services/{self.get_service_name()}/{slugify(name)}.db"
        )
        self.logger = logger.bind(name=get_classpath(self.__class__).rsplit(".", 1)[0])
        self.args = args

    def get_service_name(self):
        name = self.__class__.__name__
        assert name.endswith("Service")
        return name[:-7].lower()

    def list_files(
        self,
        repo: Repository,
        patterns: RelPath | list[RelPath],
        unique_filename: bool,
        optional: bool = False,
        compute_missing_file_key: bool = False,
    ) -> list[InputFile]:
        files = []
        for pattern in patterns if isinstance(patterns, list) else [patterns]:
            if pattern.basetype == BaseType.REPO:
                files.extend(repo.glob(pattern.relpath))
            elif pattern.basetype in [BaseType.DATA_DIR, BaseType.CFG_DIR]:
                files.extend(
                    [
                        InputFile(
                            basetype=pattern.basetype,
                            key=(
                                hashlib.sha256(file.read_bytes()).hexdigest()
                                if compute_missing_file_key
                                else ""
                            ),
                            relpath=str(file.relative_to(pattern.basepath)),
                            path=file,
                        )
                        for file in pattern.basepath.glob(pattern.relpath)
                    ]
                )
            else:
                raise ValueError(f"Unsupported base type: {pattern.basetype}")

        if unique_filename:
            filenames = Counter(file.path.name for file in files)
            if len(filenames) != len(files):
                raise ValueError(
                    "Input files must have unique names. Here are some duplications: "
                    + str([k for k, v in filenames.items() if v > 1][:5])
                )

        if not optional:
            if len(files) == 0:
                raise ValueError(
                    f"Service invocation is not optional but no files matched the pattern: {self.get_readable_patterns(patterns)}"
                )
        return files

    def get_readable_patterns(self, patterns: RelPath | list[RelPath]) -> str:
        if isinstance(patterns, list):
            return ", ".join([p.get_ident() for p in patterns])
        return patterns.get_ident()
