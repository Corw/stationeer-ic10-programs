from models import config

def main():
    empty_config = config.Config(scripts_configs=[])
    with open("config.json", "w") as f:
        f.write(empty_config.model_dump_json(indent=4))

main()