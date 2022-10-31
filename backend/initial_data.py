from backend.helpers.files import init_folders_structure
from backend.db.init_db import init_db


def init() -> None:
    init_db()
    init_folders_structure()
