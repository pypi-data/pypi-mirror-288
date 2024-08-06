import argparse
import sys
import os
import traceback

import PIL.Image

from . import main_

def prepareFolder(file: str) -> None: 
    os.makedirs(os.path.dirname(file), exist_ok=True)

def do(from_: str, to: str, type: main_.ImageType) -> None:
    from_ = os.path.realpath(from_)
    to = os.path.realpath(to)
    try:
        img = PIL.Image.open(from_, formats=["PNG"])
        after: PIL.Image.Image = main_.resize_to(img, type)
        prepareFolder(to)
        after.save(to)
        print(f"{from_} => {to} 成功")
    except Exception as e:
        print(f"{from_} => {to} 失败，原因：", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)


def run(from_: str, to: str, directory: bool, all: bool, big: bool, small: bool) -> None:
    if all:
        return run(from_, to, directory, False, True, True)
    if not big and not small:
        return run(from_, to, directory, True, False, False)
    if directory:
        for filename in os.listdir(from_):
            if not filename.endswith(".png") or filename.endswith(".apng"):
                continue
            if big:
                do(os.path.join(from_, filename), os.path.join(to, ".".join(filename.split(
                    ".")[:-1]) + "_small.png"), main_.ImageType.Small)
            if small:
                do(os.path.join(from_, filename), os.path.join(to, ".".join(filename.split(
                    ".")[:-1]) + "_big.png"), main_.ImageType.Big)
        return
    if big and small:
        do(from_, ".".join(to.split(".")[:-1]) +
           "_small.png", main_.ImageType.Small)
        do(from_, ".".join(to.split(".")[:-1]) +
           "_big.png", main_.ImageType.Big)
        return
    if big:
        return do(from_, to, main_.ImageType.Big)
    do(from_, to, main_.ImageType.Small)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "from_", help="the specific image or directory with images", type=str)
    parser.add_argument(
        "to", help="where to store your image(s).", type=str)
    parser.add_argument(
        "-d", "--directory", help="whether to process a directory instead of a single file", action="store_true"
    )
    type = parser.add_mutually_exclusive_group(required=False)
    type.add_argument(
        "-a", "--all", help="generate both small and big images.", action="store_true")
    type.add_argument(
        "-b", "--big", help="generate big image(s)", action="store_true")
    type.add_argument(
        "-s", "--small", help="generate small image(s)", action="store_true")
    parser.add_argument_group(type)
    args = parser.parse_args()
    run(args.from_, args.to, args.directory, args.all, args.big, args.small)