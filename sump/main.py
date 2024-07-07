import os
import click
from .parser import summarize_project

@click.command()
@click.option('--directory', '-d', default='.', help='Directory to summarize')
@click.option('--include', '-i', multiple=True, help='Files to include fully')
def main(directory: str, include: tuple):
    summary = summarize_project(directory, include)
    
    with open('dump.txt', 'w') as dump_file:
        dump_file.write(summary)
    
    click.echo(f"Project summary written to dump.txt")

if __name__ == '__main__':
    main()
