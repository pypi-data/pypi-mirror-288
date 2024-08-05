import click
from dejan.apps.linkbert_app import run_linkbert
from dejan.apps.roo_app import run_roo_app
from dejan.authority import get_authority

@click.group(help="""
Dejan CLI for various tools.

Commands:

- authority: Fetch the authority metric for a given domain.\n
  Examples:\n
  1. Check authority by specifying the domain directly:\n
     dejan authority dejanmarketing.com\n
  2. Check authority by using the --domain option:\n
     dejan authority --domain dejanmarketing.com\n
  3. Prompt for domain if not provided:\n
     dejan authority\n

- roo: Fetch ROO data for a specific date or for the last 'n' days.\n
  Examples:\n
  1. Fetch ROO data for the most recent day (defaults to US mobile):\n
     dejan roo\n
  2. Fetch ROO data for the last 3 days in Australia on desktop:\n
     dejan roo 3 au desktop\n
  3. Fetch ROO data for a specific date (e.g., 2024-07-01) using US mobile:\n
     dejan roo 2024-07-01\n
  4. Fetch ROO data with arguments in any order:\n
     dejan roo au 3 desktop\n
  5. Prompt for missing arguments:\n
     dejan roo 2024-07-01 desktop\n

- linkbert: Run the LinkBERT CLI tool.\n
  Examples:\n
  1. Analyze text with default grouping strategy (phrase):\n
     dejan linkbert --text "LinkBERT is a model developed by Dejan."\n
  2. Analyze text with a specific grouping strategy:\n
     dejan linkbert --text "LinkBERT is a model developed by Dejan." --group token\n
  3. Prompt for text if not provided:\n
     dejan linkbert\n
  4. Use subtoken grouping strategy:\n
     dejan linkbert --text "LinkBERT is a model developed by Dejan." --group subtoken\n
""")
def cli():
    """Dejan CLI for various tools."""
    pass

@cli.command()
@click.option('--text', default=None, help='The text to analyze.')
@click.option('--group', default="phrase", help='Grouping strategy (subtoken, token, phrase). Default is phrase.')
def linkbert(text, group):
    if not text:
        text = click.prompt("Enter text to analyze")
    
    run_linkbert(text, group)

@cli.command()
@click.argument('date_or_days', default="1", required=False)
@click.argument('region', default="us", required=False)
@click.argument('device', default="mobile", required=False)
def roo(date_or_days, region, device):
    run_roo_app(date_or_days, region, device)

@cli.command()
@click.argument('domain', required=False)
@click.option('--domain', '-d', help='The domain to analyze.')
def authority(domain):
    if not domain:
        domain = click.prompt("Enter the domain to analyze")
    
    try:
        authority_value = get_authority(domain)
        click.echo(f"Domain Authority for {domain}: {authority_value:.2f}")
    except ValueError as e:
        click.echo(e)

if __name__ == "__main__":
    cli()
