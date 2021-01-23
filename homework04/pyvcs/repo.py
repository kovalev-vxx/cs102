import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:

    if workdir == ".":
        workdir = pathlib.Path(".")
    if isinstance(workdir, str):
        workdir = pathlib.Path(workdir)

    if ".git" in os.listdir(workdir):
        return workdir / ".git"
    elif workdir.parent.name == ".git":
        return workdir.parent
    elif workdir.name == ".git":
        return workdir
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:

    if not os.getenv("GIT_DIR"):
        os.environ["GIT_DIR"] = ".git"
    workdir = pathlib.Path(workdir)
    if pathlib.Path.is_file(workdir):
        raise Exception(f"{workdir} is not a directory")
    else:
        os.makedirs(f'{workdir}/{os.environ["GIT_DIR"]}')
        os.makedirs(f'{workdir}/{os.environ["GIT_DIR"]}/refs/heads')
        os.makedirs(f'{workdir}/{os.environ["GIT_DIR"]}/refs/tags')
        os.makedirs(f'{workdir}/{os.environ["GIT_DIR"]}/objects')
        with open(f'{workdir}/{os.environ["GIT_DIR"]}/HEAD', "w") as f:
            f.write("ref: refs/heads/master\n")
        with open(f'{workdir}/{os.environ["GIT_DIR"]}/config', "w") as f:
            f.write(
                "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
            )
        with open(f'{workdir}/{os.environ["GIT_DIR"]}/description', "w") as f:
            f.write("Unnamed pyvcs repository.\n")
        return pathlib.Path(workdir / os.environ["GIT_DIR"])
