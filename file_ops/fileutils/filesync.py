import os
import filecmp
import shutil
from fnmatch import fnmatch
from pathlib import Path


def copy_dir(srcdir, destdir, recursive=False):
    if recursive:
        for root, dirs, files in os.walk(srcdir):
            reldir = Path(root).relative_to(srcdir)

            destreldir = Path(destdir) / reldir
            if not os.path.isdir(destreldir):
                os.makedirs(destreldir)

            for file in files:
                srcfile = Path(root) / file
                destfile = destreldir / file
                print(f'Copying file {srcfile} to {destfile}')
                shutil.copy2(srcfile, destfile)
    else:
        if not Path(destdir).exists():
            Path(destdir).mkdir(parents=True)

        for file in os.listdir(srcdir):
            srcfile = Path(srcdir) / file
            if not srcfile.is_file():
                continue

            srcfile = Path(srcdir) / file
            destfile = Path(destdir) / file
            print(f'Copying file {srcfile} to {destfile}')
            shutil.copy2(srcfile, destfile)


def sync_dir(srcdir, destdir, patterns=None, recursive=False):
    """

    :param str srcdir: Forrás mappa
    :param str destdir: Cél mappa
    :param list[str] or None patterns:
        None esetén minden fájlt szinkronizál, egyébként csak olyan fájlokat amelyekre igazat ad bármelyik pattern

    :return:
    """
    if Path(srcdir).absolute() == Path(destdir).absolute():
        print('srcdir equals to destdir')
        return False

    if patterns is None:
        patterns = ['*']

    if recursive:
        for root, dirs, files in os.walk(srcdir):
            reldir = Path(root).relative_to(srcdir)
            destreldir = Path(destdir) / reldir
            if not destreldir.exists():
                destreldir.mkdir(parents=True)

            for file in files:
                sync_file(Path(root) / file, Path(destreldir) / file, patterns)
    else:
        if not Path(destdir).exists():
            Path(destdir).mkdir(parents=True)

        for file in os.listdir(srcdir):
            sync_file(Path(srcdir) / file, Path(destdir) / file, patterns)

    return True


def sync_file(srcfile, destfile, patterns=None):
    """

    :param str srcfile: Forrás fájl
    :param str destfile: Cél fájl
    :param list[str] or None patterns:
        None esetén minden fájlt szinkronizál, egyébként csak olyan fájlokat amelyekre igazat ad bármelyik pattern

    :return:
    """
    if patterns is None:
        patterns = ['*']

    if not Path(srcfile).is_file():
        return False

    for pattern in patterns:
        if fnmatch(Path(srcfile).name, pattern):
            break
    else:
        print(f'Skipping file {srcfile}. Pattern match fail')
        return False

    if Path(destfile).is_file() and filecmp.cmp(srcfile, destfile):
        print(f'Skipping file {srcfile}. File not changed')
        return False

    print(f'Copying file {srcfile} to {destfile}')
    shutil.copy2(srcfile, destfile)
    return True
