from database import fs


def save_pdf(file_storage, filename):

    file_id = fs.put(file_storage, filename=filename)

    return file_id


def get_pdf(file_id):

    return fs.get(file_id)


def delete_pdf(file_id):

    if fs.exists(file_id):
        fs.delete(file_id)
