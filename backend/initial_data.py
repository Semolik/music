from helpers.files import init_folders_structure
from db.init_db import init_db


def init() -> None:
    init_db()
    init_folders_structure()
