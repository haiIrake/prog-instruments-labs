import aiohttp
import asyncio
import csv
import json
import logging
from pathlib import Path
from typing import Optional
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


class AsyncImageDownloader:
    """Асинхронный загрузчик изображений из csv-файла."""

    def __init__(self, max_concurrent: int, output_dir: str) -> None:
        """
        Инициализирует загрузчик изображений и создаёт необходимую директорию.
        :param max_concurrent: максимальное количество одновременных загрузок
        :param output_dir: каталог для сохранения изображений
        """
        self.max_concurrent = max_concurrent
        self.output_dir = Path(output_dir)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.downloaded_count = 0
        self.failed_count = 0
        self.total_urls = 0

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            logger.error(f"File system error while creating directory {self.output_dir}")

    async def download_single_image(self, session: aiohttp.ClientSession, url: str) -> Optional[Path]:
        """
        Скачивает одно изображение.
        :param session: сессия aiohttp
        :param url: URL изображения
        :returns: путь к загруженному файлу или None при ошибке
        """
        async with self.semaphore:
            filename = get_filename_from_url(url)
            filepath = self.output_dir / filename

            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        content = await response.read()

                        content_type = response.headers.get("Content-Type", "")
                        if not content_type.startswith("image/"):
                            logger.warning(f"URL is not an image: {url} (Content-Type: {content_type})")
                            self.failed_count += 1
                            return None

                        with open(filepath, "wb") as f:
                            f.write(content)

                        self.downloaded_count += 1
                        logger.info(
                            f"Downloaded: {filename} "
                            f"({self.downloaded_count + self.failed_count}/{self.total_urls})"
                        )
                        return filepath
                    else:
                        logger.error(f"HTTP error {response.status} for {url}")
                        self.failed_count += 1
                        return None

            except asyncio.TimeoutError:
                logger.error(f"Timeout downloading: {url}")
                self.failed_count += 1
                return None
            except aiohttp.ClientError as e:
                logger.error(f"Network error for {url}: {e}")
                self.failed_count += 1
                return None
            except Exception as e:
                logger.error(f"Unexpected error for {url}: {e}")
                self.failed_count += 1
                return None

    async def download_all_images(self, urls: list[str]) -> list[Path]:
        """
        Скачивает все изображения асинхронно.
        :param urls: список URL-адресов
        :returns: список путей к загруженным файлам
        """
        self.total_urls = len(urls)
        logger.info(f"Starting download of {self.total_urls} images...")

        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [
                self.download_single_image(session, url)
                for url in urls
            ]
            results = await asyncio.gather(*tasks)

        return [result for result in results if result is not None]

    def download_from_csv(self, csv_path: str) -> None:
        """
        Основной метод для загрузки изображений из csv-файла.
        :param csv_path: путь к csv-файлу
        """
        try:
            urls = extract_urls_from_csv(csv_path)

            asyncio.run(self.download_all_images(urls))

            logger.info(f"Download completed. Images saved to {self.output_dir.absolute()}")
        except Exception as e:
            logger.error(f"Critical error: {e}")


def main():
    try:
        source = load_config("settings.json")

        downloader = AsyncImageDownloader(
            max_concurrent=source["CONCURRENT"],
            output_dir=source["OUTPUT"]
        )

        downloader.download_from_csv(source["CSV_FILE"])
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
