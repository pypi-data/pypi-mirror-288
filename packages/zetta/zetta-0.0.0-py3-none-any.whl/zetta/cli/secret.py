import click

import zetta.secret as zsecret

@click.group(help="Manage secrets.")
def secret_cli():
    pass

@secret_cli.command(name="get", help="Get a secret by key.")
@click.argument("key")
def get(key):
    zsecret.get(key)

@secret_cli.command(name="list", help="List your published secrets.")
def list():
    zsecret.list()

@secret_cli.command(name="set", help="Create a new secret.")
@click.argument("key")
@click.argument("value")
def set(key, value):
    zsecret.set(key, value)
