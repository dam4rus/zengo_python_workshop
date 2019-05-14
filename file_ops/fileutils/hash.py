import hashlib
from pathlib import Path


def generate_md5_for_file(file_path):
    """

    :param str or Path file_path: Melyik fájlból generáljon md5-t
    :return str: Generált md5
    """
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        buffer = f.read(4096)
        while buffer:
            md5.update(buffer)
            buffer = f.read(4096)

        return md5.hexdigest()


def generate_md5_file_for_file(file_path, md5_file_path):
    """

    :param str or Path file_path: Melyik fájlból generáljon md5-t
    :param str or Path md5_file_path: Generált md5 fájl elérési útja
    :return:
    """
    with open(md5_file_path, 'w+') as f:
        f.write(generate_md5_for_file(file_path))


if __name__ == '__main__':
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(dest='srcfile')
    argparser.add_argument('-o', '--output')

    args = argparser.parse_args()

    if args.output is not None:
        generate_md5_file_for_file(args.srcfile, args.output)
    else:
        print(generate_md5_for_file(args.srcfile))
