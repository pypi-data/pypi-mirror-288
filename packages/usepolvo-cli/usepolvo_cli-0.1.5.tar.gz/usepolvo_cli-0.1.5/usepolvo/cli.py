import click

from .config import save_config
from .stripe import stripe


@click.group()
def cli():
    """Main CLI entry point."""
    pass


@click.group()
def config():
    """Configure API keys for integrations."""
    pass


@click.command()
@click.option("--api-key", prompt="API Key", help="The API key for Stripe.")
def stripe_config(api_key):
    """Configure the Stripe API key."""
    save_config("stripe", api_key)
    click.echo("Stripe API key has been configured.")


config.add_command(stripe_config, name="stripe")

cli.add_command(config)
cli.add_command(stripe)

if __name__ == "__main__":
    cli()
