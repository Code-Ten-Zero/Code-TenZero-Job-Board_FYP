import click
from flask.cli import AppGroup
from App.controllers.base_user_account import (
    get_all_users, get_all_users_json
)

user_cli = AppGroup('user', help='User commands')

@user_cli.command("list", help="List all users")
@click.argument("format", default="string")
def list_user_command(format):
    print(get_all_users() if format == 'string' else get_all_users_json())
