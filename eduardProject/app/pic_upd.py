from flask import current_app
from PIL import Image
import secrets
import os


def save_picture(pict, path):
    hex = secrets.token_hex(8)
    _, ext = os.path.splitext(pict.filename)
    picture_fn = hex + ext;
    picture_path = os.path.join(current_app.root_path, path, picture_fn)
    image = Image.open(pict)
    image.save(picture_path)
    return picture_fn