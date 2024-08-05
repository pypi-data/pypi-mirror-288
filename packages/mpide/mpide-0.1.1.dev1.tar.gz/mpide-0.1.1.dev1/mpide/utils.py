#!/usr/bin/env python3
#                  _     _
#  _ __ ___  _ __ (_) __| | ___
# | '_ ` _ \| '_ \| |/ _` |/ _ \
# | | | | | | |_) | | (_| |  __/
# |_| |_| |_| .__/|_|\__,_|\___|
#           |_|
#
# mpide - MicroPython (Integrated) Development Environment
# Copyright (C) 2024 - Frans Fürst
#
# mpide is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# mpide is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for machine learning. If you're using any content of this
# repository to train any sort of machine learned model (e.g. LLMs), you agree to make the whole
# model trained with this repository and all data needed to train (i.e. reproduce) the model
# publicly and freely available (i.e. free of charge and with no obligation to register to any
# service) and make sure to inform the author (me, frans.fuerst@protonmail.com) via email how to
# get and use that model and any sources needed to train it.

"""Stuff we need only on the development host"""

import asyncio
import logging
import shlex
from asyncio import StreamReader
from asyncio.subprocess import PIPE, create_subprocess_exec
from contextlib import suppress
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import TypeAlias

from apparat.misc import collect_chunks

from mpide.target.mpide.misc import file_checksum

StrSeq: TypeAlias = list[str] | tuple[str]


def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("trickkiste.mpide.utils")


def load_module(filepath: str | Path) -> ModuleType:
    """(Re)loads a python module specified by @filepath"""
    log().debug("load module '%s' from '%s'", Path(filepath).stem, filepath)
    spec = spec_from_file_location(Path(filepath).stem, filepath)
    if not (spec and spec.loader):
        raise RuntimeError("Could not load")
    module = module_from_spec(spec)
    assert module
    assert isinstance(spec.loader, SourceFileLoader)
    loader: SourceFileLoader = spec.loader
    # here the actual track definition takes place
    loader.exec_module(module)
    return module


async def mpyfy(source_path: Path, mpy_cross: Path, cache_path: Path) -> Path:
    """Takes a filename and in case it's being identified as .mpy a precompiled
    mpy file gets generated from the correspondent py file and it's path is
    returned. Just return the original filename without any action otherwise
    """
    path = Path(source_path)
    if path.suffix != ".py":
        return path
    cs_file = cache_path / f"{path.stem}-{file_checksum(path.as_posix())[:10]}.mpy"
    if not cs_file.exists():
        cs_file.parent.mkdir(parents=True, exist_ok=True)
        stdout, stderr, return_code = await async_process_output(
            f"{mpy_cross} -v {path.as_posix()} -o {cs_file}"
        )
        if return_code != 0:
            raise RuntimeError(f"Could not compile {path}")
        for line in stdout:
            log().debug("mpy-cross: %s", line)
        for line in stderr:
            log().warning("mpy-cross: %s", line)
    log().debug("precompiled: %s", cs_file.relative_to(cache_path))
    return cs_file


async def collect_list(stream: StreamReader, *, err: bool) -> StrSeq:
    """Creates a sanatized list of strings from something iterable and logs on the go"""

    def log_line(line: str) -> str:
        """Logging pass-through"""
        log().debug("%s: %s", "err" if err else "std", line)
        return line

    return [
        log_line(line.decode().rstrip())
        async for raw_lines in collect_chunks(aiter(stream), min_interval=3, bucket_size=5)
        for line in raw_lines
    ]


async def async_process_output(command: str) -> tuple[StrSeq, StrSeq, int]:
    """Local implementation of execute()"""
    log().debug("run command '%s' locally..", command)
    process = await create_subprocess_exec(*shlex.split(command), stdout=PIPE, stderr=PIPE)
    assert process.stdout and process.stderr
    try:
        stdout, stderr, return_code = await asyncio.gather(
            collect_list(process.stdout, err=False),
            collect_list(process.stderr, err=True),
            process.wait(),
        )
        return stdout, stderr, return_code
    finally:
        with suppress(ProcessLookupError):
            process.terminate()
