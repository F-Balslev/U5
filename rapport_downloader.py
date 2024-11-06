from lib.config_reader import read_config
from lib.pdf_downloader import download_and_save_pdfs
from lib.source_reader import load_dataframes

if __name__ == "__main__":
    config_file_name = "konfiguration.txt"

    # Load config
    config = read_config(config_file_name)

    # Load dataframes
    name_df, url_df = load_dataframes(config)

    # Download and save the pdfs
    download_and_save_pdfs(name_df, url_df)
