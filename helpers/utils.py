import os
import sys
from helpers._reports.logging_config import logger
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

LOCK_FILE = os.environ.get("LOCK_FILE")
VAR_DIR = Path(os.environ.get("FILES_PATH"))

#####################################################################################################################

def create_confirmation_file(filename):
    output_dir = os.getenv("FILES_PATH")

    name_part, ext = os.path.splitext(filename)
    prefix, timestamp = name_part.rsplit("_", 1)

    confirmation_prefix = f"{prefix}_potwierdzenie"
    new_name = f"{confirmation_prefix}_{timestamp}.xml"

    new_path = os.path.join(output_dir, new_name)

    xml_content = (
        '<?xml version="1.0" encoding="utf-8"?>'
        f"<{confirmation_prefix}>"
        "<info>OK</info>"
        f"</{confirmation_prefix}>"
    )
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(xml_content)


#####################################################################################################################

def check_artykuly_files():
    artykuly_xml_files = list(VAR_DIR.glob("artykuly_[0-9]*.xml")) or []
    artykuly_xml_files_sorted = sorted(artykuly_xml_files, key=lambda p: int(p.stem.split("_")[-1]))
    logger.info(f"Files artykuly_xml found: {len(artykuly_xml_files_sorted)}")
    logger.debug(f"Files artykuly_xml found: {artykuly_xml_files_sorted}")
    return artykuly_xml_files_sorted


def check_ceny_stany_files():
    ceny_stany_xml_files = list(VAR_DIR.glob("ceny_stany_[0-9]*.xml")) or []
    ceny_stany_xml_files_sorted = sorted(ceny_stany_xml_files, key=lambda p: int(p.stem.split("_")[-1]))
    logger.info(f"Files ceny_stany_xml found: {len(ceny_stany_xml_files_sorted)}")
    logger.debug(f"Files ceny_stany_xml found: {ceny_stany_xml_files_sorted}")
    return ceny_stany_xml_files_sorted


def check_all_files(artykuly_xml_files_sorted, ceny_stany_xml_files_sorted):
    if not artykuly_xml_files_sorted and not ceny_stany_xml_files_sorted:
            logger.debug(f"There are no files, the integrator will not start.")
            return True
    
#####################################################################################################################

def check_lock_file():
    if os.path.exists(LOCK_FILE):
        logger.error("Script is already running.")
        sys.exit()

def create_lock_file():
    open(LOCK_FILE, "w").close()

def delete_lock_file():
    os.remove(LOCK_FILE)

#####################################################################################################################

def create_basic_dirs():
    artykuly_archive_dir = VAR_DIR / "artykuly_archive"
    if not artykuly_archive_dir.is_dir():
        artykuly_archive_dir.mkdir()

    ceny_stany_archive_dir = VAR_DIR / "ceny_stany_archive"
    if not ceny_stany_archive_dir.is_dir():
        ceny_stany_archive_dir.mkdir()

    errors_archive_dir = VAR_DIR / "errors_archive"
    if not errors_archive_dir.is_dir():
        errors_archive_dir.mkdir()