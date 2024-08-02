import asyncio

import click
from usepolvo.stripe.customers import StripeClient

from .config import get_api_key


@click.group()
def stripe():
    """Stripe integration commands."""
    pass


def get_stripe_client():
    api_key = get_api_key("stripe")
    if not api_key:
        click.echo(
            "Stripe API key is not configured. Please run 'usepolvo config stripe --api-key <your_api_key>' to configure it."
        )
        return None
    return StripeClient(api_key)


@click.command()
def list_customers():
    """List customers in Stripe."""
    client = get_stripe_client()
    if client:
        asyncio.run(_list_customers(client))


async def _list_customers(client):
    customers = await client.customers.list_customers()
    for customer in customers:
        click.echo(f"Customer ID: {customer.id}, Email: {customer.email}")


@click.command()
@click.option("--email", prompt="Customer Email", help="The email of the customer.")
def create_customer(email):
    """Create a new customer in Stripe."""
    client = get_stripe_client()
    if client:
        asyncio.run(_create_customer(client, email))


async def _create_customer(client, email):
    customer = await client.customers.create_customer(email=email)
    click.echo(f"Created Customer ID: {customer.id}, Email: {customer.email}")


stripe.add_command(list_customers)
stripe.add_command(create_customer)
