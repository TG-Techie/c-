#!/usr/bin/env python3
import click
import inc_cmns_transpiler as cmnspiler

@click.command()
@click.argument('command', nargs=1)
@click.argument('path', nargs=1, type=click.File('r'))
@click.option('-o', '--out', '--output-destination', 'destination',
                default='a.out', type=click.File('w'),
                help='the target file for the exectable')
def hello(command, path, destination):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"transpiling file '{path.name}':")

if __name__ == '__main__':
    hello()
