"""
scan.py:    When a new scan appears in the appropriate directory this program is
            triggered with the path of the file as an argument.
"""
import glob
import os
import shutil
import sys

from filler import fill
from forms import DateField
from forms import DirectoryField
from forms import Field
from forms import Form
from forms import ObjectField
from forms import PlainTextField
from forms import TextField
from forms import TimestampField
from hu import ObjectDict

ARCHIVE_DIR = os.environ.get(
    "ARCHIVE_DIR", os.path.join(os.path.expanduser("~"), ".archive")
)
db_path = os.path.join(ARCHIVE_DIR, ".database")

form = Form(
    [
        TimestampField("scanned_at", hidden=True),
        DateField("document_date"),
        PlainTextField("description"),
        DirectoryField("link_dir"),
    ]
)

if __name__ == "__main__":
    for file_arg in sys.argv[1:]:
        try:
            # Get information from user
            data = ObjectDict(fill(form))
            # Compute archive path
            y, m, d = data.scanned_at[:10].split("-")
            dir_path = os.path.join(ARCHIVE_DIR, y, m, d)
            os.makedirs(dir_path, exist_ok=True)
            num_files = len(glob.glob(os.path.join(dir_path, "*")))
            file_num = f"file_{num_files:04}"
            file_name, ext = os.path.splitext(os.path.basename(file_arg))
            archive_path = os.path.join(dir_path, f"{file_num}{ext}")
            # Compute path for destination link
            user_path = os.path.join(data.link_dir, f"{file_name}{ext}")
            print(data, y, m, d, dir_path, file_name, ext, archive_path, user_path)
            # Move input file to archive, then link to archive file under original name
            shutil.move(file_arg, archive_path)
            os.symlink(archive_path, user_path)
            # TODO: Store archival record
        except InterruptedError:
            sys.exit("Cancelled by user.")
