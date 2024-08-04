# dejan/dirtree.py

import os

def generate_ascii_tree(root_dir=None, prefix=""):
    """
    Recursively generates an ASCII representation of the directory structure.
    
    :param root_dir: The root directory to start generating the tree from.
    :param prefix: The string prefix to add to the current line (used for indentation).
    """
    if root_dir is None:
        root_dir = os.getcwd()
        
    contents = os.listdir(root_dir)
    pointers = ['├── '] * (len(contents) - 1) + ['└── ']
    
    for pointer, path in zip(pointers, contents):
        full_path = os.path.join(root_dir, path)
        print(prefix + pointer + path)
        
        if os.path.isdir(full_path):
            extension = '│   ' if pointer == '├── ' else '    '
            generate_ascii_tree(full_path, prefix + extension)
