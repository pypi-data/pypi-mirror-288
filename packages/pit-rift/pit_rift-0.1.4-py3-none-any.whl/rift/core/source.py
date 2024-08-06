#!/usr/bin/env python

import os
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger("rift")


def clone(url, branch, dst) -> None:
    """
    Clone a git repo with designed branch to dst
    :param url: SSH url or local path from where to clone a repo
    :param branch: Git branch name
    :param dst: Where to clone the repo
    """
    if os.path.exists(dst):
        logger.warning(f"{dst} already exists")
        return

    if is_local_repo(url):
        link_local_repo(src=url, dst=dst)
    elif is_github_url(url):
        download_from_github(url, branch, dst)
    else:
        raise ValueError(f"Invalid url: {url}")


def is_local_repo(path: str) -> bool:
    """Return True if path is a clone of a git repository"""
    return os.path.exists(os.path.join(path, ".git"))


def is_github_url(url: str) -> bool:
    """Return True if url is an ssh git url"""
    return url.startswith("git@")


def download_from_github(url: str, branch: str, dst: Path) -> None:
    """
    Args:
        url: git url
        branch: branch to clone
        dst: Path where to clone the repo

    Raises:
        FileExistsError if dst already exists
    """
    dst.mkdir()

    try:
        subprocess.run(
            ["git", "clone", "-b", branch, url, dst],
            stdout=None,
            stderr=None,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logging.exception(f"An error occurred while downloading from GIT: {e}")
        raise e


def link_local_repo(src, dst):
    logger.info(f"Cloning from {src} to {dst}")
    os.symlink(src, dst)
