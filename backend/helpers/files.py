import logging
from core.config import settings
from pathlib import Path
logger = logging.getLogger(__name__)


def init_folders_structure():
    path = Path(settings.IMAGES_FOLDER)
    if not path.exists():
        logger.info("Создание структуры папок")
        path.mkdir(parents=True, exist_ok=True)
        logger.info("Структура папок создана")
