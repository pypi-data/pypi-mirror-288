from typer import Typer, Option
from rich import print
from typing_extensions import Annotated


from tizori_cli.commands.base import base_wrapper
from tizori_cli.wrapper import auth

auth_app = Typer()


@auth_app.command("login")
def login(
    username: Annotated[str, Option(help="Tizori Username", prompt=True)],
    password: Annotated[str, Option(help="Tizori Password", prompt=True, hide_input=True)],
):
    try:
        status, message = auth.login(base_wrapper, username, password)
        if status:
            print("\n[bold green]Login Successful[/bold green]")
        else:
            print(f"\n[red]Login Failed[/red]: {message}")
    except Exception as e:
        print(f"\n[red]Error[/red]: {str(e)}")


@auth_app.command("logout")
def logout():
    try:
        auth.logout()
        print("\n[bold green]Logout Successful[/bold green]")
    except Exception as e:
        print(f"\n[red]Error[/red]: {str(e)}")


@auth_app.command("reset-password")
def reset_password(
    username: Annotated[str, Option(help="Tizori Username", prompt=True)],
):
    try:
        status, message = auth.reset_password(base_wrapper, username)
        if status:
            print("\n[green]Password Reset![/green]")
            # Display generated password
            print(f"Password: [bold blue]{message}[/bold blue]")
        else:
            print(f"\n[red]Error[/red]: {message}")
    except Exception as e:
        print(f"\n[red]Error[/red]: {str(e)}")
