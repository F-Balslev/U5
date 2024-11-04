from pathlib import Path


def pe(text=None):
    if text is not None:
        print(text)

    exit()


def attempt_create_file(file_name):
    # Attempt to create destination file
    try:
        open(file_name, "w").close()
    except Exception as e:
        pe(f"Filen kunne ikke oprættes for {file_name}\n{e}")


def read_config_file_to_dict(filename):
    out_vars = {}

    with open(filename) as config_file:
        for line in config_file.readlines():
            # Skip empty lines or line with comments
            if len(line) <= 1 or line[0] == "#":
                continue

            split_line = line.split("=")

            if len(split_line) != 2:
                pe(f"Fandt linje med {len(split_line)} lighedstegn, forventede 1.")

            var, values = split_line

            # Exclude line-break which might not exist if it's the last line
            if values[-1] == "\n":
                values = values[:-1]

            # Insert variables into dict
            match var:
                case "KILDEFIL":
                    out_vars["source_path"] = values
                case "RAPPORTMAPPE":
                    out_vars["destination_path"] = values
                case "STATUSFIL":
                    out_vars["status_path"] = values
                case "NAVNKOLONNETYPE":
                    out_vars["name_column_type"] = values
                case "NAVNKOLONNE":
                    out_vars["name_column"] = values
                case "DOWNLOADKOLONNETYPE":
                    out_vars["download_column_type"] = values
                case "DOWNLOADKOLONNE":
                    out_vars["download_column"] = values
                case _:  # unexpected variable enountered in config
                    pe(f"Fandt uforventet variabel i konfigurationsfil: {var}")

    return out_vars


def validate_config(cfg_vars):
    var_names = [
        ("source_path", "KILDEFIL"),
        ("destination_path", "RAPPORTMAPPE"),
        ("status_path", "STATUSFIL"),
        ("name_column_type", "NAVNKOLONNETYPE"),
        ("name_column", "NAVNKOLONNE"),
        ("download_column_type", "DOWNLOADKOLONNETYPE"),
        ("download_column", "DOWNLOADKOLONNE"),
    ]

    # Check if all variables were set
    for var_name, da_name in var_names:
        if var_name not in cfg_vars.keys():
            pe(f"{da_name} kunne ikke findes i konfigurationsfilen.")

    # Check if source file exists and is of correct type
    source_path = cfg_vars["source_path"]
    if not Path(source_path).is_file():
        pe("Kildefilen kunne ikke findes.")

    if len(source_path) < 5 or source_path[-5:] != ".xlsx":
        pe("Kildefilen er en forkert type.")

    # Check if destination path exists
    destination_path = cfg_vars["destination_path"]
    if not Path(destination_path).is_dir():
        pe("Rapportmappen kunne ikke findes.")

    # Check if status file already exists
    status_path = cfg_vars["status_path"]
    if Path(status_path).is_file():
        pe("Statusfilen eksisterer allerede.")

    if len(status_path) < 5 or status_path[-5:] != ".xlsx":
        pe("Statusfilen er en forkert type.")

    attempt_create_file(status_path)

    # Check if column types are as expected
    for col_name_type in ["name_column_type", "download_column_type"]:
        if cfg_vars[col_name_type] not in ["INDEKS", "NAVN"]:
            pe(f"Uforventet kolonnetype for {col_name_type}")


def str_to_int(index_str: str):
    if index_str.isdigit():
        return int(index_str)

    if not index_str.isalpha():
        pe(f"Indeks kunne ikke konverteres: {index_str}")

    # Convert from excel column notation to zero-indexed int
    # AB -> 27
    base26 = [ord(char) - 96 for char in index_str.lower()]
    num = 0

    for digit in base26:
        num *= 26
        num += digit

    if num > 1000:
        print(
            f"Kolonne med {index_str} er behandlet som INDEKS, men er mugligvis NAVN i stedet"
        )

    return num - 1


def convert_column_headers(cfg_vars):
    for col, col_type in zip(
        ["name_column", "download_column"],
        ["name_column_type", "download_column_type"],
    ):
        match cfg_vars[col_type]:
            case "INDEKS":
                cfg_vars[col] = [str_to_int(idx) for idx in cfg_vars[col].split(",")]
            case "NAVN":
                cfg_vars[col] = cfg_vars[col].split(",")


def read_config(filename="konfiguration.txt"):
    # Get variables from config file
    config_vars = read_config_file_to_dict(filename)

    # Validate the extraced config variables
    validate_config(config_vars)

    # Convert column headers to appropriate format
    convert_column_headers(config_vars)

    return config_vars
