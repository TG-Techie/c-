import click


@click.group()
def entry():
    pass

@entry.command()
@click.argument('file')  # add the name argument
def run(**kwargs):
    print(kwargs)

if __name__ == '__main__':
    entry()
