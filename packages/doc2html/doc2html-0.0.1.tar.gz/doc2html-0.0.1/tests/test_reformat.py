import pytest
from hamcrest import assert_that, equal_to
import aiofiles

from doc2html import config as cfg, reformat, server
from tests import utils
from tests.expected import *


@pytest.fixture(scope='module', autouse=True)
def setup_unoserver():
    # Perform the setup for the module which in this case is to ensure unoserver is running
    print("Starting unoserver...")
    server.sync_start_uno_server()

    yield  # This marks the point after which the teardown code can execute

    # You can add any cleanup code here, if necessary
    print("Stopping unoserver...")
    utils.find_and_kill_process_by_port(cfg.UNOSERVER_PORT)


TEST_CONVERT = [
    ("word_model.docx", EXPECTED_WORD_OUTPUT),
    ("pdf_model.pdf", EXPECTED_PDF_OUTPUT),
    ("pdf_model.pdf", EXPECTED_PDF_OUTPUT),
    ("odt_model.odt", EXPECTED_ODT_OUTPUT),
    ("word97.doc", EXPECTED_WORD97_OUTPUT),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("file_name, expected_output", TEST_CONVERT)
async def test__unoserver_convert_pptx(file_name: str, expected_output: str) -> None:
    sample = cfg.SAMPLES.joinpath(file_name)
    async with aiofiles.open(sample, 'rb') as file_obj:
        success, data = await reformat.unoserver_convert(file_name, file_obj, "htm")

    assert_that((success, data), equal_to((True, expected_output)))


async def t__big_doc() -> None:
    """
    The behaviour can be tested calling directly libreoffice. Headless libreoffice fails to load the file

      libreoffice --headless --convert-to htm ./tests/samples/SampleDOCFile_2000kb.doc  output.htm
    """
    file_name = "SampleDOCFile_2000kb.doc"
    sample = cfg.SAMPLES.joinpath(file_name)
    with open(sample, 'rb') as file_obj:
       bytes_data = file_obj.read()

    success, data = await reformat.convert(file_name, bytes_data, "htm")

    assert_that((success, data), equal_to((True, 1)))
