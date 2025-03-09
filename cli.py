import click, os

@click.group()
def cli():
    ...


@click.command(help="Run Server")
@click.option('--port', type=int, default=8000, help='Http Server Port')
@click.option('--addr', type=str, default='0.0.0.0', help='Listen address')
@click.option('--ws-port', type=int, default=18080, help='WebSocket Port')
@click.option('--remove-escape', is_flag=True, help="Ablation Escape")
@click.option('--remove-switch', is_flag=True, help="Ablation Switch Pokemon")
@click.option('--shell', is_flag=True, help="Shell")
@click.option('--fight-test', is_flag=True, help="Test fight")
@click.option('--test-count', type=int, default=20, help="Test count")
@click.option('--test-setting', type=str, default='001_simple', help='Test setting')
def server(port, addr, ws_port, remove_escape, remove_switch, shell, fight_test, test_count, test_setting):
    """
    Run server
    """
    os.environ["AI_POKEMON_TRAINER_HTTP_PORT"] = str(port)
    os.environ["AI_POKEMON_TRAINER_LISTEN_ADDR"] = addr
    os.environ["AI_POKEMON_TRAINER_WS_PORT"] = str(ws_port)

    os.environ["AI_POKEMON_TRAINER_SHELL"] = '1' if shell else '0'

    # Ablation Test
    os.environ["AI_POKEMON_TRAINER_ABLATION_ESCAPE"] = '1' if remove_escape else '0'
    os.environ["AI_POKEMON_TRAINER_ABLATION_SWITCH"] = '1' if remove_switch else '0'


    os.environ["AI_POKEMON_TRAINER_FIGHT_TEST"] = '1' if fight_test else '0'
    os.environ["AI_POKEMON_TRAINER_TEST_CNT"] = str(test_count)
    os.environ["AI_POKEMON_TRAINER_TEST_SETTING"] = test_setting
    import app


@click.command(help="Use pyboy window")
@click.option('--remove-escape', is_flag=True, help="Ablation Escape")
@click.option('--remove-switch', is_flag=True, help="Ablation Switch Pokemon")
def local(remove_escape, remove_switch):
    """
    Use pyboy window
    """
    # Ablation Test
    os.environ["AI_POKEMON_TRAINER_ABLATION_ESCAPE"] = '1' if remove_escape else '0'
    os.environ["AI_POKEMON_TRAINER_ABLATION_SWITCH"] = '1' if remove_switch else '0'
    import main


cli.add_command(server)
cli.add_command(local)

if __name__ == '__main__':
    cli()
