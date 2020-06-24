import re

indent = 0

def debug(*args):
    print('    '*indent + ' '.join([str(arg) for arg in args]))

def path_from_filepath(filepath):
    filepath = str(filepath)
    while len(filepath) and not filepath.endswith('/'):
        print(filepath)
        filepath = filepath[0:-1]
    return filepath

def build(source_path):
    with open(source_path, 'r') as file:
        file_paths = re.findall(r'#include[ \t]*("[\w\./\\]*")', file.read())
    file_paths = [file.strip('\'"') for file in file_paths]
    file_paths = [re.sub(r'\w/\.\.', '', file) for file in file_paths]

    debug(source_path, '>', file_paths)

    #find currect source_path
    curpath = path_from_filepath(source_path) #re.sub(r'\w/\.\.', '', source_path)


    debug(source_path, '>', curpath)

    all = [curpath+file for file in file_paths]
    out = list(all)

    global indent
    indent += 1
    for file in all:
        out += build(file)
    indent -= 1

    debug(source_path, '>', out)

    clipped_out = []
    for path in out:
        words = path.split('/..')
        words = [path_from_filepath(word) for word in words[0:-1]] + [words[-1]]
        clipped_out.append(''.join(words))

    return [path.replace('//', '').strip('/') for path in clipped_out]
