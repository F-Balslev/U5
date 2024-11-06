import socket
import sys
import urllib.request
from io import StringIO
from pathlib import Path

from pypdf import PdfReader


def delete_pdf(file_path):
    if file_path.is_file():
        file_path.unlink()


def pdf_is_corrupt(filename):
    """
    Checks if a pdf-file can be opened
    """
    # Consider implementing a timeout feature (could be done with a new thread)
    try:
        reader = PdfReader(filename, strict=True)

        if len(reader.pages) > 0:
            return False

    except:  # noqa: E722
        pass

    return True


def download_pdf(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        return True

    except:  # noqa: E722
        return False


def download_and_save_pdfs(names, urls, cfg, timeout=15):
    # Set default timeout for downloads
    socket.setdefaulttimeout(timeout)

    # Silence command-line output temporarily because pypdf cannot shut up
    text_trap = StringIO()
    sys.stdout, sys.stderr = text_trap, text_trap

    names["status"] = "Ikke downloadet"

    # Loop through all names and attempt to download the pdf
    for index in names.index:
        pdf_name = None

        # Get name for current pdf in order of priority
        for column_name in cfg["name_column"]:
            tmp_name = names[column_name][index]

            # Check if valid name
            if isinstance(tmp_name, str) and len(tmp_name) > 1:
                pdf_name = tmp_name
                break

        # Skip this file if no valid name found
        if pdf_name is None:
            continue

        # Get full path
        pdf_path = Path(cfg["destination_path"]) / f"{pdf_name}.pdf"
        pdf_path_str = pdf_path.absolute()

        # Attempt to download pdf from urls in order or priority
        for column_name in cfg["download_column"]:
            pdf_url = urls[column_name][index]

            # Skip missing urls
            # Pandas converts missing entries to float(nan) even though datatype is specified as str
            if not isinstance(pdf_url, str) or len(pdf_url) < 1:
                continue

            # Attempt to download pdf from url and save locally
            download_pdf(pdf_url, pdf_path_str)

            # Delete pdf if it's corrupt, otherwise stop attempting more urls
            if pdf_is_corrupt(pdf_path_str):
                delete_pdf(pdf_path)
            else:
                names.loc[index, "status"] = "Downloadet"
                break

    # Unsilence command-line output
    sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
