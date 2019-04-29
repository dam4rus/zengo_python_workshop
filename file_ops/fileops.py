from fileutils import hash
from fileutils.filesync import copy_dir, sync_dir

if __name__ == '__main__':
    print('--- copy ---')
    copy_dir('assets', 'test/copy')
    print('--- copy recursive ---')
    copy_dir('assets', 'test/copy_recursive', True)
    print('--- sync ---')
    sync_dir('assets', 'test/sync')
    print('--- sync recursive ---')
    sync_dir('assets', 'test/sync_recursive', recursive=True)

    print('--- generating md5 for assets/loremipsum.txt')
    print(hash.generate_md5_for_file('assets/loremipsum.txt'))
    hash.generate_md5_file_for_file('assets/loremipsum.txt', 'test/loremipsum.md5')
