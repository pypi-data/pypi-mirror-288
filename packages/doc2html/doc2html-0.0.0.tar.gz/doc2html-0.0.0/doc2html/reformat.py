from time import time
from typing import Any, Tuple
from pathlib import Path
import subprocess
import tempfile
from fastapi import UploadFile
from io import BytesIO
import mammoth
import pdfplumber
from bs4 import BeautifulSoup

from doc2html import config as cfg, schemas, server


async def unoserver_convert(
        file_name: Path, file_obj: UploadFile, to_: str,
        interface: str = cfg.TRANSFORM_HOST, port: str = cfg.UNOSERVER_PORT) -> Tuple[bool, Any]:
    """
    Receives the file data and transform the contents to the requested format
    using libreoffice (on unoserver)
    """
    filters = []
    # At the moment unoserver does not detect correctly the filter to use with certain extensions...
    if Path(file_name).suffix in (".pdf", ".ppt", ".pptx"):
        filters = ["--filter", "impress_html_Export"]

    is_unoserver_available = server.is_unoserver_running(timeout=1)

    bytes_data = await file_obj.read()

    with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as tmp_input, \
        tempfile.NamedTemporaryFile(mode="w+b", delete=True) as tmp_output:

        if is_unoserver_available is True:
            # The input and output could be stdin and stdout using "-", "-" but in stdout is not returning anything
            command = [
                cfg.UNO_CONVERTER, "--host", interface, "--port", str(port),
                "--convert-to", to_, *filters, tmp_input.name, tmp_output.name
            ]
        else:
            # Try directly libreoffice (less efficient) if unoserver is not running
            cfg.logger.warning("Unoserver not found. Please ensure unoserver is installed an its environment "
                               "is correct. Running directly libreoffice.")
            command = [
                "libreoffice", "--headless", "--convert-to", to_, *filters,
                tmp_input.name, "--outdir", tmp_output.name
            ]

        #  In theory, it should be possible to run as module, "-m" "unoserver.converter"
        tmp_input.write(bytes_data)
        tmp_input.flush()  # Ensure data is written

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                stderr_text = stderr.decode('utf-8')
                cfg.logger.error("Failed to convert document. Error: %s", stderr_text)
                return False, stderr_text
            else:
                with open(tmp_output.name, 'r') as f_read:
                    output_data = f_read.read()
                cfg.logger.info("Document %s converted successfully to %s.", file_name, to_)
                return True, output_data

        except Exception as err:
            cfg.logger.error("Exception occurred while converting document: %s", str(err))
            return False, str(err)


async def mammoth_convert(file_name: Path, file_obj: UploadFile, to_: str) -> Tuple[bool, Any]:
    """Transform docx to html or text"""
    if Path(file_name).suffix not in (".doc", ".docx"):
        raise Exception("File extension must be .doc or .docx")
    to_ = "html" if to_ == "htm" else to_
    if to_ not in ("html", "text"):
        raise Exception("Format conversion must be to html or text")

    if to_ == "html":
        convert_func = mammoth.convert_to_html
    elif to_ == "text":
        convert_func = mammoth.extract_raw_text

    try:
        contents = await file_obj.read()
        doc_stream = BytesIO(contents)

        result = convert_func(doc_stream)
        extracted_data = result.value  # The generated HTML or raw text
        messages = result.messages  # Any messages, such as warnings during conversion
        if messages:
            cfg.logger.warning(f"{messages}")

        return True, extracted_data

    except Exception as err:
        cfg.logger.error("Exception occurred while converting document: %s", str(err))
        return False, str(err)


async def plumber_convert(file_name: Path, file_obj: UploadFile, to_: str) -> Tuple[bool, Any]:
    """Transform pdf to html"""
    if to_ not in ("html", "htm"):
        raise ValueError("Format conversion must be to html or htm")

    bytes_data = await file_obj.read()

    with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as tmp_input:

        tmp_input.write(bytes_data)
        tmp_input.flush()  # Ensure data is written

        try:

            with pdfplumber.open(tmp_input) as pdf:
                soup = BeautifulSoup(
                    '<html><head><style>.pdf-text { position: absolute; }</style></head><body></body></html>',
                    'html.parser'
                )
                body = soup.body

                for idx, page in enumerate(pdf.pages):
                    page_div = soup.new_tag("div", style=f"position: relative; width: {page.width}pt; height: {page.height}pt;")
                    body.append(page_div)

                    for char in page.extract_words():
                        left = char['x0']
                        top = char['top']
                        text = char['text']

                        span = soup.new_tag("span", **{"class": "pdf-text", "style": f"left: {left}pt; top: {top}pt;"})
                        span.string = text
                        page_div.append(span)
        except Exception as err:
            cfg.logger.error("Exception occurred while converting document: %s", str(err))
            return False, str(err)

    return True, str(soup)


DEFAULT_PARSERS = {
    "docx": mammoth_convert,
    "odt": mammoth_convert,
    "doc": unoserver_convert,
    "pdf": unoserver_convert,
    "ppt": unoserver_convert,
    "pptx": unoserver_convert,
}


async def to_format(file_obj: UploadFile, to_: str = "html", parser: str = "defaults") -> dict:
    """Transform the document received to the requested format."""
    t_ini = time()
    file_name = Path(file_obj.filename)

    if file_name.suffix in (".doc", ".docx", ".odt", ".pdf", ".ppt", ".pptx"):
        from_ = file_name.suffix.lower()[1:]
        cfg.logger.debug("Input format: %s", from_)
    else:
        return {"status": "nok", "message": "Unexpected file format"}

    # Manage parser preferences
    if parser == "defaults":
        parser_func = DEFAULT_PARSERS[from_]
    elif parser in ("mammoth", "mammoth_convert"):
        parser_func = mammoth_convert
    else:
        parser_func = unoserver_convert

    is_ok, new_format = await parser_func(file_name, file_obj, to_)

    return schemas.TransformOutput(
        status="ok" if is_ok else "error",
        data=new_format,
        runtime=round(time() - t_ini, 2)
    )
