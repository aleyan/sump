import os
from tree_sitter import Language, Parser

# Paths to the grammar repositories
PYTHON_GRAMMAR = 'tree-sitter-python'
TYPESCRIPT_GRAMMAR = 'tree-sitter-typescript'

# Build the languages library
Language.build_library(
    'build/my-languages.so',
    [
        PYTHON_GRAMMAR,
        TYPESCRIPT_GRAMMAR,
    ]
)

# Load the languages
PY_LANGUAGE = Language('build/my-languages.so', 'python')
TS_LANGUAGE = Language('build/my-languages.so', 'typescript')

parser = Parser()

def parse_files(directory, dump_file):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.ts', '.tsx')):
                file_path = os.path.join(root, file)
                parse_file(file_path, dump_file)

def parse_file(file_path, dump_file):
    with open(file_path, 'r') as f:
        code = f.read()
    
    if file_path.endswith('.py'):
        parser.set_language(PY_LANGUAGE)
    else:
        parser.set_language(TS_LANGUAGE)
    
    tree = parser.parse(bytes(code, 'utf8'))
    root_node = tree.root_node

    # Extract class definitions, method definitions, and imports
    for node in root_node.children:
        if node.type == 'class_definition':
            dump_file.write(f"Class: {node.text.decode('utf8')}\n")
        elif node.type == 'function_definition':
            dump_file.write(f"Function: {node.text.decode('utf8')}\n")
        elif node.type == 'import_statement':
            dump_file.write(f"Import: {node.text.decode('utf8')}\n")

def include_files(file_path, dump_file):
    with open(file_path, 'r') as f:
        content = f.read()
    dump_file.write(content + '\n')

def list_other_files(directory, dump_file):
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(('.py', '.ts', '.tsx', '.md')):
                file_path = os.path.join(root, file)
                dump_file.write(f"Other file: {file_path}\n")
