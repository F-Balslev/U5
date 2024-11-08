from lib.config_reader import read_config
from lib.pdf_downloader import download_and_save_pdfs
from lib.source_reader import load_dataframes
from lib.status_writer import write_status_file


def main():
    config_file_name = "konfiguration.txt"
    timeout = 15
    num_threads = 10

    # Load config
    config = read_config(config_file_name)

    # Load dataframes
    name_df, url_df, include_df = load_dataframes(config)

    # Download and save the pdfs
    download_and_save_pdfs(
        name_df,
        url_df,
        include_df,
        config,
        timeout,
        num_threads,
    )

    # Create a status file
    write_status_file(name_df, config["status_path"])


if __name__ == "__main__":
    main()
