import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree_content: tp.List[tp.Tuple[int, str, bytes]] = []
    subtrees: tp.Dict[str, tp.List[GitIndexEntry]] = dict()
    files = []
    for x in (gitdir.parent / dirname).glob("*"):
        files.append(str(x))
    for entry in index:
        if entry.name in files:
            tree_content.append((entry.mode, str(gitdir.parent / entry.name), entry.sha1))
        else:
            dname = entry.name.lstrip(dirname).split("/", 1)[0]
            if not dname in subtrees:
                subtrees[dname] = []
            subtrees[dname].append(entry)
    for name in subtrees:
        if dirname != "":
            tree_content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, subtrees[name], dirname + "/" + name)),
                )
            )
        else:
            tree_content.append(
                (
                    0o40000,
                    str(gitdir.parent / dirname / name),
                    bytes.fromhex(write_tree(gitdir, subtrees[name], name)),
                )
            )
    tree_content.sort(key=lambda x: x[1])
    data = b"".join(
        f"{elem[0]:o} {elem[1].split('/')[-1]}".encode() + b"\00" + elem[2] for elem in tree_content
    )
    return hash_object(data, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    seconds_time = str(int(time.mktime(time.localtime()))).encode()
    timezone = "{:+}00".format(int(time.timezone / -3600)).zfill(5).encode()
    if author is None:
        author = "{} <{}>".format(os.getenv("GIT_AUTHOR_NAME"), os.getenv("GIT_AUTHOR_EMAIL"))
    assert isinstance(author, str)
    if parent:
        assert isinstance(parent, str)
        result = b"tree %s\nparent %s\nauthor %s %s %s\ncommitter %s %s %s\n\n%s\n" % (
            tree.encode(),
            parent.encode(),
            author.encode(),
            seconds_time,
            timezone,
            author.encode(),
            seconds_time,
            timezone,
            message.encode(),
        )
    else:
        result = b"tree %s\nauthor %s %s %s\ncommitter %s %s %s\n\n%s\n" % (
            tree.encode(),
            author.encode(),
            seconds_time,
            timezone,
            author.encode(),
            seconds_time,
            timezone,
            message.encode(),
        )
    return hash_object(result, fmt="commit", write=True)