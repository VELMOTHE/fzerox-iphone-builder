#!/usr/bin/env python3
"""Prepare the pinned iPhone build without changing game code."""
import argparse
from pathlib import Path
import shlex

parser = argparse.ArgumentParser()
parser.add_argument("root", type=Path)
parser.add_argument("--cache", type=Path)
parser.add_argument("--patch-dependencies", action="store_true")
args = parser.parse_args()

if args.patch_dependencies:
    path = args.root / "ref/G-Diffuser/libultraship/cmake/dependencies/ios.cmake"
    source = path.read_text()
    original = "find_package(libzip QUIET)"
    replacement = "set(libzip_FOUND FALSE) # Always build the iOS library from its pinned source"
    if original in source:
        assert source.count(original) == 1
        source = source.replace(original, replacement)
        path.write_text(source)
    else:
        assert replacement in source, "Unexpected libzip dependency configuration"
else:
    assert args.cache and args.cache.is_file(), "SDK probe cache missing"
    path = args.root / "scripts/build-padmint-ios.sh"
    source = path.read_text()
    setup = "bash scripts/setup-sources.sh" + chr(10)
    assert source.count(setup) == 1
    command = "python3 " + shlex.quote(str(Path(__file__).resolve())) + " " + shlex.quote(str(args.root.resolve())) + " --patch-dependencies" + chr(10)
    source = source.replace(setup, setup + command)
    configure = "cmake -S ref/G-Diffuser -B"
    assert source.count(configure) == 1
    source = source.replace(configure, "cmake -C " + shlex.quote(str(args.cache.resolve())) + " -S ref/G-Diffuser -B")
    assert "CMAKE_DISABLE_FIND_PACKAGE_libzip" not in source
    path.write_text(source)
