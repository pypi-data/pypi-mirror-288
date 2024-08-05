# cli.py

import click
from dejan.apps.linkbert_app import run_linkbert
from dejan.apps.roo_app import run_roo_app
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
@click.argument('date_or_days', default="1")  # Default to "1" if not provided
@click.argument('region', default="us")  # Default to "us" if not provided
@click.argument('device', default="mobile")  # Default to "mobile" if not provided
def roo(date_or_days, region, device):
    """
    Fetch ROO data for a specific date or for the last 'n' days.
    
    Arguments:
    - date_or_days: The date (YYYY-MM-DD) or the number of days to look back.
    - region: The region (us or au).
    - device: The device type (desktop or mobile).
    """
    run_roo_app(date_or_days, region, device)

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
