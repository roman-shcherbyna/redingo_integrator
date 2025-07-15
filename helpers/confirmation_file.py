import os
from dotenv import load_dotenv

load_dotenv()

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

