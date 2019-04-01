if __name__ == '__main__':
    # fájl megnyitása olvasásra
    f = open('example.txt', 'r')
    print(f.read())
    f.close()

    print('Open with "with"')
    print('----------------')
    with open('example.txt', 'r') as f:
        print(f.read())

    print('Read line by line')
    print('-----------------')
    with open('example.txt', 'r') as f:
        for line in f:
            print(line)

    print('Writing files')
    print('-------------')
    with open('output.txt', 'w') as f:
        f.write('This is an output file\n\nWith multiple line')

    with open('output_bin.txt', 'wb') as f:
        f.write(b'\x74\x65\x73\x74')

    with open('output_print.txt', 'w') as f:
        print('This is an output file', file=f)
        print('', file=f)
        print('With multiple line', file=f)
