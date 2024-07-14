import os
import click
from .parser import summarize_project

@click.command()
@click.option('--directory', '-d', default='.', help='Directory to summarize')
@click.option('--output_file', '-o', default=None, help='Write summary to file')
@click.option('--include', '-i', multiple=True, help='Files to include fully')
def main(directory: str, output_file: str, include: tuple):
    summary = summarize_project(directory, include)
    
    if output_file is not None:
        with open(output_file, 'w') as dump_file:
            dump_file.write(summary)
        click.echo(f"Project summary written to dump.txt")
    else:
        print(summary)
    

if __name__ == '__main__':
    main()
