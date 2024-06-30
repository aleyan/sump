import os
from tree_sitter import Language, Parser

PY_LANGUAGE = Language('path/to/python.so', 'python')
TS_LANGUAGE = Language('path/to/typescript.so', 'typescript')

def summarize_project(directory: str, include_files: tuple) -> str:
    summary = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
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
    
    if file_path.endswith('.py'):
        language = PY_LANGUAGE
    else:
        language = TS_LANGUAGE
    
    parser = Parser()
    parser.set_language(language)
    tree = parser.parse(bytes(content, 'utf8'))

    summary = [f"File: {file_path}"]
    summary.extend(extract_imports(tree))
    summary.extend(extract_classes_and_methods(tree))
    
    return '\n'.join(summary)

def extract_imports(tree):
    # Implement import extraction logic
    pass

def extract_classes_and_methods(tree):
    # Implement class and method extraction logic
    pass

def include_markdown_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read()
    return f"File: {file_path}\n\n{content}"

def include_full_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        content = f.read()
    return f"File: {file_path}\n\n{content}"