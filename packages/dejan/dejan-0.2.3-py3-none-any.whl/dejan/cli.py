import click
from dejan.apps.linkbert_app import run_linkbert

@click.group()
def cli():
    """Dejan CLI for various tools."""
    pass

@cli.command()
@click.option('--text', prompt='Enter text to analyze', help='The text you want to analyze for link predictions.')
@click.option('--group', default='token', help='The grouping strategy to use: subtoken, token, or phrase.')
def linkbert(text, group):
    """Run the LinkBERT CLI tool."""
    run_linkbert(text, group)

if __name__ == "__main__":
    cli()
