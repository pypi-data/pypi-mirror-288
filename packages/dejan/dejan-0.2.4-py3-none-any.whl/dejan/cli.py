import click
from dejan.apps.linkbert_app import run_linkbert
from dejan.authority import get_authority

@click.group()
def cli():
    """Dejan CLI for various tools."""
    pass

@cli.command()
def linkbert():
    """Run the LinkBERT CLI tool."""
    run_linkbert()

@cli.command()
@click.argument('domain')
def authority(domain):
    """Fetch the authority metric for a given domain."""
    try:
        authority_value = get_authority(domain)
        click.echo(f"Domain Authority for {domain}: {authority_value:.2f}")
    except ValueError as e:
        click.echo(e)

if __name__ == "__main__":
    cli()
