import click
import subprocess

@click.group()
def cli():
    """Dejan CLI for various tools."""
    pass

@cli.command()
def linkbert():
    """Run the LinkBERT Streamlit app."""
    subprocess.run(["streamlit", "run", "dejan/apps/linkbert_app.py"])

if __name__ == "__main__":
    cli()
