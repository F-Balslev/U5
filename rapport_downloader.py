from lib.config_reader import read_config
from lib.source_reader import load_dataframes

if __name__ == "__main__":
    config_file_name = "konfiguration.txt"

    # Load config
    config = read_config(config_file_name)

    # Load dataframes
    name_df, download_df = load_dataframes(config)

    breakpoint()
