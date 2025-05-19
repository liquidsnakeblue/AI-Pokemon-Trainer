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
@click.option('--remove-item', is_flag=True, help="Ablation Item")
@click.option('--shell', is_flag=True, help="Shell")
@click.option('--no-auto', is_flag=True, help="Not have automatic play")
@click.option('--fight-test', is_flag=True, help="Test fight")
@click.option('--base-line', is_flag=True, help="Base Line")
@click.option('--test-count', type=int, default=20, help="Test count")
@click.option('--test-setting', type=str, default='001_simple', help='Test setting')
@click.option('--skip-animation', is_flag=True, help="Is skip animation")
@click.option('--debug', is_flag=True, help="Debug mod")
def server(port, addr, ws_port, remove_escape, remove_switch, remove_item, shell, no_auto, fight_test, base_line, test_count, test_setting, skip_animation, debug):
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
    os.environ["AI_POKEMON_TRAINER_ABLATION_ITEM"] = '1' if remove_item else '0'


    os.environ["AI_POKEMON_TRAINER_FIGHT_TEST"] = '1' if fight_test else '0'
    os.environ["AI_POKEMON_TRAINER_BASE_LINE"] = '1' if base_line else '0'
    os.environ["AI_POKEMON_TRAINER_TEST_CNT"] = str(test_count)
    os.environ["AI_POKEMON_TRAINER_TEST_SETTING"] = test_setting

    os.environ["AI_POKEMON_TRAINER_SKIP_ANIMATION"] = '1' if skip_animation else '0'
    os.environ["AI_POKEMON_TRAINER_NO_AUTO"] = '1' if no_auto else '0'
    os.environ["AI_POKEMON_TRAINER_DEBUG"] = '1' if debug else '0'
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
