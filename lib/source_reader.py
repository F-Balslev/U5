import pandas as pd

from lib.config_reader import pe


def check_valid_columns(cfg_vars, col_names):
    col_types = [
        ("download_column_type", "download_column"),
        ("name_column_type", "name_column"),
    ]

    for col_t, col in col_types:
        if cfg_vars[col_t] == "INDEKS":
            for idx in cfg_vars[col]:
                if idx >= len(col_names):
                    pe(
                        f"Kildefilen har {len(col_names)} kolonner, men kolonne {idx} er angivet i kofigurationsfilen."
                    )
        else:
            for col_name in cfg_vars[col]:
                if col_name not in col_names:
                    pe(f"Kolonne {col_name} kunne ikke findes i kildefilen.")


def load_dataframes(cfg_vars):
    """
    Loads dataframes and converts column index to column name
    """

    df = pd.read_excel(cfg_vars["source_path"], dtype=str)
    col_names = df.columns

    # Check if specified columns exist
    check_valid_columns(cfg_vars, col_names)

    # Convert column indexes to names
    if cfg_vars["name_column_type"] == "INDEKS":
        cfg_vars["name_column_type"] = "NAVN"
        cfg_vars["name_column"] = [col_names[idx] for idx in cfg_vars["name_column"]]

    if cfg_vars["download_column_type"] == "INDEKS":
        cfg_vars["download_column_type"] = "NAVN"
        cfg_vars["download_column"] = [
            col_names[idx] for idx in cfg_vars["download_column"]
        ]

    # Return dataframes
    return df[cfg_vars["name_column"]].copy(), df[cfg_vars["download_column"]].copy()
