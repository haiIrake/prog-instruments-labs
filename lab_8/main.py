import csv
import json
import logging
from pathlib import Path
from urllib.parse import urlparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_config(filename: str) -> dict:
    """
    Загружает данные конфигурации из json-файла.
    :param filename: путь к json-файлу
    :return: словарь с содержимым файла
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            config = json.load(file)
            logger.info(f"Loading configuration from {filename} completed")
            return config
    except FileNotFoundError:
        logger.error(f"File {filename} not found")
    except json.JSONDecodeError:
        logger.error(f"File {filename} isn't correct JSON")
    except Exception as e:
        logger.error(f"An error occurred while reading the file {filename}: {e}")


def extract_urls_from_csv(csv_path: str) -> list[str]:
    """
    Извлекает URL-адреса изображений из csv-файла.
    :param csv_path: путь к csv-файлу
    :returns: список URL-адресов
    """
    urls = []

    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row and row[0].strip():
                    url = row[0].strip()
                    if url.startswith(("http://", "https://")):
                        urls.append(url)
                    else:
                        logger.warning(f"Skipped invalid URL: {url}")

        if not urls:
            raise ValueError("CSV file contains no valid URLs")

        return urls

    except FileNotFoundError:
        logger.error(f"File {csv_path} not found")


def get_filename_from_url(url: str) -> str:
    """
    Генерирует имя файла из URL.
    :param url: URL изображения
    :returns: имя файла с расширением
    """
    parsed_url = urlparse(url)
    path = Path(parsed_url.path)

    if path.name:
        filename = path.name
    else:
        filename = f"{parsed_url.netloc}_{hash(url)}.jpg"

    safe_filename = "".join(
        c for c in filename if c.isalnum() or c in "._-"
    ).rstrip()

    return safe_filename or f"image_{hash(url)}.jpg"
