import pytest
from hamcrest import assert_that, equal_to
import aiofiles

from doc2html import config as cfg, reformat, server
from tests.expected import *


@pytest.mark.asyncio
async def test__mammoth_convert() -> None:
    """Validate mammoth behaviour with big file"""
    file_name = "SampleDOCFile_2MB.docx"
    sample = cfg.SAMPLES.joinpath(file_name)
    async with aiofiles.open(sample, 'rb') as file_obj:
        success, data = await reformat.mammoth_convert(file_name, file_obj, "html")

    assert_that((success, data), equal_to((True, EXPECTED_2MB_DOCX_OUTPUT)))
