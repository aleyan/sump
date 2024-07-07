import os
from typing import List, Tuple
from tree_sitter import Parser, Tree, Node
from tree_sitter_languages import get_parser
import fnmatch

def _get_parser(file_extension: str) -> Parser:
    if file_extension == '.py':
        parser = get_parser('python')
    elif file_extension in ('.ts', '.tsx'):
        parser = get_parser('typescript')
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    return parser

def read_gitignore(directory: str) -> List[str]:
    gitignore_path = os.path.join(directory, '.gitignore')
    if not os.path.exists(gitignore_path):
        return []
    
    with open(gitignore_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def is_ignored(file_path: str, ignore_patterns: List[str], base_dir: str) -> bool:
    rel_path = os.path.relpath(file_path, base_dir)

    if rel_path.startswith('.git' + os.sep) or rel_path == '.git':
        return True

    return any(fnmatch.fnmatch(rel_path, pattern) for pattern in ignore_patterns)


def summarize_project(directory: str, include_files: Tuple[str]) -> str:
    summary = []
    ignore_patterns = read_gitignore(directory)
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_ignored(file_path, ignore_patterns, directory):
                continue
            
            if file.endswith(('.py', '.ts', '.tsx')):
                summary.append(summarize_code_file(file_path))
            elif file.endswith('.md'):
                summary.append(include_markdown_file(file_path))
            elif file_path in include_files:
                summary.append(include_full_file(file_path))
            else:
                summary.append(f"File: {file_path}")
    return '\n\n'.join(summary)

def summarize_code_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read()
    
    file_extension = os.path.splitext(file_path)[1]
    parser = _get_parser(file_extension)
    tree = parser.parse(bytes(content, 'utf8'))

    summary = [f"File: {file_path}"]
    summary.extend(extract_imports(tree, content))
    summary.extend(extract_classes_and_methods(tree, content))
    
    return '\n'.join(summary)

def extract_imports(tree: Tree, content: str) -> List[str]:
    imports = []
    root_node = tree.root_node
    
    import_nodes = [
        child for child in root_node.children
        if child.type in ('import_statement', 'import_from_statement', 'import_declaration')
    ]
    
    for node in import_nodes:
        imports.append(content[node.start_byte:node.end_byte].strip())
    
    return ["Imports:"] + imports if imports else []

def extract_classes_and_methods(tree: Tree, content: str) -> List[str]:
    classes_and_methods = []
    root_node = tree.root_node
    
    for child in root_node.children:
        if child.type == 'class_definition':
            classes_and_methods.extend(extract_class(child, content))
        elif child.type in ('function_definition', 'method_definition'):
            classes_and_methods.append(extract_method(child, content))
    
    return classes_and_methods

def extract_class(node: Node, content: str) -> List[str]:
    class_name = next(child for child in node.children if child.type == 'identifier').text.decode('utf-8')
    class_def = [f"Class: {class_name}"]
    
    for child in node.children:
        if child.type in ('function_definition', 'method_definition'):
            class_def.append(f"  {extract_method(child, content)}")
    
    return class_def

def extract_method(node: Node, content: str) -> str:
    method_name = next(child for child in node.children if child.type == 'identifier').text.decode('utf-8')
    parameters = [
        param.text.decode('utf-8') for param in node.children 
        if param.type == 'parameters'
    ]
    return_type = next(
        (child for child in node.children if child.type == 'type'), 
        None
    )
    return_type_str = return_type.text.decode('utf-8') if return_type else 'None'
    parameters_str = ", ".join(parameters)
    return f"Method: {method_name}({parameters_str}) -> {return_type_str}"


def include_markdown_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read()
    return f"File: {file_path}\n\n{content}"

def include_full_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read()
    return f"File: {file_path}\n\n{content}"