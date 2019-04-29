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
                srcfile = Path(root) / file
                for pattern in patterns:
                    if fnmatch(Path(srcfile).name, pattern):
                        break
                else:
                    print(f'Skipping file {srcfile}. Pattern match fail')
                    continue

                sync_file(srcfile, Path(destreldir) / file)
    else:
        if not Path(destdir).exists():
            Path(destdir).mkdir(parents=True)

        for file in os.listdir(srcdir):
            srcfile = Path(srcdir) / file
            for pattern in patterns:
                if fnmatch(Path(srcfile).name, pattern):
                    break
            else:
                print(f'Skipping file {srcfile}. Pattern match fail')
                continue

            sync_file(srcfile, Path(destdir) / file)

    return True


def sync_file(srcfile, destfile):
    """

    :param str srcfile: Forrás fájl
    :param str destfile: Cél fájl
    :return:
    """
    if not Path(srcfile).is_file():
        return False

    if Path(destfile).is_file() and filecmp.cmp(srcfile, destfile):
        print(f'Skipping file {srcfile}. File not changed')
        return False

    print(f'Copying file {srcfile} to {destfile}')
    shutil.copy2(srcfile, destfile)
    return True


if __name__ == '__main__':
    import argparse

    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest='command')

    copydirparser = subparsers.add_parser('copy_dir')
    copydirparser.add_argument(dest='srcdir')
    copydirparser.add_argument(dest='destdir')
    copydirparser.add_argument('-r', '--recursive',
                               action='store_true')

    syncfileparser = subparsers.add_parser('sync_file')
    syncfileparser.add_argument(dest='srcfile')
    syncfileparser.add_argument(dest='destfile')

    syncdirparser = subparsers.add_parser('sync_dir')
    syncdirparser.add_argument(dest='srcdir')
    syncdirparser.add_argument(dest='destdir')
    syncdirparser.add_argument('-r', '--recursive',
                               action='store_true')
    syncdirparser.add_argument('-p', '--patterns',
                               nargs='+',
                               default='*')

    args = argparser.parse_args()
    if args.command == 'copy_dir':
        copy_dir(args.srcdir, args.destdir, args.recursive)
    elif args.command == 'sync_file':
        sync_file(args.srcfile, args.destfile)
    elif args.command == 'sync_dir':
        sync_dir(args.srcdir, args.destdir, args.patterns, args.recursive)
