from database import fs
from bson import ObjectId
import tempfile
import os


def save_pdf_to_gridfs(file):
    """
    Save uploaded PDF to MongoDB GridFS.
    Returns the ObjectId of the stored file.
    """

    pdf_id = fs.put(file, filename=file.filename, content_type="application/pdf")

    return str(pdf_id)


def download_pdf_from_gridfs(pdf_id):
    """
    Download a PDF from GridFS into a temporary file.
    Returns the temporary file path.
    """

    grid_out = fs.get(ObjectId(pdf_id))

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    temp.write(grid_out.read())
    temp.close()

    return temp.name


def delete_temp_file(path):
    """
    Delete temporary PDF after processing.
    """

    if os.path.exists(path):
        os.remove(path)


def delete_pdf_from_gridfs(pdf_id):
    """
    Delete PDF from GridFS.
    """

    fs.delete(ObjectId(pdf_id))
