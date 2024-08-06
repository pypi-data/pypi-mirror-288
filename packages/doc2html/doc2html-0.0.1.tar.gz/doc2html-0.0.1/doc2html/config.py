import logging
from pathlib import Path


# Logger
LOGGING_LEVEL = "INFO"
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()
logger.setLevel(LOGGING_LEVEL)

ROOT = Path(__file__).parent.parent
SAMPLES = ROOT.joinpath("tests", "samples")

TRANSFORM_SERVICE_NAME = "document transformer"
TRANSFORM_SERVICE_VERSION = "0.0.1"
TRANSFORM_SERVICE_INFO = "Perform operations to transform documents between formats"

TRANSFORM_HOST = "localhost"
TRANSFORM_PORT = 5000
UNOSERVER_PORT = 2024

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'odt', 'ods', 'odp'}

# Path to the desired Python interpreter incl. libreoffice
if Path("/environments").exists():
    UNO_SERVER_PATH = "/environments/virtenv/bin/"
else:
    UNO_SERVER_PATH = ROOT.joinpath("environments", "virtenv", "bin").as_posix()

UNO_PYTHON = Path(UNO_SERVER_PATH).joinpath("python3").as_posix()
UNO_CONVERTER = Path(UNO_SERVER_PATH).joinpath("unoconvert").as_posix()
