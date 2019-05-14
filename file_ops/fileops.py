from fileutils import hash
from fileutils.filesync import copy_dir, sync_dir
from pathlib import Path
import subprocess
import sys
import shutil
from filecmp import dircmp

assets_dir = 'assets'


def test_md5_file_for_file(md5_file_path):
    if not md5_file_path.exists():
        return False

    with open(md5_file_path, 'r') as f:
        return f.read() == '99f375913bc65028fc6e8549078035d1'


if __name__ == '__main__':
    if Path('test').is_dir():
        shutil.rmtree('test')

    Path('test').mkdir(parents=True)

    print('--- copy ---')
    copy_dir(assets_dir, 'test/copy')
    print('--- copy recursive ---')
    copy_dir(assets_dir, 'test/copy_recursive', recursive=True)
    print('--- copy only txt ---')
    copy_dir(assets_dir, 'test/copy_pattern', ['*.txt'])
    print('--- copy only css recursive --- ')
    copy_dir(assets_dir, 'test/copy_pattern_recursive', ['*.txt'], True)

    print('--- sync ---')
    sync_dir(assets_dir, 'test/sync')
    print('--- sync recursive ---')
    sync_dir(assets_dir, 'test/sync_recursive', recursive=True)
    print('--- sync only txt ---')
    sync_dir(assets_dir, 'test/sync_pattern', ['*.txt'])
    print('--- sync only css recursive --- ')
    sync_dir(assets_dir, 'test/sync_pattern_recursive', ['*.txt'], True)

    print('--- testing md5 generation ---')
    assert hash.generate_md5_for_file(Path(assets_dir) / 'loremipsum.txt') == '99f375913bc65028fc6e8549078035d1'
    print('SUCCESS')

    print('--- testing md5 file generation ---')

    Path('test/md5_file').mkdir()
    hash.generate_md5_file_for_file(Path(assets_dir) / 'loremipsum.txt', 'test/md5_file/loremipsum.txt')
    assert test_md5_file_for_file(Path('test/md5_file/loremipsum.txt'))
    print('SUCCESS')

    print('--- testing md5 generation CLI ---')
    assert str(subprocess.check_output([
        sys.executable,
        '-m',
        'fileutils.hash',
        str(Path(assets_dir) / 'loremipsum.txt')
    ]), encoding=sys.getdefaultencoding()).strip() == '99f375913bc65028fc6e8549078035d1'
    print('SUCCESS')

    print('--- testing md5 generation for file CLI ---')
    Path('test/md5_file_cli').mkdir()
    subprocess.call([
        sys.executable,
        '-m',
        'fileutils.hash',
        str(Path(assets_dir) / 'loremipsum.txt'),
        '-o',
        str('test/md5_file_cli/loremipsum.txt')
    ])
    print('SUCCESS')

    print('--- testing copy_dir CLI ---')
    Path('test/copy_dir_cli').mkdir()
    subprocess.call([
        sys.executable,
        '-m',
        'fileutils.filesync',
        'copy_dir',
        assets_dir,
        'test/copy_dir_cli',
        '-r',
    ])

    assert len(dircmp(assets_dir, 'test/copy_dir_cli').diff_files) == 0
    assert len(dircmp(Path(assets_dir) / 'static', 'test/copy_dir_cli/static').diff_files) == 0
    print('SUCCESS')

    print('--- testing sync_dir CLI ---')
    Path('test/sync_dir_cli').mkdir()
    subprocess.call([
        sys.executable,
        '-m',
        'fileutils.filesync',
        'sync_dir',
        assets_dir,
        'test/sync_dir_cli',
        '-r',
    ])
    assert len(dircmp(assets_dir, 'test/sync_dir_cli').diff_files) == 0
    assert len(dircmp(Path(assets_dir) / 'static', 'test/sync_dir_cli/static').diff_files) == 0
    print('SUCCESS')

    print('--- testing sync_file CLI ---')
    subprocess.call([
        sys.executable,
        '-m',
        'fileutils.filesync',
        'sync_file',
        str(Path(assets_dir) / 'loremipsum.txt'),
        str(Path('test/sync_dir_cli') / 'loremipsum.txt'),
    ])

    assert (Path('test/sync_dir_cli') / 'loremipsum.txt').is_file()
    print('SUCCESS')
