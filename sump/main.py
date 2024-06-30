import os
import click
from .parser import parse_files, include_files, list_other_files

@click.command()
@click.argument('directory', default='.')
@click.option('--include', multiple=True, help='List of files to include fully')
def main(directory, include):
    with open('dump.txt', 'w') as dump_file:
        # Include specified files
        for file_path in include:
            include_files(file_path, dump_file)
        
        # Parse and summarize py, ts, tsx files
        parse_files(directory, dump_file)
        
        # List other files
        list_other_files(directory, dump_file)

if __name__ == '__main__':
    main()
