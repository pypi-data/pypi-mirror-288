import typer

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Coolify CLI tool
    """


@app.command()
def help():
    """
    Help info
    """
    typer.echo("Help for coolify CLI")
