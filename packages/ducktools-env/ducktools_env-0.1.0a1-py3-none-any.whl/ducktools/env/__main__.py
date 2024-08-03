# ducktools.env
# MIT License
# 
# Copyright (c) 2024 David C Ellis
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys

import argparse
from ducktools.lazyimporter import LazyImporter, FromImport, MultiFromImport

_laz = LazyImporter(
    [
        FromImport("ducktools.env", "__version__"),
        FromImport("ducktools.env.run", "run_script"),
        FromImport("ducktools.env.scripts.clear_cache", "clear_cache"),
        FromImport("ducktools.env.bundle", "create_bundle"),
        MultiFromImport(
            "ducktools.env.scripts.create_zipapp",
            ["build_env_folder", "build_zipapp"]
        )
    ]
)


def main():
    parser = argparse.ArgumentParser(
        prog="ducktools-env",
        description="Script runner and bundler for scripts with inline dependencies",
    )

    parser.add_argument("-V", "--version", action="version", version=_laz.__version__)

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run",
        help="Launch the provided python script with inline dependencies",
        prefix_chars="+/",
    )

    bundle_parser = subparsers.add_parser(
        "bundle",
        help="Bundle the provided python script with inline dependencies into a python zipapp",
    )

    clear_cache_parser = subparsers.add_parser(
        "clear_cache",
        help="Completely clear the ducktools/env cache folder"
    )

    create_zipapp_parser = subparsers.add_parser(
        "rebuild_env",
        help="Recreate the ducktools-env library cache from the installed package"
    )

    create_zipapp_parser.add_argument(
        "--zipapp",
        action="store_true",
        help="Also create the portable ducktools.pyz zipapp",
    )

    run_parser.add_argument("script_filename", help="Path to the script to run")
    bundle_parser.add_argument("script_filename", help="Path to the script to bundle into a zipapp")

    args, extras = parser.parse_known_args()

    if args.command == "run":
        _laz.run_script(args.script_filename, extras)
    elif args.command == "bundle":
        if extras:
            arg_text = ' '.join(extras)
            sys.stderr.write(f"Unrecognised arguments: {arg_text}")
            return

        _laz.create_bundle(args.script_filename)
    elif args.command == "clear_cache":
        if extras:
            arg_text = ' '.join(extras)
            sys.stderr.write(f"Unrecognised arguments: {arg_text}")
            return

        _laz.clear_cache()
    elif args.command == "rebuild_env":
        if extras:
            arg_text = ' '.join(extras)
            sys.stderr.write(f"Unrecognised arguments: {arg_text}")
            return
        _laz.build_env_folder()
        if args.zipapp:
            _laz.build_zipapp()
    else:
        # Should be unreachable
        raise ValueError("Invalid command")


if __name__ == "__main__":
    main()
