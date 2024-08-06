from pathlib import Path


def dot_git_parent_path(p: Path) -> Path:
    """
    Find the parent directory of a git repository.
    Args:
        p: Starting point where start to scan

    Returns:
        Path of the directory that contains .git directory
    Raises:
        FileNotFoundError if / is reached without find any .git directory
    """
    current_p = p.resolve()
    while current_p.parent != current_p:
        if (current_p / ".git").is_dir():
            return current_p
        current_p = current_p.parent
    raise FileNotFoundError(
        f"fatal: not a git repository (or any parent up to mount point /) in {p}"
    )
