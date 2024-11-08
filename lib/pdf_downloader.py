import multiprocessing
import sys
from io import StringIO
from pathlib import Path

import requests
from pypdf import PdfReader

from lib.source_reader import files_exist_filter


def delete_pdf(file_path):
    if file_path.is_file():
        file_path.unlink()


def pdf_is_corrupt(filename):
    """
    Checks if a pdf-file can be opened
    """
    # Consider implementing a timeout feature (could be done with a new thread)

    # Silence command-line output temporarily because pypdf cannot shut up
    # A little dangerous if something goes wrong
    # Needs to be set per thread
    text_trap = StringIO()
    sys.stdout, sys.stderr = text_trap, text_trap

    could_be_read = False

    try:
        reader = PdfReader(filename, strict=True)

        if len(reader.pages) > 0:
            could_be_read = True

    except:  # noqa: E722
        pass

    # Unsilence command-line output
    sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__

    return could_be_read


def download_pdf(url, filename, timeout=30):
    try:
        response = requests.get(url, timeout=timeout)

        with open(filename, "wb") as file:
            file.write(response.content)
        return True

    except:  # noqa: E722
        return False


def process_single_pdf(name, url, cfg_vars):
    pdf_name = None

    # Get name for current pdf in order of priority
    for column_name in cfg_vars["name_column"]:
        tmp_name = name[column_name]

        # Check if valid name
        if isinstance(tmp_name, str) and len(tmp_name) > 1:
            pdf_name = tmp_name
            break

    # Skip this file if no valid name found
    if pdf_name is None:
        return

    # Get full path
    pdf_path = Path(cfg_vars["destination_path"]) / f"{pdf_name}.pdf"
    pdf_path_str = pdf_path.absolute()

    # Attempt to download pdf from urls in order or priority
    for column_name in cfg_vars["download_column"]:
        pdf_url = url[column_name]

        # Skip missing urls
        # Pandas converts missing entries to float(nan) even though datatype is specified as str
        if not isinstance(pdf_url, str) or len(pdf_url) < 1:
            continue

        # Attempt to download pdf from url and save locally
        download_pdf(pdf_url, pdf_path_str, cfg_vars["timeout"])

        # Delete pdf if it's corrupt, otherwise stop attempting more urls
        if pdf_is_corrupt(pdf_path_str):
            delete_pdf(pdf_path)
        else:
            return

    return


def download_and_save_pdfs(names, urls, include, cfg):
    # Start the pool of workers
    pool = multiprocessing.Pool(cfg["num_threads"])

    # Iterator of the indexes to include
    indexes = include.index[include]

    # Loop through all names and attempt to download the pdf
    for index in indexes:
        pool.apply_async(
            func=process_single_pdf,
            args=(
                names.iloc[index],
                urls.iloc[index],
                cfg,
            ),
        )

    pool.close()
    pool.join()

    # Update the status of the newly downloaded files
    file_exists = files_exist_filter(names, cfg)
    not_old_files = names["_status"] != "Downloadet i forvejen"

    names.loc[file_exists & not_old_files, "_status"] = "Downloadet"
