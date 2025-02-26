import click, os

@click.group()
def cli():
    ...


@click.command(help="Run Server")
@click.option('--port', type=int, default=8000, help='Http Server Port')
@click.option('--addr', type=str, default='0.0.0.0', help='Listen address')
@click.option('--ws-port', type=int, default=18080, help='WebSocket Port')
def server(port, addr, ws_port):
    """
    Run server
    """
    os.environ["AI_POKEMON_TRAINER_HTTP_PORT"] = str(port)
    os.environ["AI_POKEMON_TRAINER_LISTEN_ADDR"] = addr
    os.environ["AI_POKEMON_TRAINER_WS_PORT"] = str(ws_port)
    import app


@click.command(help="Use pyboy window")
def local():
    """
    Use pyboy window
    """
    import main


@click.command(help="Run test")
@click.option('--count', type=int, default=1, help='Times')
def test(count):
    """
    Run Test
    """
    ...

cli.add_command(server)
cli.add_command(local)
cli.add_command(test)

if __name__ == '__main__':
    cli()
